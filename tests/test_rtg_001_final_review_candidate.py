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
        [sys.executable, "ingestion/rtg_001/ingest_returned_artifacts.py"],
        [sys.executable, "state/rtg_001/update_state_from_ingestion.py"],
        [sys.executable, "state/rtg_001/select_next_instruction.py"],
        [sys.executable, "review/rtg_001/generate_review_packet.py"],
        [sys.executable, "review/rtg_001/finalize_review_candidate.py"],
    ]:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        require(proc.returncode == 0, f"Command failed {command}: {proc.stdout}\n{proc.stderr}")

    candidate = read_json(ROOT / "candidates" / "rtg_001" / "rtg_001_final_review_candidate.json")
    require(candidate["case_id"] == "RTG-001", "Wrong case id")
    require(candidate["candidate_type"] == "final_review_candidate", "Wrong candidate type")
    require(candidate["review_route"] == "route_to_review", "Wrong review route")
    require(candidate["candidate_status"] == "ready_for_human_or_formal_review_pending_real_artifact_receipt", "Wrong candidate status")
    require("request_real_artifact_ingestion" in candidate["decision_options"], "Missing real artifact decision option")
    require("reject_claim_as_premature" in candidate["decision_options"], "Missing premature claim rejection option")

    boundary = candidate["claim_boundary"]
    require(boundary["final_review_candidate_created"] is True, "Candidate not marked created")
    require(boundary["ready_for_review"] is True, "Candidate not ready for review")
    require(boundary["artifact_returned"] is False, "Must not claim artifact returned")
    require(boundary["artifact_ingested_from_real_artifact"] is False, "Must not claim real artifact ingestion")
    require(boundary["rtg_state_updated_from_real_artifact"] is False, "Must not claim real artifact state update")
    require(boundary["autonomous_theorem_proving_claimed"] is False, "Must not claim autonomous theorem proof")
    require(boundary["final_correctness_claimed"] is False, "Must not claim final correctness")
    require(boundary["human_or_formal_review_required"] is True, "Review requirement missing")

    print("RTG-001 final review candidate test passed.")


if __name__ == "__main__":
    main()
