#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def classify(counterexamples_path: Path, output_path: Path) -> Path:
    payload = json.loads(counterexamples_path.read_text(encoding="utf-8"))
    found = [c for c in payload.get("counterexamples", []) if c.get("status") == "found"]

    contradictions = []
    for item in found:
        contradictions.append({
            "contradiction_id": item["counterexample_id"].replace("RTG-CE", "RTG-CON"),
            "source_counterexample_id": item["counterexample_id"],
            "contradiction_class": "structural_invariant_contradiction",
            "severity": "blocking",
            "status": "requires_review",
        })

    posture = "no_contradiction_detected" if not contradictions else "contradiction_review_required"
    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "classification_surface": "rtg_contradiction_classification",
        "contradictions": contradictions,
        "summary": {
            "contradiction_count": len(contradictions),
            "classification_posture": posture,
        },
        "receipt": {
            "source_counterexamples_sha256": sha256_file(counterexamples_path),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--counterexamples", required=True)
    p.add_argument("--output", required=True)
    a=p.parse_args()
    print("Wrote RTG contradiction classification: " + str(classify(Path(a.counterexamples), Path(a.output))))
if __name__=="__main__":
    main()
