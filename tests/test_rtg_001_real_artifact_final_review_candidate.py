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
    commands = [
        "evidence/rtg_001/normalize_returned_artifact.py",
        "evidence/rtg_001/approve_crosswalk.py",
        "ingestion/rtg_001/ingest_wrapped_real_artifact.py",
        "state/rtg_001/update_state_from_real_artifact.py",
        "review/rtg_001/refresh_final_review_candidate_from_real_artifact.py"
    ]
    for script in commands:
        proc = subprocess.run([sys.executable, script], cwd=ROOT, text=True, capture_output=True, timeout=30)
        require(proc.returncode == 0, f"Command failed {script}: {proc.stdout}\n{proc.stderr}")

    candidate = read_json(ROOT / "candidates" / "rtg_001" / "rtg_001_real_artifact_final_review_candidate.json")
    require(candidate["case_id"] == "RTG-001", "Wrong case id")
    require(candidate["candidate_type"] == "real_artifact_final_review_candidate", "Wrong candidate type")
    require(candidate["candidate_status"] == "ready_for_human_or_formal_review_with_real_artifact_evidence", "Wrong candidate status")
    require(candidate["original_reported_run_id"] == "EXT-002-FIXED", "Original run id not preserved")
    require(candidate["actual_cost_receipt"]["total_cost_usd"] == 0.0219265, "Cost receipt mismatch")

    boundary = candidate["claim_boundary"]
    require(boundary["real_artifact_final_review_candidate_created"] is True, "Candidate not created")
    require(boundary["artifact_returned"] is True, "Artifact return not preserved")
    require(boundary["crosswalk_approved"] is True, "Crosswalk not preserved")
    require(boundary["artifact_ingested_as_rtg_001"] is True, "Artifact ingestion not preserved")
    require(boundary["rtg_state_updated_from_real_artifact"] is True, "Real state update not preserved")
    require(boundary["ready_for_human_or_formal_review"] is True, "Review readiness missing")
    require(boundary["autonomous_theorem_proving_claimed"] is False, "Autonomous proof must remain blocked")
    require(boundary["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(boundary["human_or_formal_review_required"] is True, "Review requirement missing")

    print("RTG-001 real artifact final review candidate test passed.")


if __name__ == "__main__":
    main()
