#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def require(c,m):
    if not c: raise AssertionError(m)
def read_json(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    d=read_json("math-solver/validation/rtg_instruction_artifact.json")
    require(d["instruction_id"]=="RTG-381-SOLVER-INSTRUCTION-001","instruction id mismatch")
    require(d["target_repo"]=="GCAT-BCAT-Engine/workflows","target repo mismatch")
    require(d["claim_boundary"]["autonomous_theorem_proving_claimed"] is False,"claim boundary mismatch")
    print("RTG upload-ready instruction artifact tests passed.")
if __name__=="__main__": main()
