#!/usr/bin/env python3
"""Semantic-differentiation RTG purpose convergence boundary semantic behavior tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "purpose-convergence-boundary-semantic-behavior.valid.json"
VALID_STATES = {'purpose_aligned', 'purpose_inverting', 'insufficient_protection', 'nonrecoverable_boundary'}

def classify(c):
    if c["recoverability"] < 0.50:
        return "nonrecoverable_boundary"
    if c["harm_reduction"] >= 0.70 and c["target_convergence"] < 0.40 and c["maintenance_cost"] > 0.60:
        return "purpose_inverting"
    if c["harm_reduction"] < 0.50:
        return "insufficient_protection"
    return "purpose_aligned"

def main() -> None:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if payload.get("layer_type") != "semantic differentiation":
        raise AssertionError("layer_type must be semantic differentiation.")
    if set(payload.get("valid_states", [])) != VALID_STATES:
        raise AssertionError("valid_states mismatch.")
    seen_ids = set()
    seen_states = set()
    for case in payload["cases"]:
        case_id = case["case_id"]
        if case_id in seen_ids:
            raise AssertionError(f"duplicate case_id: {case_id}")
        seen_ids.add(case_id)
        expected = case["expected_state"]
        seen_states.add(expected)
        actual = classify(case)
        if actual != expected:
            raise AssertionError(f"{case_id} expected {expected}, got {actual}")
    missing = VALID_STATES - seen_states
    if missing:
        raise AssertionError(f"missing expected states: {sorted(missing)}")
    print("RTG purpose convergence boundary semantic behavior tests passed.")

if __name__ == "__main__":
    main()
