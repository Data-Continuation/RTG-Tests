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
    ]:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        require(proc.returncode == 0, f"Command failed {command}: {proc.stdout}\n{proc.stderr}")

    packet = read_json(ROOT / "review" / "rtg_001" / "rtg_001_review_packet.json")
    require(packet["case_id"] == "RTG-001", "Wrong case id")
    require(packet["packet_type"] == "final_review_candidate_packet", "Wrong packet type")
    require(packet["review_route"] == "route_to_review", "Wrong review route")
    require(packet["review_status"] == "candidate_ready_pending_real_artifact_receipt", "Wrong review status")
    require(packet["cost_summary"]["actual_previous_stage_paid_api_cost_usd"] == 0.0, "Previous stage paid API cost should be zero until solver receipt")
    require(packet["cost_summary"]["solver_actual_cost_receipt"] is None, "Solver receipt should be pending")
    require(packet["claim_boundary"]["review_packet_generated"] is True, "Review packet not marked generated")
    require(packet["claim_boundary"]["final_review_candidate_ready"] is True, "Final review candidate not ready")
    require(packet["claim_boundary"]["autonomous_theorem_proving_claimed"] is False, "False autonomous theorem proof claim not blocked")
    require(packet["claim_boundary"]["final_correctness_claimed"] is False, "False final correctness claim not blocked")
    require(packet["claim_boundary"]["human_or_formal_review_required"] is True, "Review requirement missing")

    print("RTG-001 review packet generation test passed.")


if __name__ == "__main__":
    main()
