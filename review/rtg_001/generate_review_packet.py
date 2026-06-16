#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
INSTRUCTION = ROOT / "instructions" / "rtg_001" / "rtg_001_next_instruction.json"
COST_LEDGER = ROOT / "costs" / "rtg_001" / "lifecycle_cost_ledger.json"
OUT_JSON = ROOT / "review" / "rtg_001" / "rtg_001_review_packet.json"
OUT_MD = ROOT / "review" / "rtg_001" / "RTG_001_REVIEW_PACKET.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    instruction = read_json(INSTRUCTION)
    ledger = read_json(COST_LEDGER)

    require(instruction["case_id"] == "RTG-001", "Wrong instruction case id")
    require(instruction["selected_next_instruction"] == "route_to_review", "Review packet requires route_to_review")
    require(instruction["claim_boundary"]["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(ledger["cost_rules"]["actual_solver_cost_must_come_from_returned_artifact"] is True, "Cost rule missing")

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    packet = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "packet_type": "final_review_candidate_packet",
        "input_instruction": str(INSTRUCTION.relative_to(ROOT)),
        "cost_ledger": str(COST_LEDGER.relative_to(ROOT)),
        "review_route": "route_to_review",
        "review_status": "candidate_ready_pending_real_artifact_receipt",
        "cost_summary": {
            "actual_previous_stage_paid_api_cost_usd": ledger["actual_costs_previous_stage"]["repo_build_and_documentation_commits"],
            "solver_actual_cost_receipt": ledger["actual_costs_previous_stage"]["anthropic_api_cost_recorded_in_artifacts"],
            "expected_solver_receipt_range_usd": ledger["estimated_upcoming_stage_costs"]["expected_solver_artifact_receipt_cost_range_usd"],
            "budget_ceiling_usd": ledger["budget"]["rtg_001_budget_ceiling_usd"],
            "cost_posture": "actual_solver_cost_pending_returned_artifact"
        },
        "required_review_questions": [
            "Are the artifacts real returned workflow artifacts rather than fixtures?",
            "Does ext2_report.json preserve task identity and output type?",
            "Does the cost receipt remain within the RTG-001 budget ceiling?",
            "Does the solver analysis preserve the claim boundary?",
            "Should the next admissible route remain review, or shift to replay, quarantine, or solver iteration?"
        ],
        "claim_boundary": {
            "review_packet_generated": True,
            "final_review_candidate_ready": True,
            "artifact_returned": False,
            "artifact_ingested_from_real_artifact": False,
            "rtg_state_updated_from_real_artifact": False,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False,
            "human_or_formal_review_required": True
        }
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")

    md = f"""# RTG-001 Final Review Candidate Packet

Generated: `{generated}`

## Review Status

```text
{packet['review_status']}
```

## Cost Summary

```text
actual_previous_stage_paid_api_cost_usd: {packet['cost_summary']['actual_previous_stage_paid_api_cost_usd']}
solver_actual_cost_receipt: {packet['cost_summary']['solver_actual_cost_receipt']}
expected_solver_receipt_range_usd: {packet['cost_summary']['expected_solver_receipt_range_usd']}
budget_ceiling_usd: {packet['cost_summary']['budget_ceiling_usd']}
cost_posture: {packet['cost_summary']['cost_posture']}
```

## Required Review Questions

"""
    for q in packet["required_review_questions"]:
        md += f"- {q}\n"
    md += """
## Claim Boundary

```text
review_packet_generated: true
final_review_candidate_ready: true
artifact_returned: false
artifact_ingested_from_real_artifact: false
rtg_state_updated_from_real_artifact: false
autonomous_theorem_proving_claimed: false
final_correctness_claimed: false
human_or_formal_review_required: true
```
"""
    OUT_MD.write_text(md, encoding="utf-8")
    print("RTG-001 review packet generation passed.")


if __name__ == "__main__":
    main()
