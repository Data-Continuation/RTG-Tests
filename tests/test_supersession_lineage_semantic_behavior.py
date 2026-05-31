#!/usr/bin/env python3
"""Semantic-differentiation RTG supersession lineage semantic behavior tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "supersession-lineage-semantic-behavior.valid.json"
VALID_STATES = {'authority_conflict', 'stale_update', 'supersede', 'weak_receipt', 'fork_detected'}

def classify(c):
    if not c["same_parent"]:
        return "fork_detected"
    if not c["newer"]:
        return "stale_update"
    if c["authority_conflict"]:
        return "authority_conflict"
    if c["receipt_strength_delta"] <= 0:
        return "weak_receipt"
    return "supersede"

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
    print("RTG supersession lineage semantic behavior tests passed.")

if __name__ == "__main__":
    main()
