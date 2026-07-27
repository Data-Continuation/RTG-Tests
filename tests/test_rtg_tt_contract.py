#!/usr/bin/env python3
"""Smoke tests for the bounded RTG to Transition Table request contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "rtg_tt_request.schema.json"
FIXTURE = ROOT / "fixtures" / "rtg-tt-request.example.json"


def main() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    request = json.loads(FIXTURE.read_text(encoding="utf-8"))

    required = set(schema["required"])
    assert required <= set(request), "fixture omits required RTG-TT fields"
    assert request["contract_version"] == "rtg-tt-v0.1"
    assert request["significance_class"] in schema["properties"]["significance_class"]["enum"]
    assert request["requested_resolution"] in schema["properties"]["requested_resolution"]["enum"]
    assert 0 <= request["significance_score"] <= 1
    assert 0 <= request["contextual_threshold"] <= 1
    assert request["significance_score"] >= request["contextual_threshold"]
    assert request["authority_refs"]
    assert request["evidence_refs"]

    effects = request["reachable_state_effects"]
    assert set(effects) == {"opens", "closes", "deformation_magnitude", "irreversible"}
    assert effects["irreversible"] is True
    assert effects["closes"], "irreversible commit fixture must disclose closed paths"
    assert effects["deformation_magnitude"] >= 0.5

    # RTG selects and bounds the candidate; it does not pre-decide TT admissibility.
    forbidden_outputs = {"admissibility_result", "commit_result", "execution_result"}
    assert not (forbidden_outputs & set(request))

    print("RTG to Transition Table contract tests passed.")


if __name__ == "__main__":
    main()
