#!/usr/bin/env python3
"""Retrieve, verify, canonicalize, and seal the Experiment 003 source.

This stage performs integrity and partition assignment only. It does not compute
outcome statistics, fit RTG parameters, fit baselines, or expose locked-test row
content in the emitted manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_PATH = ROOT / "registry" / "experiment-003-dataset-selection-receipt.json"
DEFAULT_SOURCE_DIR = ROOT / "build" / "experiment-003-source"
DEFAULT_MANIFEST = ROOT / "results" / "experiment-003-sealed-split-manifest.json"
BASE_URL = "https://zenodo.org/records/4953982/files/{name}?download=1"


def digest_bytes(payload: bytes, algorithm: str) -> str:
    return hashlib.new(algorithm, payload).hexdigest()


def canonicalize_text(payload: bytes) -> str:
    text = payload.decode("utf-8-sig")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def data_rows(text: str) -> list[str]:
    rows: list[str] = []
    for raw in text.split("\n"):
        row = raw.strip()
        if not row or row.startswith("#"):
            continue
        rows.append(" ".join(row.split()))
    return rows


def partition_for_key(key: str) -> tuple[str, int, str]:
    digest = hashlib.sha256(key.encode("utf-8")).digest()
    bucket = int.from_bytes(digest[:8], "big") % 10
    if bucket <= 5:
        partition = "calibration"
    elif bucket <= 7:
        partition = "validation"
    else:
        partition = "locked_test"
    return partition, bucket, digest.hex()


def retrieve(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "RTG-Tests/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def build_manifest(receipt: dict[str, Any], source_dir: Path) -> dict[str, Any]:
    source_dir.mkdir(parents=True, exist_ok=True)
    file_records: list[dict[str, Any]] = []
    row_records: list[dict[str, Any]] = []

    for expected in receipt["files"]:
        name = expected["name"]
        url = BASE_URL.format(name=name)
        payload = retrieve(url)

        actual_md5 = digest_bytes(payload, "md5")
        if actual_md5 != expected["md5"]:
            raise ValueError(f"checksum mismatch for {name}: {actual_md5}")
        if len(payload) != expected["bytes"]:
            raise ValueError(f"byte-size mismatch for {name}: {len(payload)}")

        destination = source_dir / name
        destination.write_bytes(payload)
        canonical_text = canonicalize_text(payload)
        canonical_sha256 = hashlib.sha256(canonical_text.encode("utf-8")).hexdigest()
        source_sha256 = digest_bytes(payload, "sha256")

        rows = data_rows(canonical_text) if name.endswith("_Data.txt") else []
        file_records.append(
            {
                "name": name,
                "source_url": url,
                "bytes": len(payload),
                "md5_verified": actual_md5,
                "source_sha256": source_sha256,
                "canonical_text_sha256": canonical_sha256,
                "canonical_data_row_count": len(rows),
            }
        )

        for index, row in enumerate(rows):
            key = "\n".join(
                [receipt["source"]["record_doi"], name, str(index), row]
            )
            partition, bucket, row_key_sha256 = partition_for_key(key)
            record: dict[str, Any] = {
                "file_name": name,
                "zero_based_data_row_index": index,
                "row_key_sha256": row_key_sha256,
                "bucket": bucket,
                "partition": partition,
                "canonical_row_sha256": hashlib.sha256(row.encode("utf-8")).hexdigest(),
            }
            if partition != "locked_test":
                record["canonical_row_text"] = row
            else:
                record["canonical_row_text"] = None
                record["sealed"] = True
            row_records.append(record)

    partition_counts = {
        name: sum(1 for row in row_records if row["partition"] == name)
        for name in ("calibration", "validation", "locked_test")
    }
    manifest_core = {
        "manifest_id": "RTG-EXP-003-SEALED-SPLIT-001",
        "experiment_id": "RTG-EXP-003",
        "source_receipt_id": receipt["receipt_id"],
        "source_record_doi": receipt["source"]["record_doi"],
        "integrity_state": "ALL_SOURCE_FILES_VERIFIED",
        "analysis_state": "NOT_STARTED",
        "partition_rule": receipt["split"],
        "files": file_records,
        "rows": row_records,
        "partition_counts": partition_counts,
        "locks": {
            "outcome_statistics_computed": False,
            "rtg_parameters_fitted": False,
            "baseline_parameters_fitted": False,
            "locked_test_content_exposed": False,
            "partition_reassignment_allowed": False,
        },
        "claims": receipt["claims"],
    }
    canonical = json.dumps(manifest_core, sort_keys=True, separators=(",", ":"))
    manifest_core["manifest_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return manifest_core


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
    if receipt["selection_state"] != "LOCKED_BEFORE_ANALYSIS":
        raise ValueError("dataset selection receipt is not locked")

    manifest = build_manifest(receipt, args.source_dir)
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print("RTG Experiment 003 source integrity ingestion passed.")
    print(f"verified_files={len(manifest['files'])}")
    print(f"sealed_rows={manifest['partition_counts']['locked_test']}")
    print(f"manifest_sha256={manifest['manifest_sha256']}")


if __name__ == "__main__":
    main()
