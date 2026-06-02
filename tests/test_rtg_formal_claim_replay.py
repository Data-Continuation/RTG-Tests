#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPT_SCRIPT = ROOT / "scripts" / "bind_rtg_formal_claim_receipt.py"
REPLAY_SCRIPT = ROOT / "scripts" / "replay_rtg_formal_claim.py"
TMP = ROOT / "build" / "formal-claim-replay-test"

def require(ok, msg):
    if not ok:
        raise AssertionError(msg)

def main():
    require(RECEIPT_SCRIPT.exists(), "receipt script is missing")
    require(REPLAY_SCRIPT.exists(), "replay script is missing")
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)
    decision = TMP / "decision.json"
    registry = TMP / "registry.json"
    receipt = TMP / "receipt.json"
    replay = TMP / "replay.json"
    summary = {"record_count":2,"total_case_count":5,"formal_posture_counts":{"formally_consistent":2},"ready_for_formal_claim_count":2,"review_required_count":0}
    decision.write_text(json.dumps({"schema_version":"1.0","source_repo":"Data-Continuation/RTG-Tests","claim_type":"local_formal_progress","decision":"allow_formal_claim","reason":"ok","thresholds":{"minimum_record_count":1,"minimum_total_case_count":1,"required_ready_for_formal_claim_count":1,"maximum_formally_inconsistent_count":0,"maximum_blocked_count":0},"registry_summary":summary,"receipt":{"gate_surface":"rtg_formal_claim_gate","formal_posture_registry_sha256":"0"*64}}, indent=2)+"\n", encoding="utf-8")
    registry.write_text(json.dumps({"schema_version":"1.0","source_repo":"Data-Continuation/RTG-Tests","registry_type":"rtg_formal_posture_registry","formal_posture_records":[],"summary":summary,"receipt":{}}, indent=2)+"\n", encoding="utf-8")
    r1 = subprocess.run([sys.executable, str(RECEIPT_SCRIPT), "--decision", str(decision), "--output", str(receipt)], cwd=str(ROOT), text=True, capture_output=True)
    if r1.returncode != 0:
        raise AssertionError(r1.stdout + r1.stderr)
    r2 = subprocess.run([sys.executable, str(REPLAY_SCRIPT), "--receipt", str(receipt), "--registry", str(registry), "--output", str(replay)], cwd=str(ROOT), text=True, capture_output=True)
    if r2.returncode != 0:
        raise AssertionError(r2.stdout + r2.stderr)
    payload = json.loads(replay.read_text(encoding="utf-8"))
    require(payload["original_decision"] == "allow_formal_claim", "original decision mismatch")
    require(payload["replayed_decision"] == "allow_formal_claim", "replayed decision mismatch")
    require(payload["replay_match"] is True, "replay should match")
    require(payload["receipt"]["replay_surface"] == "rtg_formal_claim_replay", "replay surface mismatch")
    print("RTG formal claim replay tests passed.")

if __name__ == "__main__":
    main()
