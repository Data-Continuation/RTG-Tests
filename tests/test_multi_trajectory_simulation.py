#!/usr/bin/env python3
"""Validate canonical multi-step RTG simulation and persisted receipt chain."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.multi_trajectory_simulation import canonical_simulation_events, run_canonical_simulation
from engine.receipt_chain import verify_receipt_chain

FIXTURE = ROOT / "fixtures" / "multi-trajectory-simulation.receipts.jsonl"


def main() -> None:
    events = canonical_simulation_events()
    receipts = run_canonical_simulation()
    persisted = [json.loads(line) for line in FIXTURE.read_text(encoding="utf-8").splitlines()]

    assert len(events) == 5
    assert events[0]["significance_class"] == "latent"
    assert events[2]["to"] == "active"
    assert events[3]["event_type"] == "transition_block_formed"
    assert events[4]["event_type"] == "tt_request_emitted"
    assert receipts == persisted, "persisted receipt artifact must match canonical simulation"
    assert verify_receipt_chain(receipts)

    print("Canonical multi-trajectory RTG simulation tests passed.")


if __name__ == "__main__":
    main()
