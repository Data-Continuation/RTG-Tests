#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(axioms_path: Path, operators_path: Path, output_path: Path) -> Path:
    axioms = json.loads(axioms_path.read_text(encoding="utf-8"))
    operators = json.loads(operators_path.read_text(encoding="utf-8"))
    axiom_ids = {a["axiom_id"] for a in axioms.get("candidate_axioms", [])}
    op_axiom_ids = {op["source_axiom_id"] for op in operators.get("candidate_operators", [])}
    invariants = [
      {"invariant_id":"RTG-INV-001-OPERATOR-SOURCE-AXIOM-BINDING","statement":"Every candidate operator must reference an extracted candidate axiom.","result":"pass" if op_axiom_ids <= axiom_ids else "fail","details":{"operator_source_axioms":sorted(op_axiom_ids),"candidate_axioms":sorted(axiom_ids)}},
      {"invariant_id":"RTG-INV-002-NONEMPTY-FORMAL-CONSTRUCTION","statement":"A formal construction layer must not emit an empty axiom/operator set when source evidence supports formal progress.","result":"pass" if axioms.get("candidate_axioms") and operators.get("candidate_operators") else "fail","details":{"axiom_count":len(axioms.get("candidate_axioms", [])),"operator_count":len(operators.get("candidate_operators", []))}},
      {"invariant_id":"RTG-INV-003-RECEIPT-CONTINUITY","statement":"Axiom and operator extraction outputs must both include upstream source hashes.","result":"pass" if axioms.get("receipt", {}).get("source_registry_sha256") and operators.get("receipt", {}).get("source_axioms_sha256") else "fail","details":{"has_axiom_receipt":bool(axioms.get("receipt", {}).get("source_registry_sha256")),"has_operator_receipt":bool(operators.get("receipt", {}).get("source_axioms_sha256"))}}
    ]
    failed = [i for i in invariants if i["result"] != "pass"]
    record = {"schema_version":"1.0","generated":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),"source_repo":"Data-Continuation/RTG-Tests","validation_surface":"rtg_invariant_validation","invariants":invariants,"summary":{"invariant_count":len(invariants),"passed_count":len(invariants)-len(failed),"failed_count":len(failed),"validation_posture":"invariants_pass" if not failed else "invariants_review"},"receipt":{"source_axioms_sha256":sha256_file(axioms_path),"source_operators_sha256":sha256_file(operators_path),"validation_surface":"rtg_invariant_validation"}}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
    return output_path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--axioms",required=True); p.add_argument("--operators",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    print("Wrote RTG invariant validation: " + str(validate(Path(a.axioms), Path(a.operators), Path(a.output))))
if __name__=="__main__": main()
