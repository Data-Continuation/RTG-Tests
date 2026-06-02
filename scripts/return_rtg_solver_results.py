#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def return_results(status_path: Path, solver_results_path: Path, output_path: Path) -> Path:
    status = json.loads(status_path.read_text(encoding="utf-8"))
    if not solver_results_path.exists():
        raise FileNotFoundError("solver_results.json does not exist: " + str(solver_results_path))
    results = json.loads(solver_results_path.read_text(encoding="utf-8"))
    available = status.get("execution_status") == "solver_results_available"

    returned = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "return_surface": "rtg_solver_result_return",
        "solver_run_id": status.get("solver_run_id", results.get("solver_run_id", "unknown")),
        "return_status": "return_ready_for_ingestion" if available else "return_blocked_by_status",
        "solver_results_path": solver_results_path.as_posix(),
        "solver_results_sha256": sha256_file(solver_results_path),
        "result_count": len(results.get("results", [])),
        "ingestion_target": "scripts/ingest_rtg_solver_results.py",
        "expected_posture_output": "build/formal-postures/rtg_formal_posture.json",
        "summary": {
            "result_count": len(results.get("results", [])),
            "return_posture": "return_ready_for_ingestion" if available else "return_blocked_by_status",
        },
        "receipt": {
            "execution_status_sha256": sha256_file(status_path),
            "solver_results_sha256": sha256_file(solver_results_path),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(returned, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--status", required=True)
    p.add_argument("--solver-results", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG solver result return: " + str(return_results(Path(a.status), Path(a.solver_results), Path(a.output))))

if __name__ == "__main__":
    main()
