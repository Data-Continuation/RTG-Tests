"""Canonical deterministic multi-step RTG trajectory simulation."""

from __future__ import annotations

from typing import Any

from engine.receipt_chain import build_receipt_chain


def canonical_simulation_events() -> list[dict[str, Any]]:
    return [
        {
            "event_id": "rtg-sim-001",
            "event_type": "candidate_observed",
            "transition_id": "tau-route-b",
            "significance_class": "latent",
            "score": 0.54,
        },
        {
            "event_id": "rtg-sim-002",
            "event_type": "context_deformed",
            "transition_id": "tau-route-b",
            "risk": 0.82,
            "threshold": 0.50,
        },
        {
            "event_id": "rtg-sim-003",
            "event_type": "candidate_reclassified",
            "transition_id": "tau-route-b",
            "from": "latent",
            "to": "active",
            "score": 0.74,
        },
        {
            "event_id": "rtg-sim-004",
            "event_type": "transition_block_formed",
            "block_id": "block-route-17",
            "density": 0.666666666667,
        },
        {
            "event_id": "rtg-sim-005",
            "event_type": "tt_request_emitted",
            "request_id": "rtgtt-0001",
            "transition_id": "tau-route-b",
            "requested_resolution": "commit",
        },
    ]


def run_canonical_simulation() -> list[dict[str, Any]]:
    return build_receipt_chain(canonical_simulation_events())
