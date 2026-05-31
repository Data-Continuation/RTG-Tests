#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "fixtures" / "root-boundary-confidence-floor-coherence.valid.json"
VALID_STATES = {'replay_receipt_block', 'finality_blocked', 'provisional_review', 'coherent', 'quarantine_required', 'identity_authority_block', 'lineage_export_block', 'maturity_boundary'}
def classify(c):
    if c["risk"] > 0.60: return "quarantine_required"
    if not c["identity_authority"]: return "identity_authority_block"
    if not c["replay_receipt"]: return "replay_receipt_block"
    if not c["lineage_export"]: return "lineage_export_block"
    if c["confidence"] < 0.65: return "provisional_review"
    if c["finality_requested"] and not c["finality_allowed"]: return "finality_blocked"
    if not c["maturity_ready"]: return "maturity_boundary"
    return "coherent"
def main():
    p = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert p.get("layer_type") == "cross-layer coherence"
    assert set(p.get("valid_states", [])) == VALID_STATES
    ids, states = set(), set()
    for c in p["cases"]:
        assert c["case_id"] not in ids
        ids.add(c["case_id"])
        for f in ["identity_authority","replay_receipt","lineage_export","finality_requested","finality_allowed","maturity_ready"]:
            assert isinstance(c[f], bool)
        for f in ["risk","confidence"]:
            assert isinstance(c[f], (int, float)) and 0 <= c[f] <= 1
        states.add(c["expected_state"])
        assert classify(c) == c["expected_state"]
    assert VALID_STATES <= states
    print("RTG root boundary confidence floor coherence tests passed.")
if __name__ == "__main__":
    main()
