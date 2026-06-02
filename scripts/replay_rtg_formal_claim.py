#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def evaluate(summary: dict, thresholds: dict) -> tuple[str, str]:
    counts = summary.get("formal_posture_counts", {})
    if int(counts.get("formally_inconsistent", 0)) > int(thresholds.get("maximum_formally_inconsistent_count", 0)):
        return "block_claim", "formal posture registry includes formally_inconsistent evidence"
    if int(counts.get("blocked", 0)) > int(thresholds.get("maximum_blocked_count", 0)):
        return "block_claim", "formal posture registry includes blocked evidence"
    if int(summary.get("record_count", 0)) < int(thresholds.get("minimum_record_count", 1)):
        return "defer_claim", "insufficient formal posture records"
    if int(summary.get("total_case_count", 0)) < int(thresholds.get("minimum_total_case_count", 1)):
        return "defer_claim", "insufficient solver case coverage"
    if int(summary.get("ready_for_formal_claim_count", 0)) < int(thresholds.get("required_ready_for_formal_claim_count", 1)):
        return "defer_claim", "insufficient formally_consistent evidence"
    return "allow_formal_claim", "registry evidence satisfies formal claim thresholds"

def replay(receipt_path: Path, registry_path: Path, output_path: Path) -> Path:
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    summary = registry.get("summary", {})
    thresholds = receipt.get("thresholds", {})
    replay_decision, replay_reason = evaluate(summary, thresholds)
    original_decision = receipt.get("decision")
    result = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": receipt.get("source_repo", "Data-Continuation/RTG-Tests"),
        "claim_type": receipt.get("claim_type", "unknown"),
        "original_decision": original_decision,
        "replayed_decision": replay_decision,
        "replay_match": original_decision == replay_decision,
        "replay_reason": replay_reason,
        "registry_summary": summary,
        "thresholds": thresholds,
        "receipt": {
            "replay_surface": "rtg_formal_claim_replay",
            "claim_receipt_path": receipt_path.as_posix(),
            "claim_receipt_sha256": sha256_file(receipt_path),
            "formal_posture_registry_path": registry_path.as_posix(),
            "formal_posture_registry_sha256": sha256_file(registry_path),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = replay(Path(args.receipt), Path(args.registry), Path(args.output))
    print("Wrote RTG formal claim replay result: " + str(out))

if __name__ == "__main__":
    main()
