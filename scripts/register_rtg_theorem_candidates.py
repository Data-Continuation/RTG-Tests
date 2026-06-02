#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
LAYER_ID='rtg_theorem_candidate_registry'
SURFACE='theorem candidate registry'
OUTPUT_KEY='theorem_candidates'
REQUIRED_INPUTS=['proof_candidates']
def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
def build_record(inputs: dict[str, Path], output_path: Path) -> Path:
    payloads={name:load_json(path) for name,path in inputs.items()}
    receipt={f"source_{name}_sha256":sha256_file(path) for name,path in inputs.items()}
    record={"schema_version":"1.0","generated":datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),"source_repo":"Data-Continuation/RTG-Tests","layer_id":LAYER_ID,"surface":SURFACE,OUTPUT_KEY:[],"summary":{},"receipt":receipt}
    if LAYER_ID=="rtg_proof_candidate_generation":
        obligations=payloads["proof_obligations"].get("proof_obligations",[])
        record[OUTPUT_KEY]=[{"proof_candidate_id":"RTG-PC-"+str(i).zfill(3),"source_proof_obligation_id":item.get("proof_obligation_id","unknown"),"candidate_status":"candidate_satisfied" if item.get("status")=="satisfied_candidate" else "open_candidate"} for i,item in enumerate(obligations,start=1)]
        record["summary"]={"proof_candidate_count":len(record[OUTPUT_KEY]),"open_candidate_count":len([c for c in record[OUTPUT_KEY] if c["candidate_status"]!="candidate_satisfied"])}
    elif LAYER_ID=="rtg_theorem_candidate_registry":
        pcs=payloads["proof_candidates"].get("proof_candidates",[])
        record[OUTPUT_KEY]=[{"theorem_candidate_id":item["proof_candidate_id"].replace("RTG-PC","RTG-THM"),"source_proof_candidate_id":item["proof_candidate_id"],"theorem_status":"candidate" if item.get("candidate_status")=="candidate_satisfied" else "review_required"} for item in pcs]
        record["summary"]={"theorem_candidate_count":len(record[OUTPUT_KEY]),"review_required_count":len([t for t in record[OUTPUT_KEY] if t["theorem_status"]!="candidate"])}
    elif LAYER_ID=="rtg_model_check_adapter":
        th=payloads["theorem_candidates"].get("theorem_candidates",[])
        record[OUTPUT_KEY]=[{"model_check_job_id":item["theorem_candidate_id"].replace("RTG-THM","RTG-MC"),"source_theorem_candidate_id":item["theorem_candidate_id"],"adapter_status":"ready_for_model_check"} for item in th]
        record["summary"]={"model_check_job_count":len(record[OUTPUT_KEY]),"adapter_posture":"ready_for_model_check" if record[OUTPUT_KEY] else "empty"}
    elif LAYER_ID=="rtg_external_theorem_prover_adapter":
        th=payloads["theorem_candidates"].get("theorem_candidates",[])
        record[OUTPUT_KEY]=[{"prover_request_id":item["theorem_candidate_id"].replace("RTG-THM","RTG-ATP"),"source_theorem_candidate_id":item["theorem_candidate_id"],"target_prover_class":"external_theorem_prover","adapter_status":"ready_for_external_prover"} for item in th]
        record["summary"]={"prover_request_count":len(record[OUTPUT_KEY]),"adapter_posture":"ready_for_external_prover" if record[OUTPUT_KEY] else "empty"}
    elif LAYER_ID=="rtg_formal_evidence_export":
        record[OUTPUT_KEY]=[{"export_item_id":"RTG-FE-"+key.upper().replace("_","-"),"source_key":key,"source_surface":payload.get("surface",payload.get("registry_surface","unknown"))} for key,payload in payloads.items()]
        record["summary"]={"export_item_count":len(record[OUTPUT_KEY]),"export_posture":"formal_evidence_export_ready"}
    elif LAYER_ID=="rtg_master_records_formal_audit":
        exports=payloads["formal_evidence_export"].get("formal_evidence_exports",[])
        record[OUTPUT_KEY]=[{"audit_item_id":item["export_item_id"].replace("RTG-FE","RTG-MR-AUD"),"source_export_item_id":item["export_item_id"],"audit_status":"candidate_accepted"} for item in exports]
        record["summary"]={"audit_item_count":len(record[OUTPUT_KEY]),"audit_posture":"master_records_candidate_ready" if exports else "audit_review"}
    elif LAYER_ID=="rtg_semantic_formal_traceability":
        axioms=payloads["axioms"].get("candidate_axioms",[]); ops=payloads["operators"].get("candidate_operators",[])
        record[OUTPUT_KEY]=[{"trace_id":"RTG-TRACE-"+a["axiom_id"].split("-")[-1],"semantic_source":"formal_posture_registry","formal_target_id":a["axiom_id"],"trace_status":"candidate_trace"} for a in axioms]+[{"trace_id":"RTG-TRACE-"+op["operator_id"].split("-")[-1],"semantic_source":op.get("domain","unknown"),"formal_target_id":op["operator_id"],"trace_status":"candidate_trace"} for op in ops]
        record["summary"]={"trace_count":len(record[OUTPUT_KEY]),"traceability_posture":"traceable_candidate" if record[OUTPUT_KEY] else "trace_review"}
    elif LAYER_ID=="rtg_axiom_revision_ledger":
        axioms=payloads["axioms"].get("candidate_axioms",[])
        record[OUTPUT_KEY]=[{"ledger_entry_id":"RTG-AX-REV-"+str(i).zfill(3),"axiom_id":a["axiom_id"],"revision_status":"initial_candidate"} for i,a in enumerate(axioms,start=1)]
        record["summary"]={"ledger_entry_count":len(record[OUTPUT_KEY]),"ledger_posture":"revision_tracking_active"}
    elif LAYER_ID=="rtg_operator_closure_check":
        ops=payloads["operators"].get("candidate_operators",[]); domains={op.get("domain") for op in ops}; codomains={op.get("codomain") for op in ops}
        status="candidate_open" if codomains-domains else "candidate_closed"
        record[OUTPUT_KEY]=[{"closure_check_id":"RTG-OC-001","domain_count":len(domains),"codomain_count":len(codomains),"closure_status":status}]
        record["summary"]={"closure_check_count":1,"closure_posture":status}
    elif LAYER_ID=="rtg_invariant_stress_test":
        invs=payloads["invariants"].get("invariants",[])
        record[OUTPUT_KEY]=[{"stress_case_id":"RTG-STRESS-"+str(i).zfill(3),"source_invariant_id":inv["invariant_id"],"stress_result":"pass_candidate" if inv.get("result")=="pass" else "review"} for i,inv in enumerate(invs,start=1)]
        record["summary"]={"stress_case_count":len(record[OUTPUT_KEY]),"stress_review_count":len([s for s in record[OUTPUT_KEY] if s["stress_result"]!="pass_candidate"])}
    elif LAYER_ID=="rtg_minimal_basis_candidate":
        axioms=payloads["axioms"].get("candidate_axioms",[]); ops=payloads["operators"].get("candidate_operators",[])
        sel_ax=[a["axiom_id"] for a in axioms[:max(1,min(2,len(axioms)))]]; sel_op=[op["operator_id"] for op in ops[:max(1,min(2,len(ops)))]]
        record[OUTPUT_KEY]=[{"minimal_basis_id":"RTG-MB-001","selected_axiom_ids":sel_ax,"selected_operator_ids":sel_op,"basis_status":"candidate"}]
        record["summary"]={"minimal_basis_count":1,"selected_axiom_count":len(sel_ax),"selected_operator_count":len(sel_op)}
    elif LAYER_ID=="rtg_formal_architecture_readiness_gate":
        required=["proof_candidates","theorem_candidates","model_check_adapter","external_theorem_prover_adapter","formal_evidence_export","master_records_audit","traceability","axiom_revision_ledger","operator_closure","invariant_stress","minimal_basis"]
        present=[name for name in required if name in payloads]
        status="formal_architecture_ready_candidate" if len(present)==len(required) else "readiness_review"
        record[OUTPUT_KEY]=[{"readiness_gate_id":"RTG-FARG-001","present_layer_count":len(present),"required_layer_count":len(required),"readiness_status":status}]
        record["summary"]={"present_layer_count":len(present),"required_layer_count":len(required),"readiness_posture":status}
    output_path.parent.mkdir(parents=True,exist_ok=True); output_path.write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8"); return output_path
def main():
    p=argparse.ArgumentParser()
    for name in REQUIRED_INPUTS: p.add_argument("--"+name.replace("_","-"),required=True)
    p.add_argument("--output",required=True); a=p.parse_args()
    inputs={name:Path(getattr(a,name)) for name in REQUIRED_INPUTS}
    print("Wrote "+SURFACE+": "+str(build_record(inputs,Path(a.output))))
if __name__=="__main__": main()
