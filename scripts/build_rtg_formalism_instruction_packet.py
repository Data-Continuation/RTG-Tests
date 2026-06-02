
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
def build_instruction(state_path: Path, output_path: Path) -> Path:
    state = load_structured(state_path)
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "instruction_surface": "rtg_formalism_instruction_packet",
        "target_solver_repo": "GCAT-BCAT-Engine/workflows",
        "target_solver_pattern": "uploaded_spec_plus_anthropic_reasoning_plus_github_ubuntu_validation",
        "formalism": state.get("formalism", "Relative Transition Geometry"),
        "formalism_state_id": state.get("formalism_state_id", "RTG-STATE-UNKNOWN"),
        "declared_task_count": state.get("declared_task_count"),
        "problem_statement": state.get("problem_statement"),
        "known_boundaries": state.get("known_boundaries", []),
        "open_obligations": state.get("open_obligations", []),
        "requested_solver_actions": [
            "classify_formal_problem",
            "derive_candidate_proof_strategy",
            "identify_deterministic_checks_for_ubuntu_runner",
            "separate_candidate_or_reconstruction_from_solution_claim",
            "return_structured_paper_or_report_artifacts"
        ],
        "claim_boundary": {
            "autonomous_theorem_proving_claimed": False,
            "candidate_generation_allowed": True,
            "human_or_formal_verification_required": True
        },
        "receipt": {"formalism_state_sha256": sha256_file(state_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--formalism-state", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG formalism instruction packet: " + str(build_instruction(Path(a.formalism_state), Path(a.output))))
if __name__ == "__main__":
    main()
