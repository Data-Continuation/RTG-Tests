#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def audit(input_dir: Path, output_path: Path) -> Path:
    receipts, replays = [], []
    for path in sorted(input_dir.rglob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("receipt", {}).get("receipt_surface") == "rtg_formal_claim_receipt":
            receipts.append((path, payload))
        if payload.get("receipt", {}).get("replay_surface") == "rtg_formal_claim_replay":
            replays.append((path, payload))

    decision_counts = {}
    for _, payload in receipts:
        decision = payload.get("decision", "unknown")
        decision_counts[decision] = decision_counts.get(decision, 0) + 1

    replay_match_count = sum(1 for _, payload in replays if payload.get("replay_match") is True)
    replay_mismatch_count = sum(1 for _, payload in replays if payload.get("replay_match") is False)

    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "audit_type": "rtg_formal_claim_audit",
        "summary": {
            "receipt_count": len(receipts),
            "replay_count": len(replays),
            "decision_counts": decision_counts,
            "replay_match_count": replay_match_count,
            "replay_mismatch_count": replay_mismatch_count,
            "audit_posture": "audit_pass" if receipts and replay_mismatch_count == 0 else "audit_review",
        },
        "receipt": {
            "audit_surface": "rtg_formal_claim_audit",
            "input_directory": input_dir.as_posix(),
            "input_hashes": [sha256_file(path) for path, _ in receipts + replays],
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = audit(Path(args.input_dir), Path(args.output))
    print("Wrote RTG formal claim audit: " + str(out))

if __name__ == "__main__":
    main()
