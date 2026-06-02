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

def build_broker_receipt_fixture(authority_request_path: Path, output_path: Path) -> Path:
    request = json.loads(authority_request_path.read_text(encoding="utf-8"))
    receipt = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "fixture_surface": "rtg_tv_tvc_broker_receipt_fixture",
        "broker_receipt_id": "RTG-TV-TVC-BROKER-001",
        "authority_status": "authority_granted",
        "authority_class": "math_solver_workflow_dispatch",
        "authorized_action": "authorize_math_solver_workflow_dispatch",
        "credential_boundary": "tv_tvc_brokered",
        "issued_by": "StegVerse-Labs/TV+StegVerse-Labs/TVC",
        "source_request_sha256": sha256_file(authority_request_path),
        "target_workflow": request.get("target_workflow", {}),
        "solver_run_id": request.get("solver_run_id", "unknown"),
        "case_ids": request.get("case_ids", []),
        "receipt_posture": "fixture_authority_granted",
    }
    return write_json(output_path, receipt)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--authority-request", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG TV/TVC broker receipt fixture: " + str(build_broker_receipt_fixture(Path(a.authority_request), Path(a.output))))

if __name__ == "__main__":
    main()
