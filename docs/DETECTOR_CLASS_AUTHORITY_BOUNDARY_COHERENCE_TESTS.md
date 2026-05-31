# RTG Detector Class Authority Boundary Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **detector class authority boundary coherence**.

## Done State

```text
fixtures/detector-class-authority-boundary-coherence.valid.json exists
tests/test_detector_class_authority_boundary_coherence.py exists
config/rtg_declared_tasks.json declares detector_class_authority_boundary_coherence_tests
python tests/test_detector_class_authority_boundary_coherence.py passes
python scripts/rtg_dispatcher.py --task detector_class_authority_boundary_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
