
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
def materialize(handoff_receipt_path: Path, ingestion_path: Path, claim_confirmation_path: Path, cost_confirmation_path: Path, output_path: Path) -> Path:
    claim = load_structured(claim_confirmation_path)
    cost = load_structured(cost_confirmation_path)
    ok = claim.get("claim_boundary_confirmed") and cost.get("cost_status_confirmed")
    return write_json(output_path, {
        "schema_version": "1.0",
        "generated": utc_now(),
        "audit_surface": "rtg_returned_round_trip_audit_record",
        "round_trip_status": "round_trip_complete" if ok else "round_trip_review_required",
        "handoff_receipt_sha256": sha256_file(handoff_receipt_path),
        "ingestion_sha256": sha256_file(ingestion_path),
        "claim_confirmation_sha256": sha256_file(claim_confirmation_path),
        "cost_confirmation_sha256": sha256_file(cost_confirmation_path),
        "audit_summary": {
            "claim_boundary_confirmed": claim.get("claim_boundary_confirmed"),
            "cost_status_confirmed": cost.get("cost_status_confirmed")
        }
    })
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--handoff-receipt", required=True)
    p.add_argument("--ingestion", required=True)
    p.add_argument("--claim-confirmation", required=True)
    p.add_argument("--cost-confirmation", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote returned round-trip audit: " + str(materialize(Path(a.handoff_receipt), Path(a.ingestion), Path(a.claim_confirmation), Path(a.cost_confirmation), Path(a.output))))
if __name__ == "__main__":
    main()
