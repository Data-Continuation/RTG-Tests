# RTG Packet Hash Confidence Regrade Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **packet hash confidence regrade coherence**.

## Done State

```text
fixtures/packet-hash-confidence-regrade-coherence.valid.json exists
tests/test_packet_hash_confidence_regrade_coherence.py exists
config/rtg_declared_tasks.json declares packet_hash_confidence_regrade_coherence_tests
python tests/test_packet_hash_confidence_regrade_coherence.py passes
python scripts/rtg_dispatcher.py --task packet_hash_confidence_regrade_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
