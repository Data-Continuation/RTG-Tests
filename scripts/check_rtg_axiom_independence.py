#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(axioms_path: Path, operators_path: Path, output_path: Path) -> Path:
    axioms = json.loads(axioms_path.read_text(encoding="utf-8"))
    operators = json.loads(operators_path.read_text(encoding="utf-8"))

    operator_sources = {op["source_axiom_id"] for op in operators.get("candidate_operators", [])}
    checks = []
    for axiom in axioms.get("candidate_axioms", []):
        axiom_id = axiom["axiom_id"]
        checks.append({
            "axiom_id": axiom_id,
            "referenced_by_operator": axiom_id in operator_sources,
            "independence_posture": "not_independent_candidate" if axiom_id in operator_sources else "independent_candidate",
        })

    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "check_surface": "rtg_axiom_independence",
        "axiom_independence_checks": checks,
        "summary": {
            "checked_axiom_count": len(checks),
            "independent_candidate_count": len([c for c in checks if c["independence_posture"] == "independent_candidate"]),
            "operator_bound_axiom_count": len([c for c in checks if c["referenced_by_operator"]]),
        },
        "receipt": {
            "source_axioms_sha256": sha256_file(axioms_path),
            "source_operators_sha256": sha256_file(operators_path),
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--axioms", required=True)
    p.add_argument("--operators", required=True)
    p.add_argument("--output", required=True)
    a=p.parse_args()
    print("Wrote RTG axiom independence check: " + str(check(Path(a.axioms), Path(a.operators), Path(a.output))))
if __name__=="__main__":
    main()
