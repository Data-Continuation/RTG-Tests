#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "build" / "axiom-independence-test"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

def fixtures():
    axioms = {
        "schema_version":"1.0",
        "source_repo":"Data-Continuation/RTG-Tests",
        "candidate_axioms":[
            {"axiom_id":"RTG-AXIOM-001-CONSISTENT-SOLVER-EVIDENCE"},
            {"axiom_id":"RTG-AXIOM-003-RECEIPT-BOUND-FORMAL-POSTURE"}
        ],
        "summary":{"candidate_axiom_count":2},
        "receipt":{"source_registry_sha256":"0"*64}
    }
    operators = {
        "schema_version":"1.0",
        "candidate_operators":[
            {"operator_id":"RTG-OP-001-ALLOW-FORMAL-ADVANCE","source_axiom_id":"RTG-AXIOM-001-CONSISTENT-SOLVER-EVIDENCE","domain":"formal_posture_registry","codomain":"formal_claim_gate"},
            {"operator_id":"RTG-OP-003-BIND-FORMAL-POSTURE-RECEIPT","source_axiom_id":"RTG-AXIOM-003-RECEIPT-BOUND-FORMAL-POSTURE","domain":"formal_posture_record","codomain":"formal_posture_registry"}
        ],
        "summary":{"candidate_operator_count":2},
        "receipt":{"source_axioms_sha256":"1"*64}
    }
    invariants = {
        "schema_version":"1.0",
        "invariants":[
            {"invariant_id":"RTG-INV-001-OPERATOR-SOURCE-AXIOM-BINDING","result":"pass","details":{}},
            {"invariant_id":"RTG-INV-002-NONEMPTY-FORMAL-CONSTRUCTION","result":"pass","details":{}},
            {"invariant_id":"RTG-INV-003-RECEIPT-CONTINUITY","result":"pass","details":{}}
        ],
        "summary":{"invariant_count":3,"passed_count":3,"failed_count":0,"validation_posture":"invariants_pass"},
        "receipt":{"source_axioms_sha256":"2"*64,"source_operators_sha256":"3"*64}
    }
    return axioms, operators, invariants

def main():
    if TMP.exists(): shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    axioms, operators, _ = fixtures()
    ax = TMP/"axioms.json"; op = TMP/"operators.json"; out = TMP/"independence.json"
    write_json(ax, axioms); write_json(op, operators)
    mod = load("independence", ROOT/"scripts"/"check_rtg_axiom_independence.py")
    mod.check(ax, op, out)
    payload = json.loads(out.read_text())
    require(payload["summary"]["checked_axiom_count"] == 2, "checked count mismatch")
    require(payload["summary"]["operator_bound_axiom_count"] == 2, "operator-bound count mismatch")
    print("RTG axiom independence tests passed.")
if __name__ == "__main__": main()
