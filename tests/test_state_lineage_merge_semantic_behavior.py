#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "state-lineage-merge-semantic-behavior.valid.json"
VALID_STATES = {'invalid_merge', 'linear', 'merge_review', 'orphan'}
STATE_BY_SIGNAL = {1: 'linear', 2: 'orphan', 3: 'merge_review', 4: 'invalid_merge'}
def classify(case):
    signal = case["semantic_signal"]
    if signal not in STATE_BY_SIGNAL:
        raise AssertionError(f"unknown semantic signal class: {signal}")
    return STATE_BY_SIGNAL[signal]
def main():
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    if payload.get("layer_type") != "semantic differentiation":
        raise AssertionError("layer_type must be semantic differentiation")
    if payload.get("mechanism_group") != "state":
        raise AssertionError("mechanism_group mismatch")
    if set(payload.get("valid_states", [])) != VALID_STATES:
        raise AssertionError("valid_states mismatch")
    ids, seen = set(), set()
    for case in payload["cases"]:
        if case["case_id"] in ids:
            raise AssertionError("duplicate case_id")
        ids.add(case["case_id"])
        if not isinstance(case["semantic_signal"], int):
            raise AssertionError("semantic_signal must be integer")
        if not 0 <= case["risk"] <= 1 or not 0 <= case["confidence"] <= 1:
            raise AssertionError("risk/confidence out of range")
        actual, expected = classify(case), case["expected_state"]
        seen.add(expected)
        if actual != expected:
            raise AssertionError(f"{case['case_id']} expected {expected}, got {actual}")
    missing = VALID_STATES - seen
    if missing:
        raise AssertionError(f"missing states: {sorted(missing)}")
    print("RTG state lineage merge semantic behavior tests passed.")
if __name__ == "__main__":
    main()
