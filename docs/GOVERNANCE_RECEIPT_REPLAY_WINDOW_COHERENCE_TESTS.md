# RTG Governance Receipt Replay Window Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **governance receipt replay window coherence**.

## Done State

```text
fixtures/governance-receipt-replay-window-coherence.valid.json exists
tests/test_governance_receipt_replay_window_coherence.py exists
config/rtg_declared_tasks.json declares governance_receipt_replay_window_coherence_tests
python tests/test_governance_receipt_replay_window_coherence.py passes
python scripts/rtg_dispatcher.py --task governance_receipt_replay_window_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
