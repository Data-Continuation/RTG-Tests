# RTG Quarantine Release Export Boundary Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **quarantine release export boundary coherence**.

## Done State

```text
fixtures/quarantine-release-export-boundary-coherence.valid.json exists
tests/test_quarantine_release_export_boundary_coherence.py exists
config/rtg_declared_tasks.json declares quarantine_release_export_boundary_coherence_tests
python tests/test_quarantine_release_export_boundary_coherence.py passes
python scripts/rtg_dispatcher.py --task quarantine_release_export_boundary_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
