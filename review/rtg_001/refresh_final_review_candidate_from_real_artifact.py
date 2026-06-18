#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
REAL_STATE = ROOT / "status" / "rtg_001_real_artifact_state_update.json"
OUT_JSON = ROOT / "candidates" / "rtg_001" / "rtg_001_real_artifact_final_review_candidate.json"
OUT_MD = ROOT / "candidates" / "rtg_001" / "RTG_001_REAL_ARTIFACT_FINAL_REVIEW_CANDIDATE.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    state = read_json(REAL_STATE)
    require(state["case_id"] == "RTG-001", "Wrong case id")
    require(state["state_update_type"] == "real_artifact_state_update", "Wrong state update type")
    require(state["state_update_status"] == "recorded", "Real artifact state update not recorded")
    require(state["to_state"] == "rtg_state_updated_from_real_artifact", "Real artifact state not updated")
    require(state["claim_boundary"]["rtg_state_updated_from_real_artifact"] is True, "Real artifact state boundary missing")
    require(state["claim_boundary"]["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(state["claim_boundary"]["autonomous_theorem_proving_claimed"] is False, "Autonomous proof must remain blocked")
    require(state["actual_cost_receipt"]["total_cost_usd"] == 0.0219265, "Cost receipt mismatch")

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    candidate = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "candidate_type": "real_artifact_final_review_candidate",
        "source_state_update": str(REAL_STATE.relative_to(ROOT)),
        "candidate_status": "ready_for_human_or_formal_review_with_real_artifact_evidence",
        "review_route": "route_to_review",
        "original_reported_run_id": state["original_reported_run_id"],
        "target_case_id": state["target_case_id"],
        "actual_cost_receipt": state["actual_cost_receipt"],
        "decision_options": [
            "approve_boundary_and_cost_receipt",
            "request_additional_solver_iteration",
            "route_to_replay",
            "route_to_quarantine",
            "reject_final_correctness_claim_as_premature",
            "prepare_public_evidence_summary"
        ],
        "required_review_questions": [
            "Does the real artifact state update preserve original EXT-002-FIXED evidence?",
            "Is the RTG-001 crosswalk acceptable for this review candidate?",
            "Does the actual cost receipt remain within the RTG-001 budget ceiling?",
            "Are final correctness and autonomous proof claims still blocked?",
            "Should RTG-001 proceed to public evidence summary, replay, quarantine, or solver iteration?"
        ],
        "claim_boundary": {
            "real_artifact_final_review_candidate_created": True,
            "artifact_returned": True,
            "crosswalk_approved": True,
            "artifact_ingested_as_rtg_001": True,
            "rtg_state_updated_from_real_artifact": True,
            "ready_for_human_or_formal_review": True,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False,
            "human_or_formal_review_required": True
        }
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")

    md = f"""# RTG-001 Real Artifact Final Review Candidate

Generated: `{generated}`

## Candidate Status

```text
{candidate['candidate_status']}
```

## Evidence Source

```text
{candidate['source_state_update']}
```

## Cost Receipt

```text
total_cost_usd: {candidate['actual_cost_receipt']['total_cost_usd']}
total_tokens: {candidate['actual_cost_receipt']['total_tokens']}
```

## Claim Boundary

```text
artifact_returned: true
crosswalk_approved: true
artifact_ingested_as_rtg_001: true
rtg_state_updated_from_real_artifact: true
autonomous_theorem_proving_claimed: false
final_correctness_claimed: false
human_or_formal_review_required: true
```
"""
    OUT_MD.write_text(md, encoding="utf-8")
    print("RTG-001 real artifact final review candidate refresh passed.")


if __name__ == "__main__":
    main()
