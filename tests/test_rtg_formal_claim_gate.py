#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "gate_rtg_formal_claim.py"
SCHEMA = ROOT / "schemas" / "rtg_formal_claim_gate.schema.json"
TMP = ROOT / "build" / "formal-claim-gate-test"

def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)

def write_registry(path: Path, summary: dict) -> None:
    payload = {
        "schema_version": "1.0",
        "source_repo": "Data-Continuation/RTG-Tests",
        "registry_type": "rtg_formal_posture_registry",
        "formal_posture_records": [],
        "summary": summary,
        "receipt": {"registry_surface": "rtg_formal_posture_registry", "input_directory": "build/solver-results", "record_hashes": []},
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

def run_gate(registry: Path, output: Path) -> dict:
    result = subprocess.run([sys.executable, str(SCRIPT), "--registry", str(registry), "--output", str(output), "--claim-type", "local_formal_progress"], cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    return json.loads(output.read_text(encoding="utf-8"))

def main() -> None:
    require(SCRIPT.exists(), "formal claim gate script is missing")
    require(SCHEMA.exists(), "formal claim gate schema is missing")
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)

    allow_registry = TMP / "allow_registry.json"
    block_registry = TMP / "block_registry.json"
    defer_registry = TMP / "defer_registry.json"

    write_registry(allow_registry, {"record_count": 2, "total_case_count": 5, "formal_posture_counts": {"formally_consistent": 2}, "ready_for_formal_claim_count": 2, "review_required_count": 0})
    write_registry(block_registry, {"record_count": 2, "total_case_count": 5, "formal_posture_counts": {"formally_consistent": 1, "formally_inconsistent": 1}, "ready_for_formal_claim_count": 1, "review_required_count": 1})
    write_registry(defer_registry, {"record_count": 0, "total_case_count": 0, "formal_posture_counts": {}, "ready_for_formal_claim_count": 0, "review_required_count": 0})

    allow = run_gate(allow_registry, TMP / "allow_decision.json")
    block = run_gate(block_registry, TMP / "block_decision.json")
    defer = run_gate(defer_registry, TMP / "defer_decision.json")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for record in (allow, block, defer):
        missing = set(schema["required"]) - set(record)
        require(not missing, "formal claim gate record missing required fields: " + repr(sorted(missing)))
        require(record["schema_version"] == "1.0", "schema_version mismatch")
        require(record["source_repo"] == "Data-Continuation/RTG-Tests", "source_repo mismatch")
        require(record["claim_type"] == "local_formal_progress", "claim_type mismatch")
        require("formal_posture_registry_sha256" in record["receipt"], "missing registry hash receipt")

    require(allow["decision"] == "allow_formal_claim", "allow decision mismatch")
    require(block["decision"] == "block_claim", "block decision mismatch")
    require(defer["decision"] == "defer_claim", "defer decision mismatch")
    print("RTG formal claim gate tests passed.")

if __name__ == "__main__":
    main()
