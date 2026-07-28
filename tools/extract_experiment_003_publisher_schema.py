#!/usr/bin/env python3
"""Retrieve checksum-bound publisher descriptions and emit exact schema evidence.

This stage does not fit models, compute outcome statistics, or expose locked-test rows.
It retrieves only the three publisher description files already named in the locked
selection receipt, verifies byte counts and MD5 digests, preserves exact text, and
emits a machine-readable extraction artifact for human review.
"""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "registry" / "experiment-003-dataset-selection-receipt.json"
OUTPUT = ROOT / "results" / "experiment-003-publisher-schema-extraction.json"
BASE_URL = "https://zenodo.org/records/4953982/files/{name}?download=1"


def retrieve(name: str) -> bytes:
    request = urllib.request.Request(
        BASE_URL.format(name=name), headers={"User-Agent": "RTG-Tests/1.0"}
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def canonical_text(payload: bytes) -> str:
    return payload.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def extract_lines(text: str) -> list[dict[str, Any]]:
    return [
        {"line_number": i + 1, "text": line}
        for i, line in enumerate(text.splitlines())
    ]


def main() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    descriptions = [f for f in receipt["files"] if f["name"].endswith("_Description.txt")]
    records: list[dict[str, Any]] = []

    for expected in descriptions:
        payload = retrieve(expected["name"])
        actual_md5 = hashlib.md5(payload).hexdigest()
        if actual_md5 != expected["md5"]:
            raise ValueError(f"checksum mismatch for {expected['name']}")
        if len(payload) != expected["bytes"]:
            raise ValueError(f"byte-size mismatch for {expected['name']}")
        text = canonical_text(payload)
        records.append(
            {
                "name": expected["name"],
                "bytes": len(payload),
                "md5_verified": actual_md5,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "exact_text": text,
                "lines": extract_lines(text),
            }
        )

    result = {
        "artifact_id": "RTG-EXP-003-PUBLISHER-SCHEMA-EXTRACTION-001",
        "experiment_id": "RTG-EXP-003",
        "source_record_doi": receipt["source"]["record_doi"],
        "state": "PUBLISHER_DESCRIPTION_EVIDENCE_EXTRACTED",
        "description_files": records,
        "locks": {
            "data_files_opened": False,
            "outcome_statistics_computed": False,
            "model_fit_performed": False,
            "locked_test_opened": False,
        },
        "next_state": "HUMAN_REVIEW_REQUIRED_BEFORE_EXECUTABLE_SCHEMA_LOCK",
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["artifact_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    print("RTG Experiment 003 publisher schema extraction passed.")
    for record in records:
        print(f"--- {record['name']} ---")
        print(record["exact_text"].rstrip())
    print(f"artifact_sha256={result['artifact_sha256']}")


if __name__ == "__main__":
    main()
