#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def bind_receipt(decision_path: Path, output_path: Path) -> Path:
    decision = json.loads(decision_path.read_text(encoding="utf-8"))
    receipt = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": decision.get("source_repo", "Data-Continuation/RTG-Tests"),
        "claim_type": decision.get("claim_type", "unknown"),
        "decision": decision.get("decision", "unknown"),
        "reason": decision.get("reason", ""),
        "formal_claim_gate_decision_path": decision_path.as_posix(),
        "formal_claim_gate_decision_sha256": sha256_file(decision_path),
        "registry_summary": decision.get("registry_summary", {}),
        "thresholds": decision.get("thresholds", {}),
        "receipt": {
            "receipt_surface": "rtg_formal_claim_receipt",
            "upstream_gate_surface": decision.get("receipt", {}).get("gate_surface", "rtg_formal_claim_gate"),
            "formal_posture_registry_sha256": decision.get("receipt", {}).get("formal_posture_registry_sha256", ""),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = bind_receipt(Path(args.decision), Path(args.output))
    print("Wrote RTG formal claim receipt: " + str(out))

if __name__ == "__main__":
    main()
