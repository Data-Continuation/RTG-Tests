#!/usr/bin/env python3
"""Register RTG formal posture records into an indexed posture registry."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
POSTURES = {
    "formally_consistent",
    "formally_inconsistent",
    "underconstrained",
    "mixed_or_requires_review",
    "blocked",
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_formal_posture_record(payload: dict[str, Any]) -> bool:
    return (
        payload.get("schema_version") == "1.0"
        and isinstance(payload.get("solver_run_id"), str)
        and payload.get("formal_posture") in POSTURES
        and isinstance(payload.get("case_postures"), list)
        and isinstance(payload.get("receipt"), dict)
    )


def record_entry(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "solver_run_id": payload["solver_run_id"],
        "formal_posture": payload["formal_posture"],
        "case_count": payload.get("admissibility_summary", {}).get("case_count", len(payload.get("case_postures", []))),
        "source_path": path.as_posix(),
        "source_sha256": sha256_file(path),
        "source_solver_results": payload.get("source_solver_results", ""),
        "generated": payload.get("generated", ""),
        "receipt": payload.get("receipt", {}),
    }


def summarize(entries: list[dict[str, Any]]) -> dict[str, Any]:
    posture_counts: dict[str, int] = {}
    total_cases = 0

    for entry in entries:
        posture = entry["formal_posture"]
        posture_counts[posture] = posture_counts.get(posture, 0) + 1
        total_cases += int(entry.get("case_count", 0))

    return {
        "record_count": len(entries),
        "total_case_count": total_cases,
        "formal_posture_counts": posture_counts,
        "ready_for_formal_claim_count": posture_counts.get("formally_consistent", 0),
        "review_required_count": (
            posture_counts.get("underconstrained", 0)
            + posture_counts.get("mixed_or_requires_review", 0)
            + posture_counts.get("formally_inconsistent", 0)
            + posture_counts.get("blocked", 0)
        ),
    }


def build_registry(input_dir: Path, output_path: Path) -> Path:
    entries = []

    for path in sorted(input_dir.rglob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and is_formal_posture_record(payload):
            entries.append(record_entry(path, payload))

    registry = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "registry_type": "rtg_formal_posture_registry",
        "formal_posture_records": entries,
        "summary": summarize(entries),
        "receipt": {
            "registry_surface": "rtg_formal_posture_registry",
            "input_directory": input_dir.as_posix(),
            "record_hashes": [entry["source_sha256"] for entry in entries],
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RTG formal posture registry.")
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    out = build_registry(Path(args.input_dir), Path(args.output))
    print("Wrote RTG formal posture registry: " + str(out))


if __name__ == "__main__":
    main()
