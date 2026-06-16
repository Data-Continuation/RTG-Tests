#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "review" / "rtg_001" / "rtg_001_review_packet.json"
OUT_JSON = ROOT / "candidates" / "rtg_001" / "rtg_001_final_review_candidate.json"
OUT_MD = ROOT / "candidates" / "rtg_001" / "RTG_001_FINAL_REVIEW_CANDIDATE.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    packet = read_json(PACKET)
    require(packet["case_id"] == "RTG-001", "Wrong case id")
    require(packet["packet_type"] == "final_review_candidate_packet", "Wrong packet type")
    require(packet["review_route"] == "route_to_review", "Review route required")
    require(packet["claim_boundary"]["final_review_candidate_ready"] is True, "Review packet not candidate-ready")
    require(packet["claim_boundary"]["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(packet["claim_boundary"]["autonomous_theorem_proving_claimed"] is False, "Autonomous proof must remain blocked")

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    candidate = {
        "schema_version": "1.0",
        "generated": generated,
        "case_id": "RTG-001",
        "candidate_type": "final_review_candidate",
        "source_packet": str(PACKET.relative_to(ROOT)),
        "candidate_status": "ready_for_human_or_formal_review_pending_real_artifact_receipt",
        "review_route": "route_to_review",
        "decision_options": [
            "approve_as_boundary_valid_scaffold",
            "request_real_artifact_ingestion",
            "route_to_replay",
            "route_to_quarantine",
            "route_to_solver_iteration",
            "reject_claim_as_premature"
        ],
        "cost_posture": packet["cost_summary"],
        "required_evidence_before_final_claim": [
            "external-full-results artifact exists",
            "real ext2_report.json parsed",
            "actual solver cost receipt recorded",
            "claim boundary preserved after real artifact ingestion",
            "human or formal review completed"
        ],
        "claim_boundary": {
            "final_review_candidate_created": True,
            "ready_for_review": True,
            "artifact_returned": False,
            "artifact_ingested_from_real_artifact": False,
            "rtg_state_updated_from_real_artifact": False,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False,
            "human_or_formal_review_required": True
        }
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")

    md = f"""# RTG-001 Final Review Candidate

Generated: `{generated}`

## Candidate Status

```text
{candidate['candidate_status']}
```

## Review Route

```text
{candidate['review_route']}
```

## Decision Options

"""
    for option in candidate["decision_options"]:
        md += f"- `{option}`\n"
    md += """
## Required Evidence Before Final Claim

"""
    for item in candidate["required_evidence_before_final_claim"]:
        md += f"- {item}\n"
    md += """
## Claim Boundary

```text
final_review_candidate_created: true
ready_for_review: true
artifact_returned: false
artifact_ingested_from_real_artifact: false
rtg_state_updated_from_real_artifact: false
autonomous_theorem_proving_claimed: false
final_correctness_claimed: false
human_or_formal_review_required: true
```
"""
    OUT_MD.write_text(md, encoding="utf-8")
    print("RTG-001 final review candidate generation passed.")


if __name__ == "__main__":
    main()
