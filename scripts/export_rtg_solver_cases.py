#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTURES = {"satisfiable","contradictory","underconstrained","overconstrained","equivalent_to_prior_case","requires_new_axiom_or_operator"}

def signal(case):
    value = case.get("semantic_signal", case.get("signal", 0))
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError("case signal must be an integer")
    return value

def bounded_number(case, key, default):
    value = case.get(key, default)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        value = default
    return max(0.0, min(1.0, float(value)))

def infer_posture(payload, case):
    states = set(payload.get("valid_states", []))
    expected = case.get("expected_state")
    if expected is None:
        return "underconstrained"
    if states and expected not in states:
        return "contradictory"
    return "satisfiable"

def solver_case(source_fixture, payload, case):
    posture = infer_posture(payload, case)
    return {
        "schema_version": "1.0",
        "case_id": case.get("case_id", f"{payload.get('test_key','rtg')}-case"),
        "source_fixture": source_fixture.as_posix(),
        "rtg_mechanism": {
            "test_key": payload.get("test_key", "unknown"),
            "mechanism_group": payload.get("mechanism_group", "unknown"),
            "layer_type": payload.get("layer_type", "unknown"),
            "maturity": payload.get("maturity", "unknown")
        },
        "formal_variables": {
            "state": case.get("expected_state", "unknown"),
            "signal": signal(case),
            "confidence": bounded_number(case, "confidence", 0.5),
            "risk": bounded_number(case, "risk", 0.5)
        },
        "constraints": [
            {"name":"state_membership","operator":"in","value":payload.get("valid_states", [])},
            {"name":"mechanism_group","operator":"equals","value":payload.get("mechanism_group", "unknown")},
            {"name":"layer_type","operator":"equals","value":payload.get("layer_type", "unknown")},
            {"name":"export_surface","operator":"equals","value":"semantic_fixture"}
        ],
        "expected_solver_posture": posture,
        "export_posture": "ready_for_solver" if posture in POSTURES else "needs_review"
    }

def safe_name(text):
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in text).strip("-") or "solver-case"

def export_solver_cases(fixture_dir, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for fixture in sorted(fixture_dir.glob("*.valid.json")):
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        if payload.get("layer_type") != "semantic differentiation":
            continue
        for i, case in enumerate(payload.get("cases", []), 1):
            item = solver_case(fixture.relative_to(ROOT), payload, case)
            path = output_dir / f"{safe_name(item['case_id'])}-{i:03d}.json"
            path.write_text(json.dumps(item, indent=2) + "\n", encoding="utf-8")
            written.append(path)
    return written

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture-dir", default=str(ROOT / "fixtures"))
    parser.add_argument("--output-dir", default=str(ROOT / "build" / "solver-cases"))
    args = parser.parse_args()
    written = export_solver_cases(Path(args.fixture_dir), Path(args.output_dir))
    print(f"Exported {len(written)} RTG solver cases.")

if __name__ == "__main__":
    main()
