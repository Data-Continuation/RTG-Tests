# RTG Consensus Failure Quarantine Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **consensus failure quarantine coherence**.

## Done State

```text
fixtures/consensus-failure-quarantine-coherence.valid.json exists
tests/test_consensus_failure_quarantine_coherence.py exists
config/rtg_declared_tasks.json declares consensus_failure_quarantine_coherence_tests
python tests/test_consensus_failure_quarantine_coherence.py passes
python scripts/rtg_dispatcher.py --task consensus_failure_quarantine_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
