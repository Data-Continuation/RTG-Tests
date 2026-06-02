#!/usr/bin/env python3
from __future__ import annotations
import json
import shutil
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "build" / "math-solver-returned-artifact-contract-test"

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

def seed_authority_request():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    request = TMP / "authority_request.json"
    write_json(request, {
        "schema_version": "1.0",
        "source_repo": "Data-Continuation/RTG-Tests",
        "authority_surface": "rtg_tv_tvc_authority_request",
        "target_workflow": {
            "owner": "GCAT-BCAT-Engine",
            "repo": "workflows",
            "workflow": "math-solver.yml",
            "ref": "main"
        },
        "solver_run_id": "rtg-real-solver-run-test",
        "manifest_path": "build/solver-runs/rtg_solver_run_manifest.json",
        "case_ids": ["RTG-SC-001", "RTG-SC-002"],
        "case_count": 2
    })
    return request

def seed_solver_results():
    results = TMP / "solver_results.json"
    write_json(results, {
        "schema_version": "1.0",
        "solver_run_id": "rtg-real-solver-run-test",
        "results": [
            {"case_id": "RTG-SC-001", "solver_status": "satisfiable", "formal_posture": "formally_consistent"},
            {"case_id": "RTG-SC-002", "solver_status": "satisfiable", "formal_posture": "formally_consistent"}
        ]
    })
    return results

def main():
    request = seed_authority_request()
    results = seed_solver_results()
    broker = TMP / "broker_receipt.json"
    materialized = TMP / "materialized_request.json"
    out = TMP / "artifact_contract.json"
    load("broker", ROOT / "scripts" / "fixture_rtg_tv_tvc_broker_receipt.py").build_broker_receipt_fixture(request, broker)
    load("materialize", ROOT / "scripts" / "materialize_rtg_real_solver_run_request.py").materialize(request, broker, materialized)
    load("contract", ROOT / "scripts" / "validate_rtg_math_solver_returned_artifact_contract.py").validate_artifact_contract(materialized, results, out)
    payload = json.loads(out.read_text())
    require(payload["artifact_contract_valid"] is True, "artifact contract should be valid")
    require(payload["summary"]["contract_posture"] == "returned_artifact_contract_valid", "contract posture mismatch")
    print("RTG math-solver returned artifact contract tests passed.")
if __name__ == "__main__": main()
