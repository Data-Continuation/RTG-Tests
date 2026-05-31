# RTG Semantic Claim Receipt Density Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **semantic claim receipt density coherence**.

## Done State

```text
fixtures/semantic-claim-receipt-density-coherence.valid.json exists
tests/test_semantic_claim_receipt_density_coherence.py exists
config/rtg_declared_tasks.json declares semantic_claim_receipt_density_coherence_tests
python tests/test_semantic_claim_receipt_density_coherence.py passes
python scripts/rtg_dispatcher.py --task semantic_claim_receipt_density_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
