#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path

def return_results(execution_receipt_path: Path, solver_results_path: Path, output_path: Path) -> Path:
    execution_receipt = json.loads(execution_receipt_path.read_text(encoding="utf-8"))
    results_present = solver_results_path.exists()
    results = json.loads(solver_results_path.read_text(encoding="utf-8")) if results_present else {"results": []}
    if not results_present:
        return_status = "blocked_solver_results_missing"
    elif execution_receipt.get("execution_status") in {"solver_dispatched_waiting_for_results", "authority_bound_dispatch_ready_not_executed"}:
        return_status = "authority_bound_results_ready_for_ingestion"
    else:
        return_status = "blocked_execution_receipt_not_valid_for_return"
    record = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "return_surface": "rtg_authority_bound_solver_result_return",
        "return_status": return_status,
        "solver_results_present": results_present,
        "solver_result_count": len(results.get("results", [])),
        "ingestion_target": "scripts/ingest_rtg_solver_results.py",
        "summary": {
            "return_status": return_status,
            "solver_result_count": len(results.get("results", [])),
        },
        "receipt": {
            "execution_receipt_sha256": sha256_file(execution_receipt_path),
            "solver_results_sha256": sha256_file(solver_results_path) if results_present else "",
        },
    }
    return write_json(output_path, record)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--execution-receipt", required=True)
    p.add_argument("--solver-results", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG authority-bound solver result return: " + str(return_results(Path(a.execution_receipt), Path(a.solver_results), Path(a.output))))

if __name__ == "__main__":
    main()
