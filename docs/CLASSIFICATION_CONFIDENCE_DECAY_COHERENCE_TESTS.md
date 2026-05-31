# RTG Classification Confidence Decay Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **classification confidence decay coherence**.

## Done State

```text
fixtures/classification-confidence-decay-coherence.valid.json exists
tests/test_classification_confidence_decay_coherence.py exists
config/rtg_declared_tasks.json declares classification_confidence_decay_coherence_tests
python tests/test_classification_confidence_decay_coherence.py passes
python scripts/rtg_dispatcher.py --task classification_confidence_decay_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
