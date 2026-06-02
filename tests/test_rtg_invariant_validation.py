#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; AX=ROOT/"scripts"/"extract_rtg_candidate_axioms.py"; OP=ROOT/"scripts"/"extract_rtg_candidate_operators.py"; INV=ROOT/"scripts"/"validate_rtg_invariants.py"; TMP=ROOT/"build"/"invariant-validation-test"
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def req(x,m):
    if not x: raise AssertionError(m)
def main():
    for s in [AX,OP,INV]: req(s.exists(),f"missing script: {s}")
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    reg=TMP/"registry.json"; ax=TMP/"axioms.json"; op=TMP/"operators.json"; inv=TMP/"invariants.json"
    reg.write_text(json.dumps({"schema_version":"1.0","source_repo":"Data-Continuation/RTG-Tests","registry_type":"rtg_formal_posture_registry","formal_posture_records":[{"solver_run_id":"run-a"}],"summary":{"record_count":1,"total_case_count":2,"formal_posture_counts":{"formally_consistent":1},"ready_for_formal_claim_count":1,"review_required_count":0},"receipt":{}}, indent=2)+"\n", encoding="utf-8")
    load("ax",AX).extract(reg,ax); load("op",OP).extract(ax,op); load("inv",INV).validate(ax,op,inv)
    p=json.loads(inv.read_text())
    req(p["summary"]["invariant_count"]==3,"invariant count mismatch")
    req(p["summary"]["failed_count"]==0,"expected no invariant failures")
    req(p["summary"]["validation_posture"]=="invariants_pass","validation posture mismatch")
    print("RTG invariant validation tests passed.")
if __name__=="__main__": main()
