#!/usr/bin/env python3
"""Semantic-differentiation RTG confidence regrade semantic behavior tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "confidence-regrade-semantic-behavior.valid.json"
VALID_STATES = {'defer', 'source_drift_review', 'upgrade', 'downgrade', 'maintain'}

def classify(c):
    if c["source_drift"] > 0.35:
        return "source_drift_review"
    if c["detector_quality"] < 0.50:
        return "defer"
    if c["contradictions"] >= 1:
        return "downgrade"
    if c["corroboration"] >= 2 and c["base_confidence"] < 0.70:
        return "upgrade"
    return "maintain"

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
    print("RTG confidence regrade semantic behavior tests passed.")

if __name__ == "__main__":
    main()
