#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def require(c,m):
    if not c: raise AssertionError(m)
def read_json(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    t=(ROOT/"math-solver/validation/RTG_UPLOAD_README.md").read_text(encoding="utf-8")
    require("GCAT-BCAT-Engine/workflows" in t,"target repo missing")
    require("run_id=RTG-381-SOLVER-INSTRUCTION-001" in t,"run id missing")
    require("does not claim autonomous theorem proving" in t,"claim boundary missing")
    print("RTG upload-ready README tests passed.")
if __name__=="__main__": main()
