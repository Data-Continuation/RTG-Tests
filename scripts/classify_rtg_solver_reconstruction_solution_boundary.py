
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
def classify(artifact_path: Path, publication_gate_path: Path, output_path: Path) -> Path:
    text = artifact_path.read_text(encoding="utf-8").lower()
    gate = load_structured(publication_gate_path)
    if "reconstruction" in text and "does not claim" in text:
        classification = "reconstruction_not_solution"
    elif "human verification" in text or "candidate" in text:
        classification = "candidate_not_verified_solution"
    else:
        classification = "solution_boundary_review"
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "boundary_surface": "rtg_solver_reconstruction_vs_solution_boundary",
        "classification": classification,
        "publication_status": gate.get("publication_status"),
        "solution_claim_allowed": False,
        "receipt": {"artifact_sha256": sha256_file(artifact_path), "publication_gate_sha256": sha256_file(publication_gate_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--artifact", required=True)
    p.add_argument("--publication-gate", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG reconstruction vs solution boundary classification: " + str(classify(Path(a.artifact), Path(a.publication_gate), Path(a.output))))
if __name__ == "__main__":
    main()
