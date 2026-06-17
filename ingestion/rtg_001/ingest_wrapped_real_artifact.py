#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
APPROVAL = ROOT / "evidence" / "rtg_001" / "crosswalk_approval.json"
WRAPPED = ROOT / "evidence" / "rtg_001" / "rtg_001_wrapped_real_artifact_receipt.json"
OUT = ROOT / "ingestion" / "rtg_001" / "rtg_001_real_artifact_ingestion_result.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    approval = read_json(APPROVAL)
    wrapped = read_json(WRAPPED)

    require(approval["case_id"] == "RTG-001", "Wrong approval case id")
    require(approval["approval_status"] == "approved_for_wrapped_ingestion_candidate", "Crosswalk not approved")
    require(approval["claim_boundary"]["crosswalk_approved"] is True, "Crosswalk approval boundary missing")
    require(approval["claim_boundary"]["artifact_ingested_as_rtg_001"] is False, "Approval cannot pre-claim ingestion")
    require(wrapped["case_id"] == "RTG-001", "Wrong wrapped case id")
    require(wrapped["wrapped_from_original_run_id"] == "EXT-002-FIXED", "Original run id must be preserved")
    require(wrapped["crosswalk"]["approved"] is True, "Wrapped receipt crosswalk not approved")
    require(wrapped["ingestion_posture"] == "eligible_for_rtg_001_real_artifact_ingestion", "Wrapped receipt not eligible")
    require(wrapped["claim_boundary"]["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(wrapped["claim_boundary"]["autonomous_theorem_proving_claimed"] is False, "Autonomous proof must remain blocked")

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "ingestion_type": "real_artifact_ingestion_via_approved_crosswalk",
        "source_approval": str(APPROVAL.relative_to(ROOT)),
        "source_wrapped_receipt": str(WRAPPED.relative_to(ROOT)),
        "original_reported_run_id": wrapped["wrapped_from_original_run_id"],
        "target_case_id": "RTG-001",
        "ingestion_status": "complete",
        "from_state": "crosswalk_approved_for_rtg_001_ingestion",
        "to_state": "artifact_ingested_as_rtg_001",
        "next_state": "rtg_real_artifact_state_update_ready",
        "actual_cost_receipt": wrapped["cost_receipt"],
        "claim_boundary": {
            "artifact_returned": True,
            "crosswalk_approved": True,
            "artifact_ingested_as_rtg_001": True,
            "rtg_state_updated_from_real_artifact": False,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False,
            "human_or_formal_review_required": True
        },
        "preservation": {
            "original_run_id_preserved": True,
            "cost_receipt_preserved": True,
            "mismatch_hidden": False,
            "direct_ingestion_without_crosswalk_blocked": True
        }
    }

    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("RTG-001 wrapped real artifact ingestion passed.")


if __name__ == "__main__":
    main()
