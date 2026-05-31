# RTG Identity Surface Anomaly Retention Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **identity surface anomaly retention coherence**.

## Done State

```text
fixtures/identity-surface-anomaly-retention-coherence.valid.json exists
tests/test_identity_surface_anomaly_retention_coherence.py exists
config/rtg_declared_tasks.json declares identity_surface_anomaly_retention_coherence_tests
python tests/test_identity_surface_anomaly_retention_coherence.py passes
python scripts/rtg_dispatcher.py --task identity_surface_anomaly_retention_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
