#!/usr/bin/env python3
"""RTG math-solver adapter layer tests."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT_SCRIPT = ROOT / "scripts" / "export_rtg_solver_cases.py"
ADAPTER_SCRIPT = ROOT / "scripts" / "build_rtg_solver_run_manifest.py"
RUN_SCHEMA = ROOT / "schemas" / "rtg_solver_run_manifest.schema.json"
TMP_FIXTURES = ROOT / "build" / "adapter-test-fixtures"
CASE_OUTPUT = ROOT / "build" / "solver-cases-adapter-test"
RUN_OUTPUT = ROOT / "build" / "solver-runs-adapter-test"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True, check=False)

def write_sample_fixture() -> None:
    if TMP_FIXTURES.exists():
        shutil.rmtree(TMP_FIXTURES)
    TMP_FIXTURES.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "maturity": "provisional",
        "layer_type": "semantic differentiation",
        "test_key": "adapter_sample_semantic_behavior",
        "mechanism_group": "adapter",
        "title": "Adapter Sample Semantic Behavior",
        "valid_states": ["satisfiable_sample", "underconstrained_sample"],
        "cases": [
            {
                "case_id": "ADAPTER-SAMPLE-001",
                "semantic_signal": 1,
                "expected_state": "satisfiable_sample"
            }
        ]
    }
    (TMP_FIXTURES / "adapter-sample-semantic-behavior.valid.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

def main() -> None:
    require(EXPORT_SCRIPT.exists(), "solver case export script is missing")
    require(ADAPTER_SCRIPT.exists(), "solver run adapter script is missing")
    require(RUN_SCHEMA.exists(), "solver run manifest schema is missing")

    for path in [CASE_OUTPUT, RUN_OUTPUT]:
        if path.exists():
            shutil.rmtree(path)
    write_sample_fixture()

    export_result = run([
        sys.executable,
        str(EXPORT_SCRIPT),
        "--fixture-dir",
        str(TMP_FIXTURES),
        "--output-dir",
        str(CASE_OUTPUT),
    ])
    if export_result.returncode != 0:
        raise AssertionError(export_result.stdout + export_result.stderr)

    adapter_result = run([
        sys.executable,
        str(ADAPTER_SCRIPT),
        "--case-dir",
        str(CASE_OUTPUT),
        "--output-dir",
        str(RUN_OUTPUT),
    ])
    if adapter_result.returncode != 0:
        raise AssertionError(adapter_result.stdout + adapter_result.stderr)

    manifest_path = RUN_OUTPUT / "rtg_solver_run_manifest.json"
    require(manifest_path.exists(), "solver run manifest was not written")

    schema = json.loads(RUN_SCHEMA.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    missing = set(schema["required"]) - set(manifest)
    require(not missing, "solver run manifest missing required fields: " + repr(sorted(missing)))
    require(manifest["schema_version"] == "1.0", "schema_version mismatch")
    require(manifest["source_repo"] == "Data-Continuation/RTG-Tests", "source_repo mismatch")
    require(manifest["target_workflow_reference"] == "GCAT-BCAT-Engine/workflows/math-solver", "workflow reference mismatch")
    require(manifest["adapter_posture"] == "ready_for_workflow", "adapter_posture should be ready_for_workflow")
    require(isinstance(manifest["input_cases"], list) and len(manifest["input_cases"]) == 1, "input_cases must contain the sample case")
    require("solver_results_json" in manifest["expected_outputs"], "missing solver_results_json output contract")
    require("formal_posture_json" in manifest["expected_outputs"], "missing formal_posture_json output contract")

    first_case = manifest["input_cases"][0]
    require(first_case["case_id"] == "ADAPTER-SAMPLE-001", "input case_id mismatch")
    require(first_case["expected_solver_posture"] == "satisfiable", "input expected posture mismatch")

    print("RTG math solver adapter tests passed.")

if __name__ == "__main__":
    main()
