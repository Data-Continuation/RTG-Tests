#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "bind_rtg_formal_claim_receipt.py"
TMP = ROOT / "build" / "formal-claim-receipt-test"

def require(ok, msg):
    if not ok:
        raise AssertionError(msg)

def main():
    require(SCRIPT.exists(), "formal claim receipt script is missing")
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)
    decision = TMP / "decision.json"
    output = TMP / "receipt.json"
    decision.write_text(json.dumps({
        "schema_version":"1.0",
        "source_repo":"Data-Continuation/RTG-Tests",
        "claim_type":"local_formal_progress",
        "decision":"allow_formal_claim",
        "reason":"registry evidence satisfies formal claim thresholds",
        "thresholds":{"minimum_record_count":1,"minimum_total_case_count":1,"required_ready_for_formal_claim_count":1,"maximum_formally_inconsistent_count":0,"maximum_blocked_count":0},
        "registry_summary":{"record_count":1,"total_case_count":1,"formal_posture_counts":{"formally_consistent":1},"ready_for_formal_claim_count":1},
        "receipt":{"gate_surface":"rtg_formal_claim_gate","formal_posture_registry_sha256":"0"*64}
    }, indent=2) + "\n", encoding="utf-8")
    result = subprocess.run([sys.executable, str(SCRIPT), "--decision", str(decision), "--output", str(output)], cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    payload = json.loads(output.read_text(encoding="utf-8"))
    require(payload["decision"] == "allow_formal_claim", "decision mismatch")
    require(payload["receipt"]["receipt_surface"] == "rtg_formal_claim_receipt", "receipt surface mismatch")
    require("formal_claim_gate_decision_sha256" in payload, "missing gate decision hash")
    print("RTG formal claim receipt tests passed.")

if __name__ == "__main__":
    main()
