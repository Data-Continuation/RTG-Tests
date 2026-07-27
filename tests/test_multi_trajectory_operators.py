#!/usr/bin/env python3
"""Deterministic tests for provisional multi-trajectory RTG operators."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.multi_trajectory_ops import (
    compression_is_decision_preserving,
    constellation_activation,
    deterministic_receipt,
    relational_density,
    transition_block_state,
)

FIXTURE = ROOT / "fixtures" / "multi-trajectory-operators.example.json"


class MultiTrajectoryOperatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_relational_density_drives_block_formation(self) -> None:
        block = self.data["block"]
        density = relational_density(block["nodes"], block["couplings"])
        self.assertAlmostEqual(density, 4 / 6)

        state = transition_block_state(
            block["nodes"],
            block["couplings"],
            block["formation_threshold"],
            current_coupling_minimum=block["current_coupling_minimum"],
        )
        self.assertTrue(state["formed"])
        self.assertFalse(state["dissolved"])
        self.assertEqual(state["reason"], "formed")

    def test_goal_resolution_dissolves_block(self) -> None:
        block = self.data["block"]
        state = transition_block_state(
            block["nodes"],
            block["couplings"],
            block["formation_threshold"],
            goal_resolved=True,
            current_coupling_minimum=block["current_coupling_minimum"],
        )
        self.assertFalse(state["formed"])
        self.assertTrue(state["dissolved"])
        self.assertEqual(state["reason"], "goal_resolved")

    def test_constellation_can_activate_from_subthreshold_members(self) -> None:
        constellation = self.data["constellation"]
        result = constellation_activation(
            constellation["member_scores"],
            constellation["member_weights"],
            constellation["threshold"],
        )
        self.assertTrue(result["individually_subthreshold"])
        self.assertTrue(result["activated"])
        self.assertGreaterEqual(result["aggregate"], constellation["threshold"])

    def test_compression_must_preserve_decisions(self) -> None:
        compression = self.data["compression"]
        self.assertTrue(
            compression_is_decision_preserving(
                compression["original_decisions"],
                compression["preserving_compressed_decisions"],
            )
        )
        self.assertFalse(
            compression_is_decision_preserving(
                compression["original_decisions"],
                compression["destructive_compressed_decisions"],
            )
        )

    def test_receipts_are_deterministic_and_replayable(self) -> None:
        payload = self.data["receipt_payload"]
        first = deterministic_receipt(payload)
        second = deterministic_receipt(dict(reversed(list(payload.items()))))
        self.assertEqual(first, second)
        self.assertEqual(len(first["receipt_hash"]), 64)
        self.assertEqual(first["hash_algorithm"], "sha256")


if __name__ == "__main__":
    unittest.main()
