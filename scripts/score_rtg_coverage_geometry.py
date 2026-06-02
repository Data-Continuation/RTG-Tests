#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def score(axioms_path: Path, operators_path: Path, invariants_path: Path, obligations_path: Path, output_path: Path) -> Path:
    axioms = json.loads(axioms_path.read_text(encoding="utf-8"))
    operators = json.loads(operators_path.read_text(encoding="utf-8"))
    invariants = json.loads(invariants_path.read_text(encoding="utf-8"))
    obligations = json.loads(obligations_path.read_text(encoding="utf-8"))

    axiom_count = len(axioms.get("candidate_axioms", []))
    operator_count = len(operators.get("candidate_operators", []))
    invariant_count = invariants.get("summary", {}).get("invariant_count", 0)
    passed_invariants = invariants.get("summary", {}).get("passed_count", 0)
    open_obligations = obligations.get("summary", {}).get("open_obligation_count", 0)

    raw = 0
    raw += min(30, axiom_count * 10)
    raw += min(30, operator_count * 10)
    raw += 20 if invariant_count and passed_invariants == invariant_count else 0
    raw += 20 if open_obligations == 0 else 5
    score_value = min(100, raw)

    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "scoring_surface": "rtg_coverage_geometry_scoring",
        "coverage_geometry": {
            "candidate_axiom_count": axiom_count,
            "candidate_operator_count": operator_count,
            "invariant_count": invariant_count,
            "passed_invariant_count": passed_invariants,
            "open_proof_obligation_count": open_obligations,
            "coverage_score": score_value,
            "coverage_posture": "formal_coverage_candidate" if score_value >= 80 else "coverage_review_required",
        },
        "receipt": {
            "source_axioms_sha256": sha256_file(axioms_path),
            "source_operators_sha256": sha256_file(operators_path),
            "source_invariants_sha256": sha256_file(invariants_path),
            "source_obligations_sha256": sha256_file(obligations_path),
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
    p.add_argument("--obligations", required=True)
    p.add_argument("--output", required=True)
    a=p.parse_args()
    print("Wrote RTG coverage geometry score: " + str(score(Path(a.axioms), Path(a.operators), Path(a.invariants), Path(a.obligations), Path(a.output))))
if __name__=="__main__":
    main()
