#!/usr/bin/env python3
from __future__ import annotations
import json
import shutil
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "build" / "math-solver-execution-status-test"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

def seed_inputs():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    manifest = TMP / "rtg_solver_run_manifest.json"
    results = TMP / "solver_results.json"
    write_json(manifest, {
        "schema_version": "1.0",
        "solver_run_id": "rtg-solver-run-001",
        "source_repo": "Data-Continuation/RTG-Tests",
        "solver_cases": [
            {"case_id": "RTG-SC-001", "case_type": "observer_window_phase_shift"},
            {"case_id": "RTG-SC-002", "case_type": "receipt_bound_posture"}
        ],
        "workflow_reference": "GCAT-BCAT-Engine/workflows/math-solver"
    })
    write_json(results, {
        "schema_version": "1.0",
        "solver_run_id": "rtg-solver-run-001",
        "results": [
            {"case_id": "RTG-SC-001", "solver_status": "satisfiable", "formal_posture": "formally_consistent"},
            {"case_id": "RTG-SC-002", "solver_status": "satisfiable", "formal_posture": "formally_consistent"}
        ]
    })
    return manifest, results

def main():
    manifest, results = seed_inputs()
    dispatch = TMP / "dispatch_packet.json"
    missing_status = TMP / "missing_status.json"
    available_status = TMP / "available_status.json"
    load("dispatch", ROOT / "scripts" / "build_rtg_math_solver_dispatch_packet.py").build_packet(manifest, dispatch)
    status_mod = load("status", ROOT / "scripts" / "track_rtg_math_solver_execution_status.py")
    status_mod.track(dispatch, missing_status, TMP / "not-yet-results.json", dispatched=True, failed=False)
    status_mod.track(dispatch, available_status, results, dispatched=True, failed=False)
    missing = json.loads(missing_status.read_text())
    available = json.loads(available_status.read_text())
    require(missing["execution_status"] == "solver_results_missing", "missing status mismatch")
    require(available["execution_status"] == "solver_results_available", "available status mismatch")
    require(available["result_completion_allowed"] is True, "completion should be allowed")
    print("RTG math-solver execution status tests passed.")
if __name__ == "__main__": main()
