#!/usr/bin/env python3
from __future__ import annotations
import json
import shutil
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "build" / "authority-bound-solver-result-return-test"

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

def sha256_file(path):
    import hashlib
    return hashlib.sha256(path.read_bytes()).hexdigest()

def seed_manifest():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    manifest = TMP / "rtg_solver_run_manifest.json"
    write_json(manifest, {
        "schema_version": "1.0",
        "solver_run_id": "rtg-tv-tvc-solver-run-test",
        "source_repo": "Data-Continuation/RTG-Tests",
        "solver_cases": [
            {"case_id": "RTG-SC-001", "case_type": "formal_architecture_readiness"}
        ],
        "workflow_reference": "GCAT-BCAT-Engine/workflows/math-solver"
    })
    return manifest

def seed_authority_receipt(request_path):
    request = json.loads(request_path.read_text())
    receipt = TMP / "tv_tvc_authority_receipt.json"
    write_json(receipt, {
        "schema_version": "1.0",
        "authority_surface": "tv_tvc_math_solver_dispatch_authority",
        "authority_status": "authority_granted",
        "authority_class": "math_solver_workflow_dispatch",
        "authorized_action": "authorize_math_solver_workflow_dispatch",
        "source_request_sha256": sha256_file(request_path),
        "credential_boundary": "tv_tvc_brokered",
        "target_workflow": request["target_workflow"],
        "issued_by": "StegVerse-Labs/TV+StegVerse-Labs/TVC"
    })
    return receipt

def main():
    manifest = seed_manifest()
    request = TMP / "authority_request.json"
    receipt = TMP / "tv_tvc_authority_receipt.json"
    validation = TMP / "authority_validation.json"
    dispatch = TMP / "authority_bound_dispatch.json"
    exec_receipt = TMP / "execution_receipt.json"
    results = TMP / "solver_results.json"
    out = TMP / "return.json"
    write_json(results, {
        "schema_version": "1.0",
        "solver_run_id": "rtg-tv-tvc-solver-run-test",
        "results": [{"case_id": "RTG-SC-001", "solver_status": "satisfiable", "formal_posture": "formally_consistent"}]
    })
    load("request", ROOT / "scripts" / "request_rtg_tv_tvc_math_solver_authority.py").build_authority_request(manifest, request)
    receipt = seed_authority_receipt(request)
    load("validation", ROOT / "scripts" / "validate_rtg_tv_tvc_authority_receipt.py").validate_authority_receipt(request, receipt, validation)
    load("dispatch", ROOT / "scripts" / "dispatch_rtg_authority_bound_math_solver.py").dispatch_authority_bound(request, validation, dispatch, execute=False, token="")
    load("exec_receipt", ROOT / "scripts" / "receipt_rtg_authority_bound_solver_execution.py").build_execution_receipt(dispatch, exec_receipt)
    load("return_mod", ROOT / "scripts" / "return_rtg_authority_bound_solver_results.py").return_results(exec_receipt, results, out)
    payload = json.loads(out.read_text())
    require(payload["return_status"] == "authority_bound_results_ready_for_ingestion", "return status mismatch")
    require(payload["solver_result_count"] == 1, "result count mismatch")
    require(payload["ingestion_target"] == "scripts/ingest_rtg_solver_results.py", "ingestion target mismatch")
    print("RTG authority-bound solver result return tests passed.")
if __name__ == "__main__": main()
