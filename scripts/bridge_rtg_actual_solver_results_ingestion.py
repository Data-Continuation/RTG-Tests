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

def bridge(contract_path: Path, solver_results_path: Path, output_path: Path) -> Path:
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    results = json.loads(solver_results_path.read_text(encoding="utf-8"))
    if not contract.get("artifact_contract_valid"):
        bridge_status = "blocked_returned_artifact_contract_invalid"
        bridged_results = []
    else:
        bridge_status = "solver_results_ready_for_rtg_ingestion"
        bridged_results = [
            {
                "case_id": item.get("case_id"),
                "solver_status": item.get("solver_status"),
                "formal_posture": item.get("formal_posture"),
                "ingestion_status": "ready",
            }
            for item in results.get("results", [])
        ]
    record = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "bridge_surface": "rtg_actual_solver_results_ingestion_bridge",
        "bridge_status": bridge_status,
        "solver_run_id": results.get("solver_run_id"),
        "bridged_results": bridged_results,
        "ingestion_target": "scripts/ingest_rtg_solver_results.py",
        "summary": {
            "bridged_result_count": len(bridged_results),
            "bridge_status": bridge_status,
        },
        "receipt": {
            "artifact_contract_sha256": sha256_file(contract_path),
            "solver_results_sha256": sha256_file(solver_results_path),
        },
    }
    return write_json(output_path, record)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--contract", required=True)
    p.add_argument("--solver-results", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG actual solver-results ingestion bridge: " + str(bridge(Path(a.contract), Path(a.solver_results), Path(a.output))))

if __name__ == "__main__":
    main()
