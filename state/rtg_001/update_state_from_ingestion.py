#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
INGESTION_RESULT = ROOT / "ingestion" / "rtg_001" / "rtg_001_ingestion_result.json"
STATUS_OUT = ROOT / "status" / "rtg_001_state_update.json"
RECEIPT_OUT = ROOT / "receipts" / "rtg_001" / "rtg_001_state_update_receipt.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    ingestion = read_json(INGESTION_RESULT)
    require(ingestion["run_id"] == "RTG-001", "Wrong run id")
    require(ingestion["ingestion_status"] == "complete", "Ingestion must be complete")
    require(ingestion["to_state"] == "artifact_ingested", "Input state must be artifact_ingested")
    require(ingestion["next_state"] == "rtg_state_update_ready", "Ingestion must prepare state update")
    require(ingestion["claim_boundary_preserved"] is True, "Claim boundary must be preserved")
    require(ingestion["sources_verified"] is True, "Sources must be verified")
    require(ingestion["false_claims_blocked"]["autonomous_theorem_proving_claimed"] is False, "False autonomous proof claim must be blocked")
    require(ingestion["false_claims_blocked"]["final_correctness_claimed"] is False, "False final correctness claim must be blocked")

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    status = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "source_repo": "Data-Continuation/RTG-Tests",
        "execution_repo": ingestion["execution_repo"],
        "state_update_status": "recorded",
        "from_state": "artifact_ingested",
        "to_state": "rtg_state_update_recorded",
        "next_state": "review_or_next_instruction_selection",
        "cost_receipt": ingestion["cost_receipt"],
        "artifacts_ingested": ingestion["artifacts_ingested"],
        "claim_boundary": {
            "artifact_ingested": True,
            "rtg_state_update_recorded": True,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False,
            "human_or_formal_review_required": True
        }
    }

    receipt = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "receipt_type": "rtg_state_update_from_ingestion",
        "input": str(INGESTION_RESULT.relative_to(ROOT)),
        "output_status": str(STATUS_OUT.relative_to(ROOT)),
        "state_transition": {
            "from": "artifact_ingested",
            "to": "rtg_state_update_recorded"
        },
        "claim_boundary_preserved": True,
        "cost_receipt_preserved": True
    }

    STATUS_OUT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT_OUT.parent.mkdir(parents=True, exist_ok=True)
    STATUS_OUT.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    RECEIPT_OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print("RTG-001 state update from ingestion passed.")


if __name__ == "__main__":
    main()
