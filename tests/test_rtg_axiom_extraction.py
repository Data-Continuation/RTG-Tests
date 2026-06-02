#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"scripts"/"extract_rtg_candidate_axioms.py"; TMP=ROOT/"build"/"axiom-extraction-test"
def load(path):
    spec=importlib.util.spec_from_file_location("axiom_mod", path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod
def req(x,m):
    if not x: raise AssertionError(m)
def main():
    req(SCRIPT.exists(),"axiom extraction script is missing")
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    reg=TMP/"registry.json"; out=TMP/"axioms.json"
    reg.write_text(json.dumps({"schema_version":"1.0","source_repo":"Data-Continuation/RTG-Tests","registry_type":"rtg_formal_posture_registry","formal_posture_records":[{"solver_run_id":"run-a"}],"summary":{"record_count":1,"total_case_count":2,"formal_posture_counts":{"formally_consistent":1},"ready_for_formal_claim_count":1,"review_required_count":0},"receipt":{}}, indent=2)+"\n", encoding="utf-8")
    load(SCRIPT).extract(reg,out)
    p=json.loads(out.read_text()); ids=p["summary"]["candidate_axiom_ids"]
    req(p["summary"]["candidate_axiom_count"]>=2,"expected at least two candidate axioms")
    req("RTG-AXIOM-001-CONSISTENT-SOLVER-EVIDENCE" in ids,"missing consistent evidence axiom")
    req("RTG-AXIOM-003-RECEIPT-BOUND-FORMAL-POSTURE" in ids,"missing receipt-bound axiom")
    req("source_registry_sha256" in p["receipt"],"missing source registry hash")
    print("RTG axiom extraction tests passed.")
if __name__=="__main__": main()
