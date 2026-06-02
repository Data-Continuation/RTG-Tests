
from __future__ import annotations
import json, hashlib, re
from datetime import datetime, timezone
from pathlib import Path

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_structured(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        data = {}
        cur = None
        for line in text.splitlines():
            if line and not line.startswith(" ") and ":" in line:
                k, v = line.split(":", 1)
                cur = k.strip()
                data[cur] = v.strip().strip("'\"") if v.strip() else []
            elif cur and line.strip().startswith("- "):
                if not isinstance(data[cur], list):
                    data[cur] = []
                data[cur].append(line.strip()[2:])
        return data

import argparse
def generate(boundary_path: Path, output_path: Path) -> Path:
    boundary = load_structured(boundary_path)
    cls = boundary.get("classification")
    if cls == "reconstruction_not_solution":
        actions = ["select_next_external_reconstruction_benchmark", "require_source_grounding_before_public_status", "compare_reconstruction_quality_against_known_theorem_landscape"]
    elif cls == "candidate_not_verified_solution":
        actions = ["route_candidate_to_deterministic_validation", "request_lean_or_symbolic_check_if_applicable", "prepare_human_review_handoff_receipt"]
    else:
        actions = ["hold_publication_claim", "request_boundary_review", "generate_narrower_instruction_packet"]
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "next_instruction_surface": "rtg_solver_next_instruction_generation",
        "previous_boundary_classification": cls,
        "next_actions": actions,
        "next_instruction_status": "ready_for_governed_review",
        "receipt": {"boundary_sha256": sha256_file(boundary_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--boundary", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG next solver instruction: " + str(generate(Path(a.boundary), Path(a.output))))
if __name__ == "__main__":
    main()
