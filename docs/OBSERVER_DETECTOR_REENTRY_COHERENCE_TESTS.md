# RTG Observer Detector Reentry Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **observer detector reentry coherence**.

## Done State

```text
fixtures/observer-detector-reentry-coherence.valid.json exists
tests/test_observer_detector_reentry_coherence.py exists
config/rtg_declared_tasks.json declares observer_detector_reentry_coherence_tests
python tests/test_observer_detector_reentry_coherence.py passes
python scripts/rtg_dispatcher.py --task observer_detector_reentry_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
