#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def register(invariants_path: Path, contradictions_path: Path, independence_path: Path, output_path: Path) -> Path:
    invariants = json.loads(invariants_path.read_text(encoding="utf-8"))
    contradictions = json.loads(contradictions_path.read_text(encoding="utf-8"))
    independence = json.loads(independence_path.read_text(encoding="utf-8"))

    obligations = []
    for invariant in invariants.get("invariants", []):
        obligations.append({
            "proof_obligation_id": "RTG-PO-" + invariant["invariant_id"].split("-")[-1],
            "source_type": "invariant",
            "source_id": invariant["invariant_id"],
            "status": "satisfied_candidate" if invariant.get("result") == "pass" else "open",
        })

    for contradiction in contradictions.get("contradictions", []):
        obligations.append({
            "proof_obligation_id": "RTG-PO-CON-" + contradiction["contradiction_id"].split("-")[-1],
            "source_type": "contradiction",
            "source_id": contradiction["contradiction_id"],
            "status": "blocking_open",
        })

    for item in independence.get("axiom_independence_checks", []):
        if item.get("independence_posture") == "independent_candidate":
            obligations.append({
                "proof_obligation_id": "RTG-PO-IND-" + item["axiom_id"].split("-")[-1],
                "source_type": "axiom_independence",
                "source_id": item["axiom_id"],
                "status": "open",
            })

    open_count = len([o for o in obligations if o["status"] in {"open", "blocking_open"}])
    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "registry_surface": "rtg_proof_obligation_registry",
        "proof_obligations": obligations,
        "summary": {
            "proof_obligation_count": len(obligations),
            "open_obligation_count": open_count,
            "satisfied_candidate_count": len([o for o in obligations if o["status"] == "satisfied_candidate"]),
            "registry_posture": "proof_review_required" if open_count else "proof_obligations_candidate_satisfied",
        },
        "receipt": {
            "source_invariants_sha256": sha256_file(invariants_path),
            "source_contradictions_sha256": sha256_file(contradictions_path),
            "source_independence_sha256": sha256_file(independence_path),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--invariants", required=True)
    p.add_argument("--contradictions", required=True)
    p.add_argument("--independence", required=True)
    p.add_argument("--output", required=True)
    a=p.parse_args()
    print("Wrote RTG proof obligation registry: " + str(register(Path(a.invariants), Path(a.contradictions), Path(a.independence), Path(a.output))))
if __name__=="__main__":
    main()
