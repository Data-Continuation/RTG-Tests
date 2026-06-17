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
    ]:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        require(proc.returncode == 0, f"Command failed {command}: {proc.stdout}\n{proc.stderr}")

    approval = read_json(ROOT / "evidence" / "rtg_001" / "crosswalk_approval.json")
    wrapped = read_json(ROOT / "evidence" / "rtg_001" / "rtg_001_wrapped_real_artifact_receipt.json")

    require(approval["case_id"] == "RTG-001", "Wrong approval case id")
    require(approval["approval_type"] == "returned_artifact_crosswalk_approval", "Wrong approval type")
    require(approval["original_reported_run_id"] == "EXT-002-FIXED", "Original run id not preserved")
    require(approval["target_case_id"] == "RTG-001", "Wrong target case")
    require(approval["approval_status"] == "approved_for_wrapped_ingestion_candidate", "Approval status invalid")
    require(approval["preserved_mismatch"]["mismatch_hidden"] is False, "Mismatch must not be hidden")
    require(approval["claim_boundary"]["crosswalk_approved"] is True, "Crosswalk not approved")
    require(approval["claim_boundary"]["artifact_ingested_as_rtg_001"] is False, "Approval must not claim ingestion")
    require(approval["claim_boundary"]["rtg_state_updated_from_real_artifact"] is False, "Approval must not claim state update")
    require(approval["claim_boundary"]["final_correctness_claimed"] is False, "Must not claim final correctness")

    require(wrapped["case_id"] == "RTG-001", "Wrong wrapped case id")
    require(wrapped["wrapped_from_original_run_id"] == "EXT-002-FIXED", "Wrapped receipt must preserve original run id")
    require(wrapped["receipt_type"] == "wrapped_real_artifact_receipt_for_rtg_001", "Wrong wrapped receipt type")
    require(wrapped["cost_receipt"]["total_cost_usd"] == 0.0219265, "Wrapped cost mismatch")
    require(wrapped["claim_boundary"]["candidate_generation_only"] is True, "Claim boundary wrapper missing")
    require(wrapped["claim_boundary"]["final_correctness_claimed"] is False, "Wrapped receipt must not claim final correctness")
    require(wrapped["crosswalk"]["approved"] is True, "Wrapped crosswalk not approved")
    require(wrapped["crosswalk"]["direct_ingestion_without_crosswalk_blocked"] is True, "Direct ingestion block missing")
    require(wrapped["ingestion_posture"] == "eligible_for_rtg_001_real_artifact_ingestion", "Wrong ingestion posture")

    print("RTG-001 crosswalk approval test passed.")


if __name__ == "__main__":
    main()
