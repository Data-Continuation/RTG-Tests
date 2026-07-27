#!/usr/bin/env python3
"""Tests for deterministic chained RTG geometry-deformation receipts."""

from __future__ import annotations

import json
from copy import deepcopy

from engine.receipt_chain import build_receipt_chain, receipts_to_jsonl, verify_receipt_chain


def main() -> None:
    payloads = [
        {
            "event_id": "rtg-event-001",
            "event_type": "candidate_observed",
            "transition_id": "tau-commit-route-b",
            "significance_class": "latent",
        },
        {
            "event_id": "rtg-event-002",
            "event_type": "context_deformed",
            "transition_id": "tau-commit-route-b",
            "significance_class": "active",
            "cause": "risk_threshold_reduction",
        },
        {
            "event_id": "rtg-event-003",
            "event_type": "tt_request_emitted",
            "transition_id": "tau-commit-route-b",
            "request_id": "rtgtt-0001",
        },
    ]

    first = build_receipt_chain(payloads)
    replay = build_receipt_chain(payloads)

    assert first == replay, "identical payload sequences must replay identically"
    assert len(first) == len(payloads)
    assert verify_receipt_chain(first)
    assert first[1]["previous_hash"] == first[0]["receipt_hash"]
    assert first[2]["previous_hash"] == first[1]["receipt_hash"]

    jsonl = receipts_to_jsonl(first)
    decoded = [json.loads(line) for line in jsonl.splitlines()]
    assert decoded == first

    tampered = deepcopy(first)
    tampered[1]["canonical_payload"] = tampered[1]["canonical_payload"].replace("active", "latent")
    assert not verify_receipt_chain(tampered), "tampered receipt chain must fail"

    reordered = [first[1], first[0], first[2]]
    assert not verify_receipt_chain(reordered), "reordered receipt chain must fail"

    print("Multi-trajectory RTG receipt-chain tests passed.")


if __name__ == "__main__":
    main()
