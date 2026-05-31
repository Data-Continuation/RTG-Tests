# RTG Temporal Window Receipt Decay Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **temporal window receipt decay coherence**.

## Done State

```text
fixtures/temporal-window-receipt-decay-coherence.valid.json exists
tests/test_temporal_window_receipt_decay_coherence.py exists
config/rtg_declared_tasks.json declares temporal_window_receipt_decay_coherence_tests
python tests/test_temporal_window_receipt_decay_coherence.py passes
python scripts/rtg_dispatcher.py --task temporal_window_receipt_decay_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
