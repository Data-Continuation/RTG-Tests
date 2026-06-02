#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def candidate_axioms(registry: dict) -> list[dict]:
    summary = registry.get("summary", {})
    counts = summary.get("formal_posture_counts", {})
    records = registry.get("formal_posture_records", [])
    axioms = []
    if int(summary.get("ready_for_formal_claim_count", 0)) > 0 and int(counts.get("formally_inconsistent", 0)) == 0:
        axioms.append({"axiom_id":"RTG-AXIOM-001-CONSISTENT-SOLVER-EVIDENCE","name":"Consistent Solver Evidence Admissibility","statement":"A formal claim may be locally advanced only when registered solver evidence contains formally consistent posture records and no formally inconsistent records.","supporting_record_count":int(summary.get("ready_for_formal_claim_count",0)),"status":"candidate","source":"formal_posture_registry"})
    if int(summary.get("review_required_count", 0)) > 0:
        axioms.append({"axiom_id":"RTG-AXIOM-002-REVIEW-REQUIRED-NONFINALITY","name":"Review Required Nonfinality","statement":"A transition class with underconstrained, blocked, mixed, or inconsistent evidence cannot become final without additional formal review.","supporting_record_count":int(summary.get("review_required_count",0)),"status":"candidate","source":"formal_posture_registry"})
    if records:
        axioms.append({"axiom_id":"RTG-AXIOM-003-RECEIPT-BOUND-FORMAL-POSTURE","name":"Receipt-Bound Formal Posture","statement":"A formal posture record is admissible as RTG evidence only when it is bound to a source hash and registry receipt.","supporting_record_count":len(records),"status":"candidate","source":"formal_posture_registry"})
    return axioms

def extract(registry_path: Path, output_path: Path) -> Path:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    axioms = candidate_axioms(registry)
    record = {"schema_version":"1.0","generated":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),"source_repo":registry.get("source_repo","Data-Continuation/RTG-Tests"),"extraction_surface":"rtg_axiom_extraction","source_registry":registry_path.as_posix(),"candidate_axioms":axioms,"summary":{"candidate_axiom_count":len(axioms),"candidate_axiom_ids":[a["axiom_id"] for a in axioms]},"receipt":{"source_registry_sha256":sha256_file(registry_path),"extraction_surface":"rtg_axiom_extraction"}}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2)+"\n", encoding="utf-8")
    return output_path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--registry",required=True); p.add_argument("--output",required=True); a=p.parse_args()
    print("Wrote RTG candidate axioms: " + str(extract(Path(a.registry), Path(a.output))))
if __name__=="__main__": main()
