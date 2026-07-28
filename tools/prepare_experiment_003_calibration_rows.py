#!/usr/bin/env python3
"""Prepare Experiment 003 calibration and validation rows without test leakage.

Consumes the sealed split manifest produced by the integrity-ingestion stage. Only
rows whose manifest partition is calibration or validation and whose canonical
text is already unsealed are parsed. Locked-test rows must remain content-free.
No model is fitted and no outcome summary is computed by this stage.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "registries" / "experiment-003-executable-source-schema.json"
DEFAULT_MANIFEST = ROOT / "results" / "experiment-003-sealed-split-manifest.json"
DEFAULT_OUTPUT = ROOT / "results" / "experiment-003-calibration-rows.json"

ARRAY_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*(\{.*\})\s*$")
PAIR_RE = re.compile(r"\{\s*([^,{}]+)\s*,\s*([^{}]+?)\s*\}")
NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")


def parse_brace_array(text: str) -> list[float]:
    converted = text.replace("{", "[").replace("}", "]")
    value = ast.literal_eval(converted)
    if not isinstance(value, list):
        raise ValueError("expected brace-delimited array")
    return [float(item) for item in value]


def parse_fig3(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    prefixes = {"nbar", "expfidelity", "errornbar", "errorsexpfidelity"}
    for record in records:
        match = ARRAY_RE.match(record["canonical_row_text"])
        if not match or match.group(1) not in prefixes:
            continue
        group = groups.setdefault(record["partition"], {})
        name = match.group(1)
        if name in group:
            raise ValueError(f"duplicate Fig3 array {name} in {record['partition']}")
        group[name] = parse_brace_array(match.group(2))
        group.setdefault("source_row_hashes", []).append(record["canonical_row_sha256"])

    output: list[dict[str, Any]] = []
    required = sorted(prefixes)
    for partition, group in groups.items():
        if not all(name in group for name in required):
            continue
        lengths = {len(group[name]) for name in required}
        if len(lengths) != 1:
            raise ValueError(f"unaligned Fig3 arrays in {partition}")
        for index, values in enumerate(zip(*(group[name] for name in required))):
            mapped = dict(zip(required, values))
            output.append(
                {
                    "analysis_unit": "fig3_experimental_fidelity",
                    "partition": partition,
                    "element_index": index,
                    "predictor_name": "mean_photon_number",
                    "predictor": mapped["nbar"],
                    "target": mapped["expfidelity"] / 100.0,
                    "predictor_error": mapped["errornbar"],
                    "target_error": mapped["errorsexpfidelity"] / 100.0,
                    "source_row_hashes": sorted(group["source_row_hashes"]),
                }
            )
    return output


def parse_central_and_error(text: str) -> tuple[float, float | None]:
    pieces = text.split("+-", maxsplit=1)
    central_match = NUMBER_RE.search(pieces[0])
    if not central_match:
        raise ValueError(f"missing central value: {text}")
    central = float(central_match.group(0))
    error = None
    if len(pieces) == 2:
        error_match = NUMBER_RE.search(pieces[1])
        if not error_match:
            raise ValueError(f"missing uncertainty value: {text}")
        error = float(error_match.group(0))
    return central, error


def parse_fig4(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for record in records:
        text = record["canonical_row_text"]
        if "Simulated" in text or "theory" in text.lower():
            continue
        pairs = PAIR_RE.findall(text)
        for index, (raw_x, raw_y) in enumerate(pairs):
            x_match = NUMBER_RE.search(raw_x)
            if not x_match:
                continue
            central, error = parse_central_and_error(raw_y)
            output.append(
                {
                    "analysis_unit": "fig4_experimental_fidelity",
                    "partition": record["partition"],
                    "element_index": index,
                    "predictor_name": "delay_tau",
                    "predictor": float(x_match.group(0)),
                    "target": central / 100.0,
                    "predictor_error": None,
                    "target_error": None if error is None else error / 100.0,
                    "source_row_hashes": [record["canonical_row_sha256"]],
                }
            )
    return output


def prepare(manifest: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    if schema["state"] != "LOCKED_BEFORE_OUTCOME_STATISTICS_OR_MODEL_FIT":
        raise ValueError("source schema is not locked")
    if manifest["manifest_id"] != schema["evidence"]["sealed_manifest_id"]:
        raise ValueError("manifest identity does not match schema")
    if manifest["locks"]["locked_test_content_exposed"]:
        raise ValueError("manifest declares locked-test exposure")

    visible: dict[str, list[dict[str, Any]]] = {"Fig3_Data.txt": [], "Fig4_Data.txt": []}
    locked_rows = 0
    for row in manifest["rows"]:
        if row["partition"] == "locked_test":
            locked_rows += 1
            if row.get("canonical_row_text") is not None:
                raise ValueError("locked-test row content exposed")
            continue
        if row["partition"] not in {"calibration", "validation"}:
            raise ValueError(f"unexpected partition {row['partition']}")
        if row.get("canonical_row_text") is None:
            raise ValueError("allowed partition row is unexpectedly sealed")
        if row["file_name"] in visible:
            visible[row["file_name"]].append(row)

    parsed = parse_fig3(visible["Fig3_Data.txt"]) + parse_fig4(visible["Fig4_Data.txt"])
    for row in parsed:
        if not 0.0 <= row["target"] <= 1.0:
            raise ValueError("target outside locked range")

    counts = {
        partition: sum(1 for row in parsed if row["partition"] == partition)
        for partition in ("calibration", "validation")
    }
    source_visible = sum(len(rows) for rows in visible.values())
    used_hashes = {digest for row in parsed for digest in row["source_row_hashes"]}
    coverage = 0.0 if source_visible == 0 else len(used_hashes) / source_visible
    state = "READY_FOR_CALIBRATION_FIT" if coverage >= 0.70 and all(counts.values()) else "STOP_REQUIRED"

    core = {
        "receipt_id": "RTG-EXP-003-CALIBRATION-ROWS-001",
        "experiment_id": "RTG-EXP-003",
        "schema_id": schema["schema_id"],
        "manifest_id": manifest["manifest_id"],
        "state": state,
        "records": parsed,
        "record_counts": counts,
        "mapping_coverage": coverage,
        "minimum_mapping_coverage": 0.70,
        "locked_test_rows_seen_as_sealed_metadata_only": locked_rows,
        "locked_test_content_opened": False,
        "outcome_statistics_computed": False,
        "model_fit_performed": False,
    }
    canonical = json.dumps(core, sort_keys=True, separators=(",", ":"))
    core["receipt_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return core


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    receipt = prepare(manifest, schema)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"state={receipt['state']}")
    print(f"calibration_records={receipt['record_counts']['calibration']}")
    print(f"validation_records={receipt['record_counts']['validation']}")
    print(f"mapping_coverage={receipt['mapping_coverage']:.6f}")
    print("locked_test_content_opened=false")


if __name__ == "__main__":
    main()
