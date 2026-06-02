#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_DISPATCH_FIELDS = [
    "schema_version",
    "source_repo",
    "dispatch_surface",
    "target_workflow_reference",
    "dispatch_status",
    "solver_run_id",
    "input_manifest_path",
    "input_manifest_sha256",
    "case_ids",
    "case_count",
    "expected_solver_result_path",
    "completion_rule",
    "receipt",
]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_contract(dispatch_packet_path: Path, output_path: Path) -> Path:
    packet = json.loads(dispatch_packet_path.read_text(encoding="utf-8"))
    missing = [field for field in REQUIRED_DISPATCH_FIELDS if field not in packet]
    workflow_ok = packet.get("target_workflow_reference") == "GCAT-BCAT-Engine/workflows/math-solver"
    status_ok = packet.get("dispatch_status") in {"dispatch_ready", "dispatch_sent", "solver_running", "solver_results_missing", "solver_results_available", "solver_failed"}
    completion_ok = packet.get("completion_rule") == "do_not_mark_complete_until_solver_results_json_exists"
    case_count_ok = packet.get("case_count") == len(packet.get("case_ids", [])) and packet.get("case_count", 0) > 0

    failures = []
    if missing:
        failures.append({"failure_type": "missing_fields", "details": missing})
    if not workflow_ok:
        failures.append({"failure_type": "workflow_reference_mismatch", "details": packet.get("target_workflow_reference")})
    if not status_ok:
        failures.append({"failure_type": "invalid_dispatch_status", "details": packet.get("dispatch_status")})
    if not completion_ok:
        failures.append({"failure_type": "completion_rule_mismatch", "details": packet.get("completion_rule")})
    if not case_count_ok:
        failures.append({"failure_type": "case_count_mismatch_or_empty", "details": {"case_count": packet.get("case_count"), "case_ids": packet.get("case_ids")}})

    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "contract_surface": "rtg_math_solver_interface_contract",
        "target_workflow_reference": packet.get("target_workflow_reference"),
        "contract_failures": failures,
        "summary": {
            "required_field_count": len(REQUIRED_DISPATCH_FIELDS),
            "missing_field_count": len(missing),
            "failure_count": len(failures),
            "contract_posture": "interface_contract_valid" if not failures else "interface_contract_review",
        },
        "receipt": {
            "dispatch_packet_sha256": sha256_file(dispatch_packet_path),
            "contract_surface": "rtg_math_solver_interface_contract",
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dispatch-packet", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG math-solver interface contract: " + str(validate_contract(Path(a.dispatch_packet), Path(a.output))))

if __name__ == "__main__":
    main()
