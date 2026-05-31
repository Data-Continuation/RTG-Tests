# RTG Stabilization Detector Authority Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **stabilization detector authority coherence**.

## Done State

```text
fixtures/stabilization-detector-authority-coherence.valid.json exists
tests/test_stabilization_detector_authority_coherence.py exists
config/rtg_declared_tasks.json declares stabilization_detector_authority_coherence_tests
python tests/test_stabilization_detector_authority_coherence.py passes
python scripts/rtg_dispatcher.py --task stabilization_detector_authority_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
