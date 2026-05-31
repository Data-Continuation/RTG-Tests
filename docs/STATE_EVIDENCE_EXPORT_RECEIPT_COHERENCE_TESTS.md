# RTG State Evidence Export Receipt Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **state evidence export receipt coherence**.

## Done State

```text
fixtures/state-evidence-export-receipt-coherence.valid.json exists
tests/test_state_evidence_export_receipt_coherence.py exists
config/rtg_declared_tasks.json declares state_evidence_export_receipt_coherence_tests
python tests/test_state_evidence_export_receipt_coherence.py passes
python scripts/rtg_dispatcher.py --task state_evidence_export_receipt_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
