#!/usr/bin/env python3
"""Semantic-differentiation RTG false transition semantic behavior tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "false-transition-semantic-behavior.valid.json"
VALID_STATES = {'unattributed_claim', 'contradicted_transition', 'spoofed_transition', 'overclaimed_transition', 'valid_transition'}

def classify(c):
    if not c["signature_valid"]:
        return "spoofed_transition"
    if not c["source_known"]:
        return "unattributed_claim"
    if c["contradiction_count"] > 0:
        return "contradicted_transition"
    if c["claim_strength"] >= 0.90 and c["evidence_count"] < 2:
        return "overclaimed_transition"
    return "valid_transition"

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
    print("RTG false transition semantic behavior tests passed.")

if __name__ == "__main__":
    main()
