
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

def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_structured(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        data = {}
        stack = [(-1, data)]
        for raw in text.splitlines():
            if not raw.strip() or raw.strip().startswith("#"):
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            line = raw.strip()
            if ":" in line and not line.startswith("- "):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip("'\"")
                while stack and stack[-1][0] >= indent:
                    stack.pop()
                parent = stack[-1][1]
                if value == "":
                    parent[key] = {}
                    stack.append((indent, parent[key]))
                else:
                    if value.lower() in {"true", "false"}:
                        parent[key] = value.lower() == "true"
                    else:
                        try:
                            parent[key] = int(value)
                        except ValueError:
                            try:
                                parent[key] = float(value)
                            except ValueError:
                                parent[key] = value
        return data

def walk_numbers(obj, keys=("cost", "spend")):
    vals = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            lk = str(k).lower()
            if any(word in lk for word in keys) and isinstance(v, (int, float)):
                vals.append(float(v))
            vals.extend(walk_numbers(v, keys))
    elif isinstance(obj, list):
        for item in obj:
            vals.extend(walk_numbers(item, keys))
    return vals

import argparse
def materialize(formalism_state_path: Path, output_path: Path) -> Path:
    state = load_structured(formalism_state_path)
    payload = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "artifact_surface": "rtg_actual_instruction_artifact",
        "source_repo": "Data-Continuation/RTG-Tests",
        "target_solver_repo": "GCAT-BCAT-Engine/workflows",
        "instruction_id": state.get("formalism_state_id", "RTG-STATE-381") + "-SOLVER-INSTRUCTION-001",
        "formalism": state.get("formalism", "Relative Transition Geometry"),
        "problem_statement": state.get("problem_statement", "Generate RTG formalism-solving candidate artifacts."),
        "solver_instruction": {
            "anthropic_phase": "derive proof strategy, model boundary classification, deterministic check plan",
            "ubuntu_phase": "run deterministic validation over candidate vectors and produce report artifacts",
            "output_phase": "emit paper/report artifacts with claim boundaries, costs, status, and next obligations"
        },
        "claim_boundary": {
            "candidate_generation_allowed": True,
            "reconstruction_allowed": True,
            "solution_claim_allowed_without_external_verification": False,
            "human_or_formal_verification_required": True
        },
        "open_obligations": state.get("open_obligations", []),
        "receipt": {"formalism_state_sha256": sha256_file(formalism_state_path)}
    }
    return write_json(output_path, payload)
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--formalism-state", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote actual RTG instruction artifact: " + str(materialize(Path(a.formalism_state), Path(a.output))))
if __name__ == "__main__":
    main()
