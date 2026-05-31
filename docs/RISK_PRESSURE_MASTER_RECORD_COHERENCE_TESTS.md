# RTG Risk Pressure Master Record Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **risk pressure master record coherence**.

## Done State

```text
fixtures/risk-pressure-master-record-coherence.valid.json exists
tests/test_risk_pressure_master_record_coherence.py exists
config/rtg_declared_tasks.json declares risk_pressure_master_record_coherence_tests
python tests/test_risk_pressure_master_record_coherence.py passes
python scripts/rtg_dispatcher.py --task risk_pressure_master_record_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
