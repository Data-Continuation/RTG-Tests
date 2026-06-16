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
        [sys.executable, "ingestion/rtg_001/ingest_returned_artifacts.py"],
        [sys.executable, "state/rtg_001/update_state_from_ingestion.py"],
        [sys.executable, "state/rtg_001/select_next_instruction.py"],
    ]:
        proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
        require(proc.returncode == 0, f"Command failed {command}: {proc.stdout}\n{proc.stderr}")

    instruction = read_json(ROOT / "instructions" / "rtg_001" / "rtg_001_next_instruction.json")
    require(instruction["case_id"] == "RTG-001", "Wrong case id")
    require(instruction["input_state"] == "rtg_state_update_recorded", "Wrong input state")
    require(instruction["selected_next_instruction"] == "route_to_review", "Expected route_to_review")
    require("route_to_review" in instruction["allowed_routes"], "route_to_review missing")
    require("route_to_replay" in instruction["allowed_routes"], "route_to_replay missing")
    require("route_to_quarantine" in instruction["allowed_routes"], "route_to_quarantine missing")
    require("route_to_solver_iteration" in instruction["allowed_routes"], "route_to_solver_iteration missing")

    boundary = instruction["claim_boundary"]
    require(boundary["next_instruction_selected"] is True, "Next instruction not selected")
    require(boundary["route_to_review"] is True, "Review route not selected")
    require(boundary["autonomous_theorem_proving_claimed"] is False, "False autonomous theorem proving claim not blocked")
    require(boundary["final_correctness_claimed"] is False, "False final correctness claim not blocked")
    require(boundary["human_or_formal_review_required"] is True, "Review requirement missing")

    print("RTG-001 next instruction selection test passed.")


if __name__ == "__main__":
    main()
