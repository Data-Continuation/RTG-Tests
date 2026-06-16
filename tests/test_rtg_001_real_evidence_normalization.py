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
        [sys.executable, "evidence/rtg_001/normalize_returned_artifact.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    require(proc.returncode == 0, f"Normalizer failed: {proc.stdout}\n{proc.stderr}")

    candidate = read_json(ROOT / "evidence" / "rtg_001" / "normalized_ingestion_candidate.json")
    require(candidate["case_id"] == "RTG-001", "Wrong case id")
    require(candidate["candidate_type"] == "normalized_returned_artifact_ingestion_candidate", "Wrong candidate type")
    require(candidate["original_reported_run_id"] == "EXT-002-FIXED", "Original run id must be preserved")
    require(candidate["target_case_id"] == "RTG-001", "Target case id must be RTG-001")
    require(candidate["crosswalk_status"] == "required_and_recorded", "Crosswalk status must be recorded")
    require(candidate["ingestion_posture"] == "candidate_not_direct_ingestion", "Must not claim direct ingestion")
    require(candidate["actual_cost_receipt"]["total_cost_usd"] == 0.0219265, "Cost receipt mismatch")
    require(candidate["actual_cost_receipt"]["total_tokens"] == 3193, "Token count mismatch")

    boundary = candidate["claim_boundary"]
    require(boundary["artifact_returned"] is True, "Artifact returned must be true")
    require(boundary["actual_solver_cost_receipt_detected"] is True, "Actual cost receipt missing")
    require(boundary["artifact_ingested_as_rtg_001"] is False, "Must not claim RTG-001 ingestion yet")
    require(boundary["rtg_state_updated_from_real_artifact"] is False, "Must not claim RTG state update yet")
    require(boundary["crosswalk_required_before_ingestion"] is True, "Crosswalk requirement missing")
    require(boundary["autonomous_theorem_proving_claimed"] is False, "Must not claim autonomous proof")
    require(boundary["final_correctness_claimed"] is False, "Must not claim final correctness")

    print("RTG-001 real evidence normalization test passed.")


if __name__ == "__main__":
    main()
