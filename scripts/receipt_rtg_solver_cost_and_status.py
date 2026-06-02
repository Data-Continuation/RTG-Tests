
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
def receipt(artifact_path: Path, claim_mapping_path: Path, output_path: Path) -> Path:
    artifact = load_structured(artifact_path)
    mapping = load_structured(claim_mapping_path)
    costs = walk_numbers(artifact)
    status = artifact.get("status") or artifact.get("pipeline_status") or artifact.get("presentation_status") or "status_not_declared"
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "receipt_surface": "rtg_solver_cost_and_status_receipt",
        "status_observed": status,
        "cost_values_observed_usd": costs,
        "max_observed_cost_usd": max(costs) if costs else None,
        "claim_boundary_status": mapping.get("claim_boundary_status"),
        "receipt_status": "cost_status_receipted",
        "receipt": {"artifact_sha256": sha256_file(artifact_path), "claim_mapping_sha256": sha256_file(claim_mapping_path)}
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--artifact", required=True)
    p.add_argument("--claim-mapping", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG solver cost and status receipt: " + str(receipt(Path(a.artifact), Path(a.claim_mapping), Path(a.output))))
if __name__ == "__main__":
    main()
