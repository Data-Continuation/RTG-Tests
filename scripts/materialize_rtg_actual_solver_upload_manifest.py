
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
def materialize(instruction_path: Path, problem_spec_path: Path, vector_seed_path: Path, output_path: Path) -> Path:
    manifest = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "manifest_surface": "rtg_actual_solver_upload_bundle_manifest",
        "target_repo": "GCAT-BCAT-Engine/workflows",
        "upload_files": [
            {"source": str(instruction_path), "target": "math_solver/validation/rtg_instruction_artifact.json", "sha256": sha256_file(instruction_path)},
            {"source": str(problem_spec_path), "target": "math_solver/validation/problem_spec_rtg_instruction.yml", "sha256": sha256_file(problem_spec_path)},
            {"source": str(vector_seed_path), "target": "math_solver/validation/candidate_vectors/rtg/rtg_candidate_vectors.json", "sha256": sha256_file(vector_seed_path)}
        ],
        "workflow": ".github/workflows/validation_run_inline.yml",
        "workflow_inputs": {"run_id": "RTG-SOLVER-001", "budget_ceiling": "10.00"},
        "manifest_status": "ready_for_upload"
    }
    return write_json(output_path, manifest)
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--instruction", required=True)
    p.add_argument("--problem-spec", required=True)
    p.add_argument("--vector-seed", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote actual RTG solver upload manifest: " + str(materialize(Path(a.instruction), Path(a.problem_spec), Path(a.vector_seed), Path(a.output))))
if __name__ == "__main__":
    main()
