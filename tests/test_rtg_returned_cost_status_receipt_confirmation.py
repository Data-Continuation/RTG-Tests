#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, importlib.util
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "build" / "test_rtg_returned_cost_status_receipt_confirmation"

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
    state = TMP / "rtg_formalism_state.json"
    report_dir = TMP / "returned_artifacts"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = report_dir / "publisher_document_or_solver_report.json"
    write_json(state, {
        "formalism": "Relative Transition Geometry",
        "formalism_state_id": "RTG-STATE-366",
        "declared_task_count": 366,
        "problem_statement": "Run the first actual RTG formalism-solving instruction through the math-solver pattern.",
        "open_obligations": ["preserve claim boundary", "confirm costs", "produce next instruction"]
    })
    write_json(report, {
        "status": "candidate_generation_complete",
        "presentation_thesis": "RTG generated a candidate formalism-solving artifact under claim boundaries.",
        "executive_summary": {"total_api_spend_usd": 0.041, "total_runs": 1},
        "claim_boundary": {
            "what_this_artifact_proves": ["RTG instruction handoff and candidate artifact generation completed."],
            "what_this_artifact_does_not_claim": ["Autonomous theorem proving or final correctness without human verification."]
        },
        "results": {"total_cost_usd": 0.041, "candidate_generation_validated": True}
    })
    summary = report_dir / "gcat_bcat_candidate_summary.md"
    summary.write_text("# Candidate Summary\n\nHuman verification required.\n", encoding="utf-8")
    return state, report_dir, report

def pipeline():
    state, report_dir, report = seed()
    instruction = TMP / "actual_instruction.json"
    spec = TMP / "problem_spec_rtg_instruction.yml"
    vectors = TMP / "candidate_vectors.json"
    upload_manifest = TMP / "upload_manifest.json"
    handoff = TMP / "handoff_receipt.json"
    collection = TMP / "artifact_collection.json"
    ingestion = TMP / "artifact_ingestion.json"
    claim_confirm = TMP / "claim_confirmation.json"
    cost_confirm = TMP / "cost_confirmation.json"
    audit = TMP / "round_trip_audit.json"
    selection = TMP / "next_selection.json"
    delta = TMP / "instruction_delta.json"
    loop_state = TMP / "loop_state.json"
    readiness = TMP / "readiness_gate.json"
    cycle = TMP / "cycle_contract.json"
    load("s1", ROOT/"scripts/materialize_rtg_actual_instruction_artifact.py").materialize(state, instruction)
    load("s2", ROOT/"scripts/materialize_rtg_actual_problem_spec_yaml.py").materialize(instruction, spec)
    load("s3", ROOT/"scripts/materialize_rtg_actual_candidate_vector_seeds.py").materialize(instruction, vectors)
    load("s4", ROOT/"scripts/materialize_rtg_actual_solver_upload_manifest.py").materialize(instruction, spec, vectors, upload_manifest)
    load("s5", ROOT/"scripts/materialize_rtg_actual_solver_handoff_receipt.py").materialize(upload_manifest, handoff)
    load("s6", ROOT/"scripts/collect_rtg_returned_solver_artifacts.py").collect(report_dir, collection)
    load("s7", ROOT/"scripts/ingest_rtg_returned_solver_artifacts.py").ingest(collection, ingestion)
    load("s8", ROOT/"scripts/confirm_rtg_returned_claim_boundaries.py").confirm(ingestion, report, claim_confirm)
    load("s9", ROOT/"scripts/confirm_rtg_returned_cost_status_receipt.py").confirm(report, cost_confirm)
    load("s10", ROOT/"scripts/materialize_rtg_returned_round_trip_audit.py").materialize(handoff, ingestion, claim_confirm, cost_confirm, audit)
    load("s11", ROOT/"scripts/select_rtg_repeat_next_instruction.py").select(audit, selection)
    load("s12", ROOT/"scripts/materialize_rtg_repeat_instruction_delta.py").materialize(instruction, selection, delta)
    load("s13", ROOT/"scripts/update_rtg_repeat_solver_loop_state.py").update(audit, delta, loop_state)
    load("s14", ROOT/"scripts/gate_rtg_repeat_solver_loop_readiness.py").gate(loop_state, readiness)
    load("s15", ROOT/"scripts/validate_rtg_repeatable_solver_cycle_contract.py").validate(instruction, handoff, audit, readiness, cycle)
    return {
        "instruction": instruction, "spec": spec, "vectors": vectors, "upload_manifest": upload_manifest,
        "handoff": handoff, "collection": collection, "ingestion": ingestion, "claim_confirm": claim_confirm,
        "cost_confirm": cost_confirm, "audit": audit, "selection": selection, "delta": delta,
        "loop_state": loop_state, "readiness": readiness, "cycle": cycle
    }

def main():
    p = pipeline()
    data=json.loads(pipeline()["cost_confirm"].read_text()); require(data["cost_status_confirmed"] is True,"cost status not confirmed"); require(data["max_observed_cost_usd"]==0.041,"cost mismatch")
    print("RTG returned cost/status receipt confirmation tests passed.")
if __name__ == "__main__":
    main()
