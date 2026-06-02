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

def materialize(authority_request_path: Path, broker_receipt_path: Path, output_path: Path) -> Path:
    request = json.loads(authority_request_path.read_text(encoding="utf-8"))
    receipt = json.loads(broker_receipt_path.read_text(encoding="utf-8"))
    if receipt.get("authority_status") != "authority_granted":
        raise SystemExit("Cannot materialize solver-run request without granted TV/TVC authority.")
    materialized = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "materialization_surface": "rtg_real_solver_run_request_materialization",
        "solver_run_id": request.get("solver_run_id"),
        "target_workflow": request.get("target_workflow", {}),
        "dispatch_inputs": {
            "source_repo": "Data-Continuation/RTG-Tests",
            "solver_run_id": request.get("solver_run_id"),
            "solver_manifest_path": request.get("manifest_path"),
            "expected_result_path": "build/solver-results/solver_results.json",
            "case_ids": ",".join(request.get("case_ids", [])),
            "authority_receipt_id": receipt.get("broker_receipt_id"),
            "authority_boundary": "tv_tvc_brokered",
        },
        "case_ids": request.get("case_ids", []),
        "case_count": request.get("case_count", len(request.get("case_ids", []))),
        "request_status": "materialized_for_solver_dispatch",
        "receipt": {
            "authority_request_sha256": sha256_file(authority_request_path),
            "broker_receipt_sha256": sha256_file(broker_receipt_path),
        },
    }
    return write_json(output_path, materialized)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--authority-request", required=True)
    p.add_argument("--broker-receipt", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG real solver-run request materialization: " + str(materialize(Path(a.authority_request), Path(a.broker_receipt), Path(a.output))))

if __name__ == "__main__":
    main()
