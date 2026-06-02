#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def search(axioms_path: Path, operators_path: Path, invariants_path: Path, output_path: Path) -> Path:
    axioms = json.loads(axioms_path.read_text(encoding="utf-8"))
    operators = json.loads(operators_path.read_text(encoding="utf-8"))
    invariants = json.loads(invariants_path.read_text(encoding="utf-8"))

    candidates = []
    for invariant in invariants.get("invariants", []):
        if invariant.get("result") != "pass":
            candidates.append({
                "counterexample_id": "RTG-CE-" + invariant["invariant_id"].split("-")[-1],
                "source_invariant_id": invariant["invariant_id"],
                "counterexample_type": "invariant_failure",
                "status": "found",
                "details": invariant.get("details", {}),
            })

    if not candidates:
        candidates.append({
            "counterexample_id": "RTG-CE-000-NONE-FOUND",
            "counterexample_type": "none_found",
            "status": "not_found",
            "details": {
                "candidate_axiom_count": len(axioms.get("candidate_axioms", [])),
                "candidate_operator_count": len(operators.get("candidate_operators", [])),
                "invariant_count": len(invariants.get("invariants", [])),
            },
        })

    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "search_surface": "rtg_counterexample_search",
        "counterexamples": candidates,
        "summary": {
            "counterexample_count": len([c for c in candidates if c["status"] == "found"]),
            "none_found": all(c["status"] != "found" for c in candidates),
        },
        "receipt": {
            "source_axioms_sha256": sha256_file(axioms_path),
            "source_operators_sha256": sha256_file(operators_path),
            "source_invariants_sha256": sha256_file(invariants_path),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--axioms", required=True)
    p.add_argument("--operators", required=True)
    p.add_argument("--invariants", required=True)
    p.add_argument("--output", required=True)
    a=p.parse_args()
    print("Wrote RTG counterexample search: " + str(search(Path(a.axioms), Path(a.operators), Path(a.invariants), Path(a.output))))
if __name__=="__main__":
    main()
