
from __future__ import annotations
import json, hashlib, re
from datetime import datetime, timezone
from pathlib import Path

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_structured(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        data = {}
        stack = [(-1, data)]
        for raw in text.splitlines():
            if not raw.strip() or raw.strip().startswith("#"):
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            line = raw.strip()
            if ":" in line and not line.startswith("- "):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip("'\"")
                while stack and stack[-1][0] >= indent:
                    stack.pop()
                parent = stack[-1][1]
                if value == "":
                    parent[key] = {}
                    stack.append((indent, parent[key]))
                else:
                    if value.lower() in {"true", "false"}:
                        parent[key] = value.lower() == "true"
                    else:
                        try:
                            parent[key] = int(value)
                        except ValueError:
                            try:
                                parent[key] = float(value)
                            except ValueError:
                                parent[key] = value
        return data

def walk_numbers(obj, keys=("cost", "spend")):
    vals = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            lk = str(k).lower()
            if any(word in lk for word in keys) and isinstance(v, (int, float)):
                vals.append(float(v))
            vals.extend(walk_numbers(v, keys))
    elif isinstance(obj, list):
        for item in obj:
            vals.extend(walk_numbers(item, keys))
    return vals

import argparse
def validate(instruction_path: Path, handoff_receipt_path: Path, audit_path: Path, readiness_gate_path: Path, output_path: Path) -> Path:
    instruction = load_structured(instruction_path)
    handoff = load_structured(handoff_receipt_path)
    audit = load_structured(audit_path)
    gate = load_structured(readiness_gate_path)
    failures = []
    if not instruction.get("claim_boundary"):
        failures.append("missing_instruction_claim_boundary")
    if handoff.get("handoff_status") != "ready_for_manual_or_automated_math_solver_upload":
        failures.append("handoff_not_ready")
    if audit.get("round_trip_status") != "round_trip_complete":
        failures.append("round_trip_not_complete")
    if not gate.get("repeat_loop_ready"):
        failures.append("repeat_loop_not_ready")
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "contract_surface": "rtg_repeatable_solver_cycle_contract",
        "cycle_contract_valid": not failures,
        "failures": failures,
        "cycle": [
            "instruction_artifact",
            "solver_upload_handoff",
            "returned_artifact_ingestion",
            "round_trip_audit",
            "next_instruction_selection",
            "repeat_readiness_gate"
        ],
        "receipt": {
            "instruction_sha256": sha256_file(instruction_path),
            "handoff_sha256": sha256_file(handoff_receipt_path),
            "audit_sha256": sha256_file(audit_path),
            "readiness_gate_sha256": sha256_file(readiness_gate_path)
        }
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--instruction", required=True)
    p.add_argument("--handoff-receipt", required=True)
    p.add_argument("--audit", required=True)
    p.add_argument("--readiness-gate", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote repeatable solver cycle contract: " + str(validate(Path(a.instruction), Path(a.handoff_receipt), Path(a.audit), Path(a.readiness_gate), Path(a.output))))
if __name__ == "__main__":
    main()
