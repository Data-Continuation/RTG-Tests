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
    for command in [
        [sys.executable, "evidence/rtg_001/normalize_returned_artifact.py"],
        [sys.executable, "evidence/rtg_001/approve_crosswalk.py"],
        [sys.executable, "ingestion/rtg_001/ingest_wrapped_real_artifact.py"],
        [sys.executable, "state/rtg_001/update_state_from_real_artifact.py"],
    ]:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        require(proc.returncode == 0, f"Command failed {command}: {proc.stdout}\n{proc.stderr}")

    status = read_json(ROOT / "status" / "rtg_001_real_artifact_state_update.json")
    receipt = read_json(ROOT / "receipts" / "rtg_001" / "rtg_001_real_artifact_state_update_receipt.json")

    require(status["case_id"] == "RTG-001", "Wrong status case id")
    require(status["state_update_type"] == "real_artifact_state_update", "Wrong update type")
    require(status["state_update_status"] == "recorded", "State update not recorded")
    require(status["original_reported_run_id"] == "EXT-002-FIXED", "Original run id not preserved")
    require(status["target_case_id"] == "RTG-001", "Wrong target case")
    require(status["from_state"] == "artifact_ingested_as_rtg_001", "Wrong from state")
    require(status["to_state"] == "rtg_state_updated_from_real_artifact", "Wrong to state")
    require(status["next_state"] == "real_artifact_review_candidate_refresh_ready", "Wrong next state")
    require(status["actual_cost_receipt"]["total_cost_usd"] == 0.0219265, "Cost receipt mismatch")

    boundary = status["claim_boundary"]
    require(boundary["artifact_returned"] is True, "Artifact return not preserved")
    require(boundary["crosswalk_approved"] is True, "Crosswalk approval not preserved")
    require(boundary["artifact_ingested_as_rtg_001"] is True, "Artifact ingestion not preserved")
    require(boundary["rtg_state_updated_from_real_artifact"] is True, "Real state update not recorded")
    require(boundary["autonomous_theorem_proving_claimed"] is False, "Autonomous proof must remain blocked")
    require(boundary["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(boundary["human_or_formal_review_required"] is True, "Review requirement missing")

    require(receipt["receipt_type"] == "rtg_real_artifact_state_update_receipt", "Wrong receipt type")
    require(receipt["state_transition"]["from"] == "artifact_ingested_as_rtg_001", "Receipt wrong from state")
    require(receipt["state_transition"]["to"] == "rtg_state_updated_from_real_artifact", "Receipt wrong to state")
    require(receipt["original_reported_run_id_preserved"] is True, "Receipt did not preserve original run id")
    require(receipt["cost_receipt_preserved"] is True, "Receipt did not preserve cost")
    require(receipt["claim_boundary_preserved"] is True, "Receipt did not preserve boundary")
    require(receipt["final_claims_blocked"] is True, "Receipt did not block final claims")

    print("RTG-001 real artifact state update test passed.")


if __name__ == "__main__":
    main()
