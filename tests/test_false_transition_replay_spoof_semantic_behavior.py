#!/usr/bin/env python3
"""Semantic-differentiation RTG false transition replay spoof semantic behavior hotfix test."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "false-transition-replay-spoof-semantic-behavior.valid.json"

VALID_STATES = ['valid', 'spoof', 'collision', 'replay_spoof', 'overclaim']
STATE_BY_SIGNAL = {1: 'valid', 2: 'spoof', 3: 'collision', 4: 'replay_spoof', 5: 'overclaim'}
EXPECTED_GROUP = "false"

def classify(case):
    signal = case.get("semantic_signal")
    if signal not in STATE_BY_SIGNAL:
        raise AssertionError("unknown semantic signal class: " + repr(signal))
    return STATE_BY_SIGNAL[signal]

def main():
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    if payload.get("layer_type") != "semantic differentiation":
        raise AssertionError("layer_type must be semantic differentiation")

    if payload.get("mechanism_group") != EXPECTED_GROUP:
        raise AssertionError("mechanism_group mismatch")

    valid_states = payload.get("valid_states")
    if not isinstance(valid_states, list) or set(valid_states) != set(VALID_STATES):
        raise AssertionError("valid_states mismatch")

    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise AssertionError("cases must be a non-empty list")

    seen_ids = set()
    seen_states = set()

    for case in cases:
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id:
            raise AssertionError("case_id must be a non-empty string")
        if case_id in seen_ids:
            raise AssertionError("duplicate case_id: " + case_id)
        seen_ids.add(case_id)

        if not isinstance(case.get("semantic_signal"), int):
            raise AssertionError(case_id + " semantic_signal must be integer")

        expected = case.get("expected_state")
        actual = classify(case)
        seen_states.add(expected)

        if actual != expected:
            raise AssertionError(case_id + " expected " + repr(expected) + ", got " + repr(actual))

    missing = set(VALID_STATES) - seen_states
    if missing:
        raise AssertionError("missing states: " + repr(sorted(missing)))

    print("RTG false transition replay spoof semantic behavior tests passed.")

if __name__ == "__main__":
    main()
