#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_RESULT_FIELDS = ["case_id", "solver_status", "formal_posture"]

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path

def validate_artifact_contract(materialized_request_path: Path, solver_results_path: Path, output_path: Path) -> Path:
    request = json.loads(materialized_request_path.read_text(encoding="utf-8"))
    results = json.loads(solver_results_path.read_text(encoding="utf-8"))
    expected_case_ids = set(request.get("case_ids", []))
    observed_results = results.get("results", [])
    observed_case_ids = {item.get("case_id") for item in observed_results}
    failures = []
    if results.get("solver_run_id") != request.get("solver_run_id"):
        failures.append({"failure_type": "solver_run_id_mismatch"})
    missing_cases = sorted(expected_case_ids - observed_case_ids)
    extra_cases = sorted(observed_case_ids - expected_case_ids)
    if missing_cases:
        failures.append({"failure_type": "missing_case_results", "details": missing_cases})
    if extra_cases:
        failures.append({"failure_type": "unexpected_case_results", "details": extra_cases})
    for item in observed_results:
        missing_fields = [field for field in REQUIRED_RESULT_FIELDS if field not in item]
        if missing_fields:
            failures.append({"failure_type": "missing_result_fields", "case_id": item.get("case_id"), "details": missing_fields})
    contract = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "contract_surface": "rtg_math_solver_returned_artifact_contract",
        "artifact_contract_valid": not failures,
        "failures": failures,
        "expected_case_count": len(expected_case_ids),
        "observed_result_count": len(observed_results),
        "summary": {
            "failure_count": len(failures),
            "contract_posture": "returned_artifact_contract_valid" if not failures else "returned_artifact_contract_review",
        },
        "receipt": {
            "materialized_request_sha256": sha256_file(materialized_request_path),
            "solver_results_sha256": sha256_file(solver_results_path),
        },
    }
    return write_json(output_path, contract)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--materialized-request", required=True)
    p.add_argument("--solver-results", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG math-solver returned artifact contract: " + str(validate_artifact_contract(Path(a.materialized_request), Path(a.solver_results), Path(a.output))))

if __name__ == "__main__":
    main()
