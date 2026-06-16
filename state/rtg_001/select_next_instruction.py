#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
STATE_UPDATE = ROOT / "status" / "rtg_001_state_update.json"
OUT = ROOT / "instructions" / "rtg_001" / "rtg_001_next_instruction.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    state = read_json(STATE_UPDATE)
    require(state["case_id"] == "RTG-001", "Wrong case id")
    require(state["state_update_status"] == "recorded", "State update must be recorded")
    require(state["to_state"] == "rtg_state_update_recorded", "Wrong input state")
    require(state["claim_boundary"]["rtg_state_update_recorded"] is True, "State update boundary missing")
    require(state["claim_boundary"]["final_correctness_claimed"] is False, "Final correctness must remain blocked")
    require(state["claim_boundary"]["autonomous_theorem_proving_claimed"] is False, "Autonomous theorem proving must remain blocked")

    # Deterministic routing rule for RTG-001 fixture/first-pass evidence.
    # Real returned artifacts can later add confidence/status fields and route differently.
    instruction = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "case_id": "RTG-001",
        "input_state": "rtg_state_update_recorded",
        "selected_next_instruction": "route_to_review",
        "allowed_routes": [
            "route_to_review",
            "route_to_replay",
            "route_to_quarantine",
            "route_to_solver_iteration"
        ],
        "selection_reason": "RTG-001 evidence preserves claim boundary and cost receipt but still requires human or formal review before final correctness claims.",
        "review_requirements": [
            "verify returned artifacts are real, not fixtures",
            "review solver analysis for boundary preservation",
            "confirm no final theorem-proof claim is made",
            "decide whether next iteration, replay, or publication note is admissible"
        ],
        "claim_boundary": {
            "next_instruction_selected": True,
            "artifact_ingested": True,
            "rtg_state_update_recorded": True,
            "route_to_review": True,
            "route_to_replay": False,
            "route_to_quarantine": False,
            "route_to_solver_iteration": False,
            "autonomous_theorem_proving_claimed": False,
            "final_correctness_claimed": False,
            "human_or_formal_review_required": True
        }
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(instruction, indent=2) + "\n", encoding="utf-8")
    print("RTG-001 next instruction selection passed.")


if __name__ == "__main__":
    main()
