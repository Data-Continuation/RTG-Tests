
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
def confirm(ingestion_path: Path, solver_report_path: Path, output_path: Path) -> Path:
    report = load_structured(solver_report_path)
    text = solver_report_path.read_text(encoding="utf-8").lower()
    boundary_ok = ("does_not_claim" in text or "does not claim" in text or "human verification" in text or "claim_boundary" in report)
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "confirmation_surface": "rtg_returned_claim_boundary_confirmation",
        "claim_boundary_confirmed": boundary_ok,
        "publication_claim_allowed": False,
        "ingestion_sha256": sha256_file(ingestion_path),
        "solver_report_sha256": sha256_file(solver_report_path)
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--ingestion", required=True)
    p.add_argument("--solver-report", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote returned claim boundary confirmation: " + str(confirm(Path(a.ingestion), Path(a.solver_report), Path(a.output))))
if __name__ == "__main__":
    main()
