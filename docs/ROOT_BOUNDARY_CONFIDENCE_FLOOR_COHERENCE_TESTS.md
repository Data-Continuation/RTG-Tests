# RTG Root Boundary Confidence Floor Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **root boundary confidence floor coherence**.

## Done State

```text
fixtures/root-boundary-confidence-floor-coherence.valid.json exists
tests/test_root_boundary_confidence_floor_coherence.py exists
config/rtg_declared_tasks.json declares root_boundary_confidence_floor_coherence_tests
python tests/test_root_boundary_confidence_floor_coherence.py passes
python scripts/rtg_dispatcher.py --task root_boundary_confidence_floor_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
