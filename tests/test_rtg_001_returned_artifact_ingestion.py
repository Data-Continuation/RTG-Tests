#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    proc = subprocess.run(
        [sys.executable, "ingestion/rtg_001/ingest_returned_artifacts.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    require(proc.returncode == 0, f"Ingestion command failed: {proc.stdout}\n{proc.stderr}")

    result = read_json(ROOT / "ingestion" / "rtg_001" / "rtg_001_ingestion_result.json")
    require(result["ingestion_status"] == "complete", "Ingestion did not complete")
    require(result["from_state"] == "artifact_returned", "Wrong from_state")
    require(result["to_state"] == "artifact_ingested", "Wrong to_state")
    require(result["next_state"] == "rtg_state_update_ready", "Wrong next_state")
    require(result["claim_boundary_preserved"] is True, "Claim boundary not preserved")
    require(result["sources_verified"] is True, "Sources not verified")
    require(result["cost_receipt"]["pre_execution_estimate_replaced_by_receipt"] is True, "Cost receipt did not replace estimate")
    require(result["false_claims_blocked"]["autonomous_theorem_proving_claimed"] is False, "False theorem-proving claim not blocked")
    require(result["false_claims_blocked"]["final_correctness_claimed"] is False, "False correctness claim not blocked")
    print("RTG-001 returned artifact ingestion test passed.")


if __name__ == "__main__":
    main()
