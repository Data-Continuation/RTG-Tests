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

def build_execution_receipt(dispatch_path: Path, output_path: Path) -> Path:
    dispatch = json.loads(dispatch_path.read_text(encoding="utf-8"))
    status = dispatch.get("dispatch_status")
    if status == "dispatch_accepted":
        execution_status = "solver_dispatched_waiting_for_results"
    elif status == "dispatch_ready_authority_bound":
        execution_status = "authority_bound_dispatch_ready_not_executed"
    elif status.startswith("blocked"):
        execution_status = "authority_bound_dispatch_blocked"
    else:
        execution_status = "authority_bound_dispatch_review"
    record = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "receipt_surface": "rtg_authority_bound_solver_execution_receipt",
        "execution_status": execution_status,
        "dispatch_status": status,
        "target_workflow": dispatch.get("target_workflow", {}),
        "completion_rule": dispatch.get("completion_rule", "do_not_mark_complete_until_solver_results_json_exists"),
        "summary": {
            "execution_status": execution_status,
            "solver_results_required": True,
        },
        "receipt": {
            "authority_bound_dispatch_sha256": sha256_file(dispatch_path),
        },
    }
    return write_json(output_path, record)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dispatch", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG authority-bound solver execution receipt: " + str(build_execution_receipt(Path(a.dispatch), Path(a.output))))

if __name__ == "__main__":
    main()
