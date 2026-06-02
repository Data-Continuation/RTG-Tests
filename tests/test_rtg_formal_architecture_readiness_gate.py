#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TMP=ROOT/"build"/"formal-architecture-readiness-gate-test"
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def require(condition,message):
    if not condition: raise AssertionError(message)
def write_json(path,payload):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
def seed_inputs():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    axioms=TMP/"axioms.json"; operators=TMP/"operators.json"; invariants=TMP/"invariants.json"; obligations=TMP/"obligations.json"
    write_json(axioms,{"schema_version":"1.0","candidate_axioms":[{"axiom_id":"RTG-AXIOM-001-CONSISTENT-SOLVER-EVIDENCE"},{"axiom_id":"RTG-AXIOM-003-RECEIPT-BOUND-FORMAL-POSTURE"}],"receipt":{"source_registry_sha256":"0"*64}})
    write_json(operators,{"schema_version":"1.0","candidate_operators":[{"operator_id":"RTG-OP-001-ALLOW-FORMAL-ADVANCE","source_axiom_id":"RTG-AXIOM-001-CONSISTENT-SOLVER-EVIDENCE","domain":"formal_posture_registry","codomain":"formal_claim_gate"},{"operator_id":"RTG-OP-003-BIND-FORMAL-POSTURE-RECEIPT","source_axiom_id":"RTG-AXIOM-003-RECEIPT-BOUND-FORMAL-POSTURE","domain":"formal_posture_record","codomain":"formal_posture_registry"}],"receipt":{"source_axioms_sha256":"1"*64}})
    write_json(invariants,{"schema_version":"1.0","invariants":[{"invariant_id":"RTG-INV-001-OPERATOR-SOURCE-AXIOM-BINDING","result":"pass"},{"invariant_id":"RTG-INV-002-NONEMPTY-FORMAL-CONSTRUCTION","result":"pass"},{"invariant_id":"RTG-INV-003-RECEIPT-CONTINUITY","result":"pass"}],"summary":{"invariant_count":3,"passed_count":3,"failed_count":0}})
    write_json(obligations,{"schema_version":"1.0","proof_obligations":[{"proof_obligation_id":"RTG-PO-001","status":"satisfied_candidate"},{"proof_obligation_id":"RTG-PO-002","status":"satisfied_candidate"},{"proof_obligation_id":"RTG-PO-003","status":"satisfied_candidate"}],"summary":{"proof_obligation_count":3,"open_obligation_count":0}})
    return axioms,operators,invariants,obligations

def main():
    ax,op,inv,obl=seed_inputs(); pc=TMP/"pc.json"; thm=TMP/"thm.json"; mc=TMP/"mc.json"; pr=TMP/"pr.json"; exp=TMP/"exp.json"; audit=TMP/"audit.json"; trace=TMP/"trace.json"; ledger=TMP/"ledger.json"; closure=TMP/"closure.json"; stress=TMP/"stress.json"; basis=TMP/"basis.json"; out=TMP/"ready.json"
    load("pc",ROOT/"scripts"/"generate_rtg_proof_candidates.py").build_record({"proof_obligations":obl},pc); load("thm",ROOT/"scripts"/"register_rtg_theorem_candidates.py").build_record({"proof_candidates":pc},thm); load("mc",ROOT/"scripts"/"adapt_rtg_model_check.py").build_record({"theorem_candidates":thm},mc); load("pr",ROOT/"scripts"/"adapt_rtg_external_theorem_prover.py").build_record({"theorem_candidates":thm},pr); load("ex",ROOT/"scripts"/"export_rtg_formal_evidence.py").build_record({"proof_candidates":pc,"theorem_candidates":thm,"model_check_adapter":mc,"external_theorem_prover_adapter":pr},exp); load("au",ROOT/"scripts"/"audit_rtg_master_records_formal.py").build_record({"formal_evidence_export":exp},audit); load("tr",ROOT/"scripts"/"trace_rtg_semantic_formal.py").build_record({"axioms":ax,"operators":op},trace); load("led",ROOT/"scripts"/"ledger_rtg_axiom_revisions.py").build_record({"axioms":ax},ledger); load("cl",ROOT/"scripts"/"check_rtg_operator_closure.py").build_record({"operators":op},closure); load("st",ROOT/"scripts"/"stress_rtg_invariants.py").build_record({"invariants":inv},stress); load("ba",ROOT/"scripts"/"select_rtg_minimal_basis.py").build_record({"axioms":ax,"operators":op},basis); load("rd",ROOT/"scripts"/"gate_rtg_formal_architecture_readiness.py").build_record({"proof_candidates":pc,"theorem_candidates":thm,"model_check_adapter":mc,"external_theorem_prover_adapter":pr,"formal_evidence_export":exp,"master_records_audit":audit,"traceability":trace,"axiom_revision_ledger":ledger,"operator_closure":closure,"invariant_stress":stress,"minimal_basis":basis},out)
    p=json.loads(out.read_text()); require(p["summary"]["present_layer_count"]==11,"present count mismatch"); require(p["summary"]["readiness_posture"]=="formal_architecture_ready_candidate","posture mismatch")
    print("RTG formal architecture readiness gate tests passed.")
if __name__=="__main__": main()
