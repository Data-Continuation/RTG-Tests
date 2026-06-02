#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_THRESHOLDS = {
    "minimum_record_count": 1,
    "minimum_total_case_count": 1,
    "required_ready_for_formal_claim_count": 1,
    "maximum_formally_inconsistent_count": 0,
    "maximum_blocked_count": 0,
}

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_thresholds(config_path: Path | None) -> dict[str, int]:
    thresholds = dict(DEFAULT_THRESHOLDS)
    if config_path and config_path.exists():
        payload = json.loads(config_path.read_text(encoding="utf-8"))
        thresholds.update(payload.get("thresholds", {}))
    return thresholds

def evaluate(summary: dict, thresholds: dict) -> tuple[str, str]:
    counts = summary.get("formal_posture_counts", {})
    inconsistent = int(counts.get("formally_inconsistent", 0))
    blocked = int(counts.get("blocked", 0))
    if inconsistent > thresholds["maximum_formally_inconsistent_count"]:
        return "block_claim", "formal posture registry includes formally_inconsistent evidence"
    if blocked > thresholds["maximum_blocked_count"]:
        return "block_claim", "formal posture registry includes blocked evidence"
    if int(summary.get("record_count", 0)) < thresholds["minimum_record_count"]:
        return "defer_claim", "insufficient formal posture records"
    if int(summary.get("total_case_count", 0)) < thresholds["minimum_total_case_count"]:
        return "defer_claim", "insufficient solver case coverage"
    if int(summary.get("ready_for_formal_claim_count", 0)) < thresholds["required_ready_for_formal_claim_count"]:
        return "defer_claim", "insufficient formally_consistent evidence"
    return "allow_formal_claim", "registry evidence satisfies formal claim thresholds"

def gate(registry_path: Path, output_path: Path, claim_type: str, config_path: Path | None = None) -> Path:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    thresholds = load_thresholds(config_path)
    summary = registry.get("summary", {})
    decision, reason = evaluate(summary, thresholds)
    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": registry.get("source_repo", "Data-Continuation/RTG-Tests"),
        "claim_type": claim_type,
        "decision": decision,
        "reason": reason,
        "thresholds": thresholds,
        "registry_summary": summary,
        "receipt": {
            "gate_surface": "rtg_formal_claim_gate",
            "formal_posture_registry_path": registry_path.as_posix(),
            "formal_posture_registry_sha256": sha256_file(registry_path),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--claim-type", default="local_formal_progress")
    parser.add_argument("--config", default="")
    args = parser.parse_args()
    config_path = Path(args.config) if args.config else None
    out = gate(Path(args.registry), Path(args.output), args.claim_type, config_path)
    print("Wrote RTG formal claim gate decision: " + str(out))

if __name__ == "__main__":
    main()
