#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_SCRIPT = ROOT / "scripts" / "bind_rtg_formal_claim_receipt.py"
REPLAY_SCRIPT = ROOT / "scripts" / "replay_rtg_formal_claim.py"
AUDIT_SCRIPT = ROOT / "scripts" / "audit_rtg_formal_claims.py"
TMP = ROOT / "build" / "formal-claim-audit-test"

def require(ok, msg):
    if not ok:
        raise AssertionError(msg)

def main():
    for script in (RECEIPT_SCRIPT, REPLAY_SCRIPT, AUDIT_SCRIPT):
        require(script.exists(), f"missing script: {script}")
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)
    summary = {"record_count":1,"total_case_count":1,"formal_posture_counts":{"formally_consistent":1},"ready_for_formal_claim_count":1,"review_required_count":0}
    thresholds = {"minimum_record_count":1,"minimum_total_case_count":1,"required_ready_for_formal_claim_count":1,"maximum_formally_inconsistent_count":0,"maximum_blocked_count":0}
    decision = TMP / "decision.json"
    registry = TMP / "registry.json"
    receipt = TMP / "receipt.json"
    replay = TMP / "replay.json"
    audit = TMP / "audit.json"
    decision.write_text(json.dumps({"schema_version":"1.0","source_repo":"Data-Continuation/RTG-Tests","claim_type":"local_formal_progress","decision":"allow_formal_claim","reason":"ok","thresholds":thresholds,"registry_summary":summary,"receipt":{"gate_surface":"rtg_formal_claim_gate","formal_posture_registry_sha256":"0"*64}}, indent=2)+"\n", encoding="utf-8")
    registry.write_text(json.dumps({"schema_version":"1.0","source_repo":"Data-Continuation/RTG-Tests","registry_type":"rtg_formal_posture_registry","formal_posture_records":[],"summary":summary,"receipt":{}}, indent=2)+"\n", encoding="utf-8")
    for cmd in [
        [sys.executable, str(RECEIPT_SCRIPT), "--decision", str(decision), "--output", str(receipt)],
        [sys.executable, str(REPLAY_SCRIPT), "--receipt", str(receipt), "--registry", str(registry), "--output", str(replay)],
        [sys.executable, str(AUDIT_SCRIPT), "--input-dir", str(TMP), "--output", str(audit)],
    ]:
        result = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True)
        if result.returncode != 0:
            raise AssertionError(result.stdout + result.stderr)
    payload = json.loads(audit.read_text(encoding="utf-8"))
    require(payload["summary"]["receipt_count"] == 1, "receipt_count mismatch")
    require(payload["summary"]["replay_count"] == 1, "replay_count mismatch")
    require(payload["summary"]["replay_match_count"] == 1, "replay_match_count mismatch")
    require(payload["summary"]["audit_posture"] == "audit_pass", "audit_posture mismatch")
    print("RTG formal claim audit tests passed.")

if __name__ == "__main__":
    main()
