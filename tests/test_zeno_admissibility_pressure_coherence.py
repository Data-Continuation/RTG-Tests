#!/usr/bin/env python3
"""Provisional RTG zeno admissibility pressure coherence tests."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "zeno-admissibility-pressure-coherence.valid.json"

VALID_STATES = {'observation_block', 'finality_blocked', 'provisional_review', 'coherent', 'authority_block', 'quarantine_required', 'lineage_export_block', 'receipt_replay_block', 'maturity_boundary'}

def classify(case):
    if case["risk"] > 0.60:
        return "quarantine_required"
    if not case["observer_compatible"]:
        return "observation_block"
    if not case["authority_valid"]:
        return "authority_block"
    if not case["receipt_replay_valid"]:
        return "receipt_replay_block"
    if not case["lineage_export_valid"]:
        return "lineage_export_block"
    if case["confidence"] < 0.65:
        return "provisional_review"
    if case["finality_requested"] and not case["finality_allowed"]:
        return "finality_blocked"
    if not case["maturity_ready"]:
        return "maturity_boundary"
    return "coherent"

def main():
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if payload.get("layer_type") != "cross-layer coherence":
        raise AssertionError("layer_type must be cross-layer coherence")
    if set(payload.get("valid_states", [])) != VALID_STATES:
        raise AssertionError("valid_states mismatch")
    ids, states = set(), set()
    for case in payload["cases"]:
        if case["case_id"] in ids:
            raise AssertionError("duplicate case_id")
        ids.add(case["case_id"])
        for field in ["observer_compatible", "authority_valid", "receipt_replay_valid", "lineage_export_valid", "finality_requested", "finality_allowed", "maturity_ready"]:
            if not isinstance(case[field], bool):
                raise AssertionError(f"{field} must be boolean")
        for field in ["risk", "confidence"]:
            if not isinstance(case[field], (int, float)) or not 0 <= case[field] <= 1:
                raise AssertionError(f"{field} out of range")
        states.add(case["expected_state"])
        actual = classify(case)
        if actual != case["expected_state"]:
            raise AssertionError(f"{case['case_id']} expected {case['expected_state']}, got {actual}")
    missing = VALID_STATES - states
    if missing:
        raise AssertionError(f"missing states: {sorted(missing)}")
    print("RTG zeno admissibility pressure coherence tests passed.")

if __name__ == "__main__":
    main()
