# RTG Multi Observer Authority Decay Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **multi observer authority decay coherence**.

## Done State

```text
fixtures/multi-observer-authority-decay-coherence.valid.json exists
tests/test_multi_observer_authority_decay_coherence.py exists
config/rtg_declared_tasks.json declares multi_observer_authority_decay_coherence_tests
python tests/test_multi_observer_authority_decay_coherence.py passes
python scripts/rtg_dispatcher.py --task multi_observer_authority_decay_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
