#!/usr/bin/env python3
from __future__ import annotations
import json
import shutil
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "build" / "actual-math-solver-dispatch-test"

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
    manifest, _ = seed_inputs()
    out = TMP / "dispatch_packet.json"
    mod = load("dispatch", ROOT / "scripts" / "build_rtg_math_solver_dispatch_packet.py")
    mod.build_packet(manifest, out)
    payload = json.loads(out.read_text())
    require(payload["target_workflow_reference"] == "GCAT-BCAT-Engine/workflows/math-solver", "workflow reference mismatch")
    require(payload["dispatch_status"] == "dispatch_ready", "dispatch status mismatch")
    require(payload["case_count"] == 2, "case count mismatch")
    require(payload["completion_rule"] == "do_not_mark_complete_until_solver_results_json_exists", "completion rule mismatch")
    print("RTG actual math-solver dispatch tests passed.")
if __name__ == "__main__": main()
