
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
def gate(state_path: Path, output_path: Path) -> Path:
    state = load_structured(state_path)
    ready = state.get("last_round_trip_status") == "round_trip_complete" and state.get("next_instruction_class") is not None
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "gate_surface": "rtg_repeat_solver_loop_readiness_gate",
        "repeat_loop_ready": ready,
        "gate_status": "repeatable_solver_loop_ready" if ready else "repeatable_solver_loop_review_required",
        "required_next": ["generate_next_instruction_artifact", "upload_to_math_solver_pattern", "ingest_returned_artifacts"],
        "receipt": {"state_sha256": sha256_file(state_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote repeat solver loop readiness gate: " + str(gate(Path(a.state), Path(a.output))))
if __name__ == "__main__":
    main()
