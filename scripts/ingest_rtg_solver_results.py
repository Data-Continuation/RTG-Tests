#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

MAP = {
    "satisfiable": "admissible",
    "contradictory": "blocked",
    "underconstrained": "deferred",
    "overconstrained": "review",
    "equivalent_to_prior_case": "admissible_equivalent",
    "requires_new_axiom_or_operator": "requires_formal_extension",
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("solver results must be an object")
    if not isinstance(payload.get("case_results"), list):
        raise ValueError("solver results must include case_results list")
    return payload

def formal_posture(items):
    if not items:
        return "blocked"
    states = {x["solver_posture"] for x in items}
    if "contradictory" in states:
        return "formally_inconsistent"
    if states <= {"satisfiable", "equivalent_to_prior_case"}:
        return "formally_consistent"
    if states <= {"underconstrained"}:
        return "underconstrained"
    return "mixed_or_requires_review"

def summary(items):
    solver_counts, admiss_counts = {}, {}
    for item in items:
        solver_counts[item["solver_posture"]] = solver_counts.get(item["solver_posture"], 0) + 1
        admiss_counts[item["rtg_admissibility"]] = admiss_counts.get(item["rtg_admissibility"], 0) + 1
    return {"case_count": len(items), "solver_posture_counts": solver_counts, "rtg_admissibility_counts": admiss_counts}

def ingest(input_path: Path, output_path: Path) -> Path:
    payload = load(input_path)
    items = []
    for result in payload["case_results"]:
        case_id = result.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise ValueError("case_result missing case_id")
        posture = result.get("solver_posture", result.get("posture", "underconstrained"))
        if posture not in MAP:
            posture = "underconstrained"
        items.append({
            "case_id": case_id,
            "solver_posture": posture,
            "rtg_admissibility": MAP[posture],
            "solver_confidence": result.get("solver_confidence", result.get("confidence")),
            "notes": result.get("notes", "")
        })
    record = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z"),
        "source_repo": payload.get("source_repo", "Data-Continuation/RTG-Tests"),
        "solver_run_id": payload.get("solver_run_id", payload.get("run_id", "unknown_solver_run")),
        "source_solver_results": input_path.as_posix(),
        "formal_posture": formal_posture(items),
        "case_postures": items,
        "admissibility_summary": summary(items),
        "receipt": {
            "solver_results_sha256": sha(input_path),
            "ingestion_surface": "rtg_solver_result_ingestion",
            "target_workflow_reference": payload.get("target_workflow_reference", "GCAT-BCAT-Engine/workflows/math-solver")
        }
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return output_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = ingest(Path(args.input), Path(args.output))
    print("Wrote RTG formal posture record: " + str(out))

if __name__ == "__main__":
    main()
