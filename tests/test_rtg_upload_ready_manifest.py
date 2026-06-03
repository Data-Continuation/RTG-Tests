#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def require(c,m):
    if not c: raise AssertionError(m)
def read_json(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    d=read_json("math-solver/validation/rtg_upload_manifest.json")
    require(d["manifest_status"]=="upload_ready","manifest status mismatch")
    require(".github/workflows/validation_run_inline.yml" in d["workflow_targets"],"workflow target missing")
    targets={f["target_path"] for f in d["upload_files"]}
    require("math_solver/validation/rtg_instruction_artifact.json" in targets,"instruction target missing")
    require("math_solver/validation/problem_spec_rtg_instruction.yml" in targets,"spec target missing")
    require("math_solver/validation/candidate_vectors/rtg/rtg_candidate_vectors.json" in targets,"vectors target missing")
    print("RTG upload-ready manifest tests passed.")
if __name__=="__main__": main()
