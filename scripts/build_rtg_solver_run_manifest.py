#!/usr/bin/env python3
"""Build an RTG math-solver run manifest from exported solver cases."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASE_DIR = ROOT / "build" / "solver-cases"
DEFAULT_OUTPUT_DIR = ROOT / "build" / "solver-runs"
DEFAULT_CONFIG = ROOT / "config" / "rtg_math_solver_adapter.json"

def load_config(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "schema_version": "1.0",
        "source_repo": "Data-Continuation/RTG-Tests",
        "target_workflow_reference": "GCAT-BCAT-Engine/workflows/math-solver",
        "solver_case_schema": "schemas/rtg_solver_case.schema.json",
        "solver_run_manifest_schema": "schemas/rtg_solver_run_manifest.schema.json",
        "expected_outputs": {
            "solver_results_json": "build/solver-results/solver_results.json",
            "solver_summary_json": "build/solver-results/solver_summary.json",
            "formal_posture_json": "build/solver-results/rtg_formal_posture.json",
        },
    }

def stable_run_id(cases: list[dict]) -> str:
    count = len(cases)
    first = cases[0]["case_id"] if cases else "empty"
    last = cases[-1]["case_id"] if cases else "empty"
    def safe(text: str) -> str:
        return "".join(ch.lower() if ch.isalnum() else "-" for ch in text).strip("-") or "case"
    return f"rtg-solver-run-{count}-{safe(first)[:24]}-{safe(last)[:24]}"

def build_manifest(case_dir: Path, output_dir: Path, config_path: Path) -> Path:
    config = load_config(config_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    cases = []
    for path in sorted(case_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        cases.append({
            "case_path": str(path.as_posix()),
            "case_id": payload.get("case_id", path.stem),
            "expected_solver_posture": payload.get("expected_solver_posture", "underconstrained"),
            "export_posture": payload.get("export_posture", "needs_review"),
            "mechanism_group": payload.get("rtg_mechanism", {}).get("mechanism_group", "unknown"),
        })

    manifest = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "run_id": stable_run_id(cases),
        "source_repo": config.get("source_repo", "Data-Continuation/RTG-Tests"),
        "target_workflow_reference": config.get("target_workflow_reference", "GCAT-BCAT-Engine/workflows/math-solver"),
        "solver_case_schema": config.get("solver_case_schema", "schemas/rtg_solver_case.schema.json"),
        "solver_run_manifest_schema": config.get("solver_run_manifest_schema", "schemas/rtg_solver_run_manifest.schema.json"),
        "input_cases": cases,
        "expected_outputs": config.get("expected_outputs", {}),
        "adapter_posture": "ready_for_workflow" if cases else "blocked",
    }
    out_path = output_dir / "rtg_solver_run_manifest.json"
    out_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return out_path

def main() -> None:
    parser = argparse.ArgumentParser(description="Build RTG math-solver run manifest.")
    parser.add_argument("--case-dir", default=str(DEFAULT_CASE_DIR))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()
    manifest = build_manifest(Path(args.case_dir), Path(args.output_dir), Path(args.config))
    print("Wrote RTG solver run manifest: " + str(manifest))

if __name__ == "__main__":
    main()
