#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "evidence" / "rtg_001" / "real_evidence_manifest.json"
OUT = ROOT / "evidence" / "rtg_001" / "normalized_ingestion_candidate.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    manifest = read_json(MANIFEST)
    summary = manifest["ext2_report_summary"]
    boundary = manifest["rtg_boundary_assessment"]

    require(manifest["case_id"] == "RTG-001", "Wrong case id")
    require(boundary["real_artifact_returned"] is True, "Real artifact must be returned")
    require(boundary["actual_cost_receipt_available"] is True, "Actual cost receipt must be available")
    require(boundary["artifact_run_id_matches_rtg_case_id"] is False, "This adapter is for mismatched returned run id")
    require(boundary["normalization_or_crosswalk_required"] is True, "Crosswalk requirement must be explicit")
    require(summary["total_cost_usd"] == 0.0219265, "Unexpected cost receipt")
    require(summary["sources_verified"] is True, "Sources must be verified")

    candidate = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "case_id": "RTG-001",
        "candidate_type": "normalized_returned_artifact_ingestion_candidate",
        "source_manifest": str(MANIFEST.relative_to(ROOT)),
        "original_reported_run_id": summary["reported_run_id"],
        "target_case_id": "RTG-001",
        "crosswalk_status": "required_and_recorded",
        "ingestion_posture": "candidate_not_direct_ingestion",
        "actual_cost_receipt": {
            "total_cost_usd": summary["total_cost_usd"],
            "total_tokens": summary["total_tokens"],
            "phase_1_cost_usd": summary["phase_1_cost_usd"],
            "phase_3_batch_cost_usd": summary["phase_3_batch_cost_usd"]
        },
        "required_before_rtg_state_update": [
            "explicitly approve EXT-002-FIXED to RTG-001 crosswalk",
            "inject or wrap missing claim_boundary field",
            "preserve original reported run id",
            "preserve cost receipt without overwriting original artifact",
            "record that final correctness remains unclaimed"
        ],
        "claim_boundary": {
            "artifact_returned": True,
            "actual_solver_cost_receipt_detected": True,
            "artifact_ingested_as_rtg_001": False,
            "rtg_state_updated_from_real_artifact": False,
            "crosswalk_required_before_ingestion": True,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False
        }
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    print("RTG-001 returned artifact normalization candidate passed.")


if __name__ == "__main__":
    main()
