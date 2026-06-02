#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

VALID_STATUSES = [
    "not_dispatched",
    "dispatch_ready",
    "dispatch_sent",
    "solver_running",
    "solver_results_missing",
    "solver_results_available",
    "solver_failed",
]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def track(dispatch_packet_path: Path, output_path: Path, results_path: Path | None = None, dispatched: bool = False, failed: bool = False) -> Path:
    packet = json.loads(dispatch_packet_path.read_text(encoding="utf-8"))
    if failed:
        status = "solver_failed"
    elif results_path and results_path.exists():
        status = "solver_results_available"
    elif dispatched:
        status = "solver_results_missing"
    elif packet.get("dispatch_status") == "dispatch_ready":
        status = "dispatch_ready"
    else:
        status = "not_dispatched"

    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "status_surface": "rtg_math_solver_execution_status",
        "solver_run_id": packet.get("solver_run_id"),
        "execution_status": status,
        "valid_statuses": VALID_STATUSES,
        "result_completion_allowed": status == "solver_results_available",
        "expected_solver_result_path": packet.get("expected_solver_result_path"),
        "observed_solver_result_path": results_path.as_posix() if results_path else "",
        "summary": {
            "execution_status": status,
            "result_completion_allowed": status == "solver_results_available",
        },
        "receipt": {
            "dispatch_packet_sha256": sha256_file(dispatch_packet_path),
            "solver_result_sha256": sha256_file(results_path) if results_path and results_path.exists() else "",
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dispatch-packet", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--results", default="")
    p.add_argument("--dispatched", action="store_true")
    p.add_argument("--failed", action="store_true")
    a = p.parse_args()
    results = Path(a.results) if a.results else None
    print("Wrote RTG math-solver execution status: " + str(track(Path(a.dispatch_packet), Path(a.output), results, a.dispatched, a.failed)))

if __name__ == "__main__":
    main()
