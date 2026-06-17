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
    ]:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        require(proc.returncode == 0, f"Command failed {command}: {proc.stdout}\n{proc.stderr}")

    result = read_json(ROOT / "ingestion" / "rtg_001" / "rtg_001_real_artifact_ingestion_result.json")
    require(result["case_id"] == "RTG-001", "Wrong case id")
    require(result["ingestion_type"] == "real_artifact_ingestion_via_approved_crosswalk", "Wrong ingestion type")
    require(result["original_reported_run_id"] == "EXT-002-FIXED", "Original run id not preserved")
    require(result["target_case_id"] == "RTG-001", "Wrong target case id")
    require(result["ingestion_status"] == "complete", "Ingestion not complete")
    require(result["from_state"] == "crosswalk_approved_for_rtg_001_ingestion", "Wrong from state")
    require(result["to_state"] == "artifact_ingested_as_rtg_001", "Wrong to state")
    require(result["next_state"] == "rtg_real_artifact_state_update_ready", "Wrong next state")
    require(result["actual_cost_receipt"]["total_cost_usd"] == 0.0219265, "Cost receipt mismatch")

    boundary = result["claim_boundary"]
    require(boundary["artifact_returned"] is True, "Artifact returned not preserved")
    require(boundary["crosswalk_approved"] is True, "Crosswalk approval not preserved")
    require(boundary["artifact_ingested_as_rtg_001"] is True, "Real artifact ingestion not recorded")
    require(boundary["rtg_state_updated_from_real_artifact"] is False, "State update must remain blocked")
    require(boundary["autonomous_theorem_proving_claimed"] is False, "Autonomous proof must remain blocked")
    require(boundary["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(boundary["human_or_formal_review_required"] is True, "Review requirement missing")

    preservation = result["preservation"]
    require(preservation["original_run_id_preserved"] is True, "Original run id preservation missing")
    require(preservation["cost_receipt_preserved"] is True, "Cost receipt preservation missing")
    require(preservation["mismatch_hidden"] is False, "Mismatch must not be hidden")
    require(preservation["direct_ingestion_without_crosswalk_blocked"] is True, "Direct ingestion block missing")

    print("RTG-001 wrapped real artifact ingestion test passed.")


if __name__ == "__main__":
    main()
