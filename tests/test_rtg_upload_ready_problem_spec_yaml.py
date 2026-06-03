#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def require(c,m):
    if not c: raise AssertionError(m)
def read_json(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    t=(ROOT/"math-solver/validation/problem_spec_rtg_instruction.yml").read_text(encoding="utf-8")
    require("problem_spec_rtg_instruction_v1:" in t,"root missing")
    require("problem_id: RTG-381-SOLVER-INSTRUCTION-001" in t,"id missing")
    require("human_or_formal_verification_required: true" in t,"boundary missing")
    require("do not ask the API for work the Ubuntu runner can check deterministically" in t,"minimization missing")
    print("RTG upload-ready problem spec YAML tests passed.")
if __name__=="__main__": main()
