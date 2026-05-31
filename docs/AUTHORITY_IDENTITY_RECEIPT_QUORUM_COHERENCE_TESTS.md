# RTG Authority Identity Receipt Quorum Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **authority identity receipt quorum coherence**.

## Done State

```text
fixtures/authority-identity-receipt-quorum-coherence.valid.json exists
tests/test_authority_identity_receipt_quorum_coherence.py exists
config/rtg_declared_tasks.json declares authority_identity_receipt_quorum_coherence_tests
python tests/test_authority_identity_receipt_quorum_coherence.py passes
python scripts/rtg_dispatcher.py --task authority_identity_receipt_quorum_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
