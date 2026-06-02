#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

OPERATOR_MAP = {
 "RTG-AXIOM-001-CONSISTENT-SOLVER-EVIDENCE":{"operator_id":"RTG-OP-001-ALLOW-FORMAL-ADVANCE","name":"Allow Formal Advance","domain":"formal_posture_registry","codomain":"formal_claim_gate","transition":"formally_consistent_registry -> allow_formal_claim"},
 "RTG-AXIOM-002-REVIEW-REQUIRED-NONFINALITY":{"operator_id":"RTG-OP-002-DEFER-OR-BLOCK-NONFINAL","name":"Defer Or Block Nonfinal Evidence","domain":"formal_posture_registry","codomain":"formal_claim_gate","transition":"review_required_registry -> defer_or_block_claim"},
 "RTG-AXIOM-003-RECEIPT-BOUND-FORMAL-POSTURE":{"operator_id":"RTG-OP-003-BIND-FORMAL-POSTURE-RECEIPT","name":"Bind Formal Posture Receipt","domain":"formal_posture_record","codomain":"formal_posture_registry","transition":"formal_posture_record -> receipt_bound_registry_entry"}
}

def extract(axioms_path: Path, output_path: Path) -> Path:
    payload = json.loads(axioms_path.read_text(encoding="utf-8"))
    operators = []
    for axiom in payload.get("candidate_axioms", []):
        op = OPERATOR_MAP.get(axiom.get("axiom_id"))
        if op:
            item = dict(op); item["source_axiom_id"] = axiom["axiom_id"]; item["status"] = "candidate"; operators.append(item)
    record = {"schema_version":"1.0","generated":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),"source_repo":payload.get("source_repo","Data-Continuation/RTG-Tests"),"extraction_surface":"rtg_operator_extraction","source_axioms":axioms_path.as_posix(),"candidate_operators":operators,"summary":{"candidate_operator_count":len(operators),"candidate_operator_ids":[op["operator_id"] for op in operators]},"receipt":{"source_axioms_sha256":sha256_file(axioms_path),"extraction_surface":"rtg_operator_extraction"}}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
    return output_path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--axioms",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    print("Wrote RTG candidate operators: " + str(extract(Path(a.axioms), Path(a.output))))
if __name__=="__main__": main()
