# RTG Cell Geometry Detector Upgrade Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **cell geometry detector upgrade coherence**.

## Done State

```text
fixtures/cell-geometry-detector-upgrade-coherence.valid.json exists
tests/test_cell_geometry_detector_upgrade_coherence.py exists
config/rtg_declared_tasks.json declares cell_geometry_detector_upgrade_coherence_tests
python tests/test_cell_geometry_detector_upgrade_coherence.py passes
python scripts/rtg_dispatcher.py --task cell_geometry_detector_upgrade_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
