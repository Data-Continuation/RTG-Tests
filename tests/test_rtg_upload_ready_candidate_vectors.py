#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def require(c,m):
    if not c: raise AssertionError(m)
def read_json(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    d=read_json("math_solver/validation/candidate_vectors/rtg/rtg_candidate_vectors.json")
    v=d["candidate_vectors"]; require(len(v)==4,"vector count mismatch")
    c={x["class"] for x in v}
    require({"admissible_transition_candidate","false_transition_candidate","unknown_unknown_candidate","repeatable_round_trip_candidate"}.issubset(c),"classes missing")
    print("RTG upload-ready candidate vectors tests passed.")
if __name__=="__main__": main()
