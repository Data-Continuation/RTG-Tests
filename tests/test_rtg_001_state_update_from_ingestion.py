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
    ingest_proc = subprocess.run(
        [sys.executable, "ingestion/rtg_001/ingest_returned_artifacts.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    require(ingest_proc.returncode == 0, f"Ingestion failed: {ingest_proc.stdout}\n{ingest_proc.stderr}")

    update_proc = subprocess.run(
        [sys.executable, "state/rtg_001/update_state_from_ingestion.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    require(update_proc.returncode == 0, f"State update failed: {update_proc.stdout}\n{update_proc.stderr}")

    status = read_json(ROOT / "status" / "rtg_001_state_update.json")
    receipt = read_json(ROOT / "receipts" / "rtg_001" / "rtg_001_state_update_receipt.json")

    require(status["state_update_status"] == "recorded", "State update not recorded")
    require(status["from_state"] == "artifact_ingested", "Wrong from_state")
    require(status["to_state"] == "rtg_state_update_recorded", "Wrong to_state")
    require(status["claim_boundary"]["artifact_ingested"] is True, "Artifact ingestion not preserved")
    require(status["claim_boundary"]["rtg_state_update_recorded"] is True, "State update not preserved")
    require(status["claim_boundary"]["autonomous_theorem_proving_claimed"] is False, "False theorem-proving claim not blocked")
    require(status["claim_boundary"]["final_correctness_claimed"] is False, "False final correctness claim not blocked")
    require(status["claim_boundary"]["human_or_formal_review_required"] is True, "Review boundary missing")

    require(receipt["receipt_type"] == "rtg_state_update_from_ingestion", "Wrong receipt type")
    require(receipt["state_transition"]["from"] == "artifact_ingested", "Receipt wrong from state")
    require(receipt["state_transition"]["to"] == "rtg_state_update_recorded", "Receipt wrong to state")
    require(receipt["claim_boundary_preserved"] is True, "Receipt boundary not preserved")
    require(receipt["cost_receipt_preserved"] is True, "Receipt cost preservation missing")

    print("RTG-001 state update from ingestion test passed.")


if __name__ == "__main__":
    main()
