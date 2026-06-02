#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def reduce(axioms_path: Path, operators_path: Path, output_path: Path) -> Path:
    axioms = json.loads(axioms_path.read_text(encoding="utf-8"))
    operators = json.loads(operators_path.read_text(encoding="utf-8"))

    classes = {}
    for op in operators.get("candidate_operators", []):
        key = op.get("domain", "unknown") + "=>" + op.get("codomain", "unknown")
        classes.setdefault(key, []).append(op["operator_id"])

    equivalence_classes = [
        {
            "equivalence_class_id": "RTG-EQ-" + str(index).zfill(3),
            "signature": signature,
            "member_operator_ids": members,
            "representative_operator_id": members[0],
        }
        for index, (signature, members) in enumerate(sorted(classes.items()), start=1)
    ]

    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "reduction_surface": "rtg_equivalence_reduction",
        "equivalence_classes": equivalence_classes,
        "summary": {
            "candidate_axiom_count": len(axioms.get("candidate_axioms", [])),
            "candidate_operator_count": len(operators.get("candidate_operators", [])),
            "equivalence_class_count": len(equivalence_classes),
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
    print("Wrote RTG equivalence reduction: " + str(reduce(Path(a.axioms), Path(a.operators), Path(a.output))))
if __name__=="__main__":
    main()
