#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_json(path: Path) -> dict:
    require(path.exists(), f"Missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    contract = read_json(ROOT / "config" / "rtg_to_gcat_bcat_workflows_contract.json")
    require(contract["source_repo"] == "Data-Continuation/RTG-Tests", "Wrong source repo")
    require(contract["target_repo"] == "GCAT-BCAT-Engine/workflows", "Wrong target repo")
    require(contract["target_execution_layer"] == "math_solver/validation", "Wrong target execution layer")
    require(contract["workflow"] == ".github/workflows/validation_run.yml", "Wrong workflow")
    require(contract["trigger"] == "workflow_dispatch", "Wrong trigger")
    require(contract["runner"] == "ubuntu-latest", "Wrong runner")
    require(contract["required_secret"] == "ANTHROPIC_API_KEY", "Wrong secret")
    require(contract["dispatch_inputs"]["run_id"] == "RTG-001", "Wrong run id")
    require(contract["dispatch_inputs"]["budget_ceiling"] == "50.00", "Wrong budget ceiling")
    require({"ext2_phase1.json", "ext2_sources.json", "ext2_phase3.json", "ext2_report.json"}.issubset(set(contract["expected_artifacts"])), "Missing expected artifacts")

    boundary = contract["claim_boundary"]
    require(boundary["handoff_contract_ready"] is True, "Contract not ready")
    require(boundary["actual_dispatch_performed"] is False, "RTG contract must not claim dispatch")
    require(boundary["math_solver_executed"] is False, "RTG contract must not claim solver execution")
    require(boundary["artifacts_returned"] is False, "RTG contract must not claim artifacts returned")
    require(boundary["rtg_state_updated"] is False, "RTG contract must not claim state update")
    require(boundary["no_false_execution_claim"] is True, "False execution guard missing")
    print("RTG to GCAT-BCAT workflows connectivity contract test passed.")


if __name__ == "__main__":
    main()
