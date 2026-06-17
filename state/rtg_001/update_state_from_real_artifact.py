#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
INGESTION = ROOT / "ingestion" / "rtg_001" / "rtg_001_real_artifact_ingestion_result.json"
OUT_STATUS = ROOT / "status" / "rtg_001_real_artifact_state_update.json"
OUT_RECEIPT = ROOT / "receipts" / "rtg_001" / "rtg_001_real_artifact_state_update_receipt.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ingestion = read_json(INGESTION)
    require(ingestion["case_id"] == "RTG-001", "Wrong case id")
    require(ingestion["ingestion_type"] == "real_artifact_ingestion_via_approved_crosswalk", "Wrong ingestion type")
    require(ingestion["ingestion_status"] == "complete", "Real artifact ingestion must be complete")
    require(ingestion["to_state"] == "artifact_ingested_as_rtg_001", "Input state must be artifact_ingested_as_rtg_001")
    require(ingestion["next_state"] == "rtg_real_artifact_state_update_ready", "Input must be ready for real artifact state update")
    require(ingestion["claim_boundary"]["artifact_ingested_as_rtg_001"] is True, "Real artifact ingestion boundary missing")
    require(ingestion["claim_boundary"]["rtg_state_updated_from_real_artifact"] is False, "Ingestion must not pre-claim state update")
    require(ingestion["claim_boundary"]["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(ingestion["preservation"]["original_run_id_preserved"] is True, "Original run id must be preserved")
    require(ingestion["preservation"]["cost_receipt_preserved"] is True, "Cost receipt must be preserved")
    require(ingestion["preservation"]["mismatch_hidden"] is False, "Mismatch must not be hidden")

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    status = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "state_update_type": "real_artifact_state_update",
        "source_ingestion": str(INGESTION.relative_to(ROOT)),
        "original_reported_run_id": ingestion["original_reported_run_id"],
        "target_case_id": ingestion["target_case_id"],
        "state_update_status": "recorded",
        "from_state": "artifact_ingested_as_rtg_001",
        "to_state": "rtg_state_updated_from_real_artifact",
        "next_state": "real_artifact_review_candidate_refresh_ready",
        "actual_cost_receipt": ingestion["actual_cost_receipt"],
        "claim_boundary": {
            "artifact_returned": True,
            "crosswalk_approved": True,
            "artifact_ingested_as_rtg_001": True,
            "rtg_state_updated_from_real_artifact": True,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False,
            "human_or_formal_review_required": True
        },
        "preservation": ingestion["preservation"]
    }

    receipt = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "receipt_type": "rtg_real_artifact_state_update_receipt",
        "input": str(INGESTION.relative_to(ROOT)),
        "output_status": str(OUT_STATUS.relative_to(ROOT)),
        "state_transition": {
            "from": "artifact_ingested_as_rtg_001",
            "to": "rtg_state_updated_from_real_artifact"
        },
        "original_reported_run_id_preserved": True,
        "cost_receipt_preserved": True,
        "claim_boundary_preserved": True,
        "final_claims_blocked": True
    }

    OUT_STATUS.parent.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    OUT_STATUS.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    OUT_RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("RTG-001 real artifact state update passed.")


if __name__ == "__main__":
    main()
