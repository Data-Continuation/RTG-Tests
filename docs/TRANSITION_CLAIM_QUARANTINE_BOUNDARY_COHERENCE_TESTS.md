# RTG Transition Claim Quarantine Boundary Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **transition claim quarantine boundary coherence**.

## Done State

```text
fixtures/transition-claim-quarantine-boundary-coherence.valid.json exists
tests/test_transition_claim_quarantine_boundary_coherence.py exists
config/rtg_declared_tasks.json declares transition_claim_quarantine_boundary_coherence_tests
python tests/test_transition_claim_quarantine_boundary_coherence.py passes
python scripts/rtg_dispatcher.py --task transition_claim_quarantine_boundary_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
