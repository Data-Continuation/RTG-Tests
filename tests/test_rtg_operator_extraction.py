#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; AX=ROOT/"scripts"/"extract_rtg_candidate_axioms.py"; OP=ROOT/"scripts"/"extract_rtg_candidate_operators.py"; TMP=ROOT/"build"/"operator-extraction-test"
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def req(x,m):
    if not x: raise AssertionError(m)
def main():
    req(AX.exists(),"axiom script is missing"); req(OP.exists(),"operator script is missing")
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    reg=TMP/"registry.json"; ax=TMP/"axioms.json"; op=TMP/"operators.json"
    reg.write_text(json.dumps({"schema_version":"1.0","source_repo":"Data-Continuation/RTG-Tests","registry_type":"rtg_formal_posture_registry","formal_posture_records":[{"solver_run_id":"run-a"}],"summary":{"record_count":1,"total_case_count":2,"formal_posture_counts":{"formally_consistent":1},"ready_for_formal_claim_count":1,"review_required_count":0},"receipt":{}}, indent=2)+"\n", encoding="utf-8")
    load("ax",AX).extract(reg,ax); load("op",OP).extract(ax,op)
    p=json.loads(op.read_text()); ids=p["summary"]["candidate_operator_ids"]
    req(p["summary"]["candidate_operator_count"]>=2,"expected at least two candidate operators")
    req("RTG-OP-001-ALLOW-FORMAL-ADVANCE" in ids,"missing allow operator")
    req("RTG-OP-003-BIND-FORMAL-POSTURE-RECEIPT" in ids,"missing receipt operator")
    req("source_axioms_sha256" in p["receipt"],"missing source axiom hash")
    print("RTG operator extraction tests passed.")
if __name__=="__main__": main()
