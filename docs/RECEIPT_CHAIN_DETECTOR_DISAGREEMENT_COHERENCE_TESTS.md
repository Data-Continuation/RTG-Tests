# RTG Receipt Chain Detector Disagreement Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **receipt chain detector disagreement coherence**.

## Done State

```text
fixtures/receipt-chain-detector-disagreement-coherence.valid.json exists
tests/test_receipt_chain_detector_disagreement_coherence.py exists
config/rtg_declared_tasks.json declares receipt_chain_detector_disagreement_coherence_tests
python tests/test_receipt_chain_detector_disagreement_coherence.py passes
python scripts/rtg_dispatcher.py --task receipt_chain_detector_disagreement_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
