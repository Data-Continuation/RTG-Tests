#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "build" / "solver-cost-and-status-receipt-test"

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
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def seed():
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True)
    state = TMP / "state.json"
    artifact = TMP / "artifact.json"
    write_json(state, {
        "formalism": "Relative Transition Geometry",
        "formalism_state_id": "RTG-STATE-358",
        "declared_task_count": 358,
        "problem_statement": "Package RTG formalism state into a governed math-solver instruction artifact.",
        "known_boundaries": ["candidate_generation_not_autonomous_theorem_proving"],
        "open_obligations": ["source_grounding", "artifact_ingestion", "claim_boundary_mapping"]
    })
    write_json(artifact, {
        "presentation_thesis": "The admissible optimization is the cheapest run that preserves task identity.",
        "status": "Final Draft",
        "executive_summary": {"total_api_spend_usd": 0.1095, "total_runs": 4},
        "claim_boundary": {
            "what_this_paper_proves": ["Cost reduction under preserved task identity and auditability."],
            "what_this_paper_does_not_claim": ["Autonomous theorem proving without human verification."]
        },
        "results": {"total_cost_usd": 0.035, "cross_domain_validated": True},
        "presentation_use": "Use as candidate-generation and reconstruction benchmark, not final theorem proof."
    })
    return state, artifact

def pipeline():
    state, artifact = seed()
    instruction = TMP / "instruction.json"
    upload = TMP / "upload.json"
    contract = TMP / "contract.json"
    mapping = TMP / "mapping.json"
    receipt = TMP / "receipt.json"
    gate = TMP / "gate.json"
    boundary = TMP / "boundary.json"
    nexti = TMP / "next.json"
    load("i", ROOT/"scripts/build_rtg_formalism_instruction_packet.py").build_instruction(state, instruction)
    load("u", ROOT/"scripts/build_rtg_math_solver_upload_spec.py").build_upload_spec(instruction, upload)
    load("c", ROOT/"scripts/validate_rtg_solver_paper_artifact_contract.py").validate_artifact(artifact, contract)
    load("m", ROOT/"scripts/map_rtg_solver_claim_boundaries.py").map_claims(artifact, contract, mapping)
    load("r", ROOT/"scripts/receipt_rtg_solver_cost_and_status.py").receipt(artifact, mapping, receipt)
    load("g", ROOT/"scripts/gate_rtg_solver_publication_artifact.py").gate(contract, mapping, receipt, gate)
    load("b", ROOT/"scripts/classify_rtg_solver_reconstruction_solution_boundary.py").classify(artifact, gate, boundary)
    load("n", ROOT/"scripts/generate_rtg_solver_next_instruction.py").generate(boundary, nexti)
    return {"instruction": instruction, "upload": upload, "contract": contract, "mapping": mapping, "receipt": receipt, "gate": gate, "boundary": boundary, "next": nexti}

def main():
    p = pipeline()
    data = json.loads(p["receipt"].read_text())
    require(data["receipt_status"] == "cost_status_receipted", "receipt status mismatch")
    require(data["max_observed_cost_usd"] is not None, "cost observation missing")
    print("RTG solver cost and status receipt tests passed.")
if __name__ == "__main__": main()
