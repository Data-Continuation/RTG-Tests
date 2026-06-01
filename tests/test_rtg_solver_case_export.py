#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "export_rtg_solver_cases.py"
SCHEMA = ROOT / "schemas" / "rtg_solver_case.schema.json"
OUTPUT = ROOT / "build" / "solver-cases-test"

def require(ok, msg):
    if not ok:
        raise AssertionError(msg)

def main():
    require(SCRIPT.exists(), "export script is missing")
    require(SCHEMA.exists(), "solver case schema is missing")
    require((ROOT / "fixtures").exists(), "fixtures directory is missing")
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    result = subprocess.run([sys.executable, str(SCRIPT), "--output-dir", str(OUTPUT)], cwd=str(ROOT), text=True, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(result.stdout + result.stderr)
    exported = sorted(OUTPUT.glob("*.json"))
    require(exported, "no solver cases were exported")
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    sample = json.loads(exported[0].read_text(encoding="utf-8"))
    missing = set(schema["required"]) - set(sample)
    require(not missing, "missing required fields: " + repr(sorted(missing)))
    require(sample["expected_solver_posture"] in schema["properties"]["expected_solver_posture"]["enum"], "bad solver posture")
    require(sample["export_posture"] in schema["properties"]["export_posture"]["enum"], "bad export posture")
    require(sample["rtg_mechanism"]["layer_type"] == "semantic differentiation", "wrong layer type")
    require(isinstance(sample["constraints"], list) and sample["constraints"], "constraints missing")
    print("RTG math solver bridge export tests passed.")

if __name__ == "__main__":
    main()
