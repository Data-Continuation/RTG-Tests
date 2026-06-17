#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "evidence" / "rtg_001" / "crosswalk_policy.json"
CANDIDATE = ROOT / "evidence" / "rtg_001" / "normalized_ingestion_candidate.json"
OUT = ROOT / "evidence" / "rtg_001" / "crosswalk_approval.json"
WRAPPED = ROOT / "evidence" / "rtg_001" / "rtg_001_wrapped_real_artifact_receipt.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    policy = read_json(POLICY)
    candidate = read_json(CANDIDATE)

    require(policy["case_id"] == "RTG-001", "Wrong policy case id")
    require(candidate["case_id"] == "RTG-001", "Wrong candidate case id")
    require(candidate["original_reported_run_id"] in policy["allowed_original_run_ids"], "Original run id not allowed")
    require(candidate["target_case_id"] == policy["target_case_id"], "Target case mismatch")
    require(candidate["claim_boundary"]["artifact_returned"] is True, "Artifact return not established")
    require(candidate["claim_boundary"]["actual_solver_cost_receipt_detected"] is True, "Cost receipt missing")
    require(candidate["claim_boundary"]["artifact_ingested_as_rtg_001"] is False, "Candidate must not pre-claim ingestion")
    require(candidate["claim_boundary"]["crosswalk_required_before_ingestion"] is True, "Crosswalk requirement missing")

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    approval = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "approval_type": "returned_artifact_crosswalk_approval",
        "original_reported_run_id": candidate["original_reported_run_id"],
        "target_case_id": "RTG-001",
        "approval_status": "approved_for_wrapped_ingestion_candidate",
        "preserved_mismatch": {
            "original_reported_run_id": candidate["original_reported_run_id"],
            "target_case_id": "RTG-001",
            "mismatch_hidden": False
        },
        "actual_cost_receipt": candidate["actual_cost_receipt"],
        "claim_boundary": {
            "crosswalk_approved": True,
            "wrapped_receipt_created": True,
            "artifact_returned": True,
            "actual_solver_cost_receipt_detected": True,
            "artifact_ingested_as_rtg_001": False,
            "rtg_state_updated_from_real_artifact": False,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False,
            "human_or_formal_review_required": True
        }
    }

    wrapped = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "wrapped_from_original_run_id": candidate["original_reported_run_id"],
        "receipt_type": "wrapped_real_artifact_receipt_for_rtg_001",
        "cost_receipt": candidate["actual_cost_receipt"],
        "claim_boundary": policy["claim_boundary_defaults"],
        "crosswalk": {
            "approved": True,
            "approval_file": str(OUT.relative_to(ROOT)),
            "original_run_id_preserved": True,
            "direct_ingestion_without_crosswalk_blocked": True
        },
        "ingestion_posture": "eligible_for_rtg_001_real_artifact_ingestion"
    }

    OUT.write_text(json.dumps(approval, indent=2) + "\n", encoding="utf-8")
    WRAPPED.write_text(json.dumps(wrapped, indent=2) + "\n", encoding="utf-8")
    print("RTG-001 crosswalk approval passed.")


if __name__ == "__main__":
    main()
