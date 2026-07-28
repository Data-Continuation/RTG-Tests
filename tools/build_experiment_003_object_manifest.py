#!/usr/bin/env python3
"""Build the corrected Experiment 003 observation-level sealed manifest.

The partition unit is one publisher-aligned experimental observation. Figure 3
arrays are aligned by zero-based element index; Figure 4 experimental pairs are
individual objects. Theoretical/simulated records are excluded. Locked-test
object values are sealed immediately after deterministic assignment.

This stage performs no outcome statistics and no model fitting.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_PATH = ROOT / "registry" / "experiment-003-dataset-selection-receipt.json"
SPLIT_PATH = ROOT / "registries" / "experiment-003-composite-object-split.json"
DEFAULT_SOURCE_DIR = ROOT / "build" / "experiment-003-object-source"
DEFAULT_OUTPUT = ROOT / "results" / "experiment-003-object-manifest.json"
BASE_URL = "https://zenodo.org/records/4953982/files/{name}?download=1"
ARRAY_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*(\{.*\})\s*$")
PAIR_RE = re.compile(r"\{\s*([^,{}]+)\s*,\s*([^{}]+?)\s*\}")
NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")


def retrieve(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "RTG-Tests/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def canonicalize(payload: bytes) -> str:
    return payload.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def parse_brace_array(text: str) -> list[float]:
    value = ast.literal_eval(text.replace("{", "[").replace("}", "]"))
    if not isinstance(value, list):
        raise ValueError("expected brace-delimited numeric array")
    return [float(item) for item in value]


def parse_central_error(text: str) -> tuple[float, float | None]:
    pieces = text.split("+-", maxsplit=1)
    central = NUMBER_RE.search(pieces[0])
    if not central:
        raise ValueError(f"missing central value: {text}")
    error = None
    if len(pieces) == 2:
        match = NUMBER_RE.search(pieces[1])
        if not match:
            raise ValueError(f"missing uncertainty: {text}")
        error = float(match.group(0))
    return float(central.group(0)), error


def figure3_objects(text: str) -> list[dict[str, Any]]:
    arrays: dict[str, list[float]] = {}
    wanted = {"nbar", "expfidelity", "errornbar", "errorsexpfidelity"}
    for raw in text.splitlines():
        row = " ".join(raw.strip().split())
        match = ARRAY_RE.match(row)
        if match and match.group(1) in wanted:
            arrays[match.group(1)] = parse_brace_array(match.group(2))
    if set(arrays) != wanted:
        raise ValueError(f"Figure 3 required arrays missing: {sorted(wanted - set(arrays))}")
    lengths = {len(arrays[name]) for name in wanted}
    if len(lengths) != 1:
        raise ValueError("Figure 3 arrays are not aligned")
    objects = []
    for index in range(next(iter(lengths))):
        objects.append({
            "analysis_unit": "fig3_experimental_fidelity",
            "element_index": index,
            "predictor_name": "mean_photon_number",
            "predictor": arrays["nbar"][index],
            "target": arrays["expfidelity"][index] / 100.0,
            "predictor_error": arrays["errornbar"][index],
            "target_error": arrays["errorsexpfidelity"][index] / 100.0,
        })
    return objects


def figure4_objects(text: str) -> list[dict[str, Any]]:
    experimental_lines: list[str] = []
    active = False
    for raw in text.splitlines():
        row = " ".join(raw.strip().split())
        lower = row.lower()
        if row.startswith("Data points, {tau, teleportation fidelity in percent}"):
            active = True
            continue
        if active and ("simulated" in lower or "theory" in lower):
            break
        if active and row:
            experimental_lines.append(row)
    body = " ".join(experimental_lines)
    objects = []
    for index, (raw_x, raw_y) in enumerate(PAIR_RE.findall(body)):
        x_match = NUMBER_RE.search(raw_x)
        if not x_match:
            continue
        central, error = parse_central_error(raw_y)
        objects.append({
            "analysis_unit": "fig4_experimental_fidelity",
            "element_index": index,
            "predictor_name": "delay_tau",
            "predictor": float(x_match.group(0)),
            "target": central / 100.0,
            "predictor_error": None,
            "target_error": None if error is None else error / 100.0,
        })
    if not objects:
        raise ValueError("no Figure 4 experimental observations parsed")
    return objects


def partition_for_object(object_id: str, split: dict[str, Any]) -> tuple[str, int, str]:
    salt = split["allocation"]["salt"]
    digest = hashlib.sha256(f"{salt}\n{object_id}".encode("utf-8")).hexdigest()
    bucket = int(digest[:16], 16) % 100
    if bucket <= 59:
        partition = "calibration"
    elif bucket <= 79:
        partition = "validation"
    else:
        partition = "locked_test"
    return partition, bucket, digest


def build_manifest(receipt: dict[str, Any], split: dict[str, Any], source_dir: Path) -> dict[str, Any]:
    if split["state"] != "LOCKED_BEFORE_COMPOSITE_ASSIGNMENT":
        raise ValueError("composite split is not locked")
    source_dir.mkdir(parents=True, exist_ok=True)
    parsed: list[dict[str, Any]] = []
    source_files: list[dict[str, Any]] = []
    expected_by_name = {item["name"]: item for item in receipt["files"]}
    for name, parser in (("Fig3_Data.txt", figure3_objects), ("Fig4_Data.txt", figure4_objects)):
        expected = expected_by_name[name]
        payload = retrieve(BASE_URL.format(name=name))
        if hashlib.md5(payload).hexdigest() != expected["md5"] or len(payload) != expected["bytes"]:
            raise ValueError(f"source integrity mismatch for {name}")
        destination = source_dir / name
        destination.write_bytes(payload)
        text = canonicalize(payload)
        source_files.append({
            "name": name,
            "bytes": len(payload),
            "md5_verified": expected["md5"],
            "source_sha256": hashlib.sha256(payload).hexdigest(),
            "canonical_text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })
        parsed.extend(parser(text))

    objects: list[dict[str, Any]] = []
    for item in parsed:
        identity_core = {
            "source_record_doi": receipt["source"]["record_doi"],
            "analysis_unit": item["analysis_unit"],
            "element_index": item["element_index"],
            "predictor_name": item["predictor_name"],
        }
        object_id = hashlib.sha256(json.dumps(identity_core, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        partition, bucket, assignment_sha256 = partition_for_object(object_id, split)
        values_sha256 = hashlib.sha256(json.dumps(item, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        record: dict[str, Any] = {
            "object_id": object_id,
            "analysis_unit": item["analysis_unit"],
            "element_index": item["element_index"],
            "predictor_name": item["predictor_name"],
            "partition": partition,
            "bucket": bucket,
            "assignment_sha256": assignment_sha256,
            "values_sha256": values_sha256,
        }
        if partition == "locked_test":
            record.update({"sealed": True, "values": None})
        else:
            record.update({"sealed": False, "values": {
                "predictor": item["predictor"],
                "target": item["target"],
                "predictor_error": item["predictor_error"],
                "target_error": item["target_error"],
            }})
        objects.append(record)

    counts = {name: sum(o["partition"] == name for o in objects) for name in ("calibration", "validation", "locked_test")}
    core = {
        "manifest_id": "RTG-EXP-003-OBJECT-MANIFEST-001",
        "experiment_id": "RTG-EXP-003",
        "split_id": split["split_id"],
        "supersedes_for_fitting": split["supersedes_for_fitting"],
        "source_record_doi": receipt["source"]["record_doi"],
        "partition_unit": "publisher_aligned_experimental_observation",
        "source_files": source_files,
        "objects": objects,
        "partition_counts": counts,
        "locks": {
            "locked_test_content_exposed": False,
            "outcome_statistics_computed": False,
            "model_fit_performed": False,
            "partition_reassignment_allowed": False,
        },
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["manifest_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return core


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    split = json.loads(SPLIT_PATH.read_text(encoding="utf-8"))
    manifest = build_manifest(receipt, split, args.source_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("state=OBJECT_MANIFEST_GENERATED")
    print(f"objects={len(manifest['objects'])}")
    print(f"calibration={manifest['partition_counts']['calibration']}")
    print(f"validation={manifest['partition_counts']['validation']}")
    print(f"locked_test={manifest['partition_counts']['locked_test']}")
    print("locked_test_content_exposed=false")
    print("model_fit_performed=false")


if __name__ == "__main__":
    main()
