#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_RECEIPT_FIELDS = [
    "schema_version",
    "authority_surface",
    "authority_status",
    "authority_class",
    "authorized_action",
    "source_request_sha256",
    "credential_boundary",
    "target_workflow",
    "issued_by",
]

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path

def validate_authority_receipt(request_path: Path, receipt_path: Path, output_path: Path) -> Path:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_RECEIPT_FIELDS if field not in receipt]
    request_hash_ok = receipt.get("source_request_sha256") == sha256_file(request_path)
    granted = receipt.get("authority_status") == "authority_granted"
    class_ok = receipt.get("authority_class") == "math_solver_workflow_dispatch"
    action_ok = receipt.get("authorized_action") == "authorize_math_solver_workflow_dispatch"
    boundary_ok = receipt.get("credential_boundary") == "tv_tvc_brokered"
    target_ok = receipt.get("target_workflow") == request.get("target_workflow")
    failures = []
    if missing:
        failures.append({"failure_type": "missing_receipt_fields", "details": missing})
    if not request_hash_ok:
        failures.append({"failure_type": "request_hash_mismatch"})
    if not granted:
        failures.append({"failure_type": "authority_not_granted", "details": receipt.get("authority_status")})
    if not class_ok:
        failures.append({"failure_type": "authority_class_mismatch"})
    if not action_ok:
        failures.append({"failure_type": "authorized_action_mismatch"})
    if not boundary_ok:
        failures.append({"failure_type": "credential_boundary_mismatch"})
    if not target_ok:
        failures.append({"failure_type": "target_workflow_mismatch"})
    validation = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "validation_surface": "rtg_tv_tvc_authority_receipt_validation",
        "authority_receipt_valid": not failures,
        "failures": failures,
        "summary": {
            "failure_count": len(failures),
            "validation_posture": "authority_receipt_valid" if not failures else "authority_receipt_review",
        },
        "receipt": {
            "request_sha256": sha256_file(request_path),
            "authority_receipt_sha256": sha256_file(receipt_path),
        },
    }
    return write_json(output_path, validation)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--request", required=True)
    p.add_argument("--authority-receipt", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG TV/TVC authority receipt validation: " + str(validate_authority_receipt(Path(a.request), Path(a.authority_receipt), Path(a.output))))

if __name__ == "__main__":
    main()
