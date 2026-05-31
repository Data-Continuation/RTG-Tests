# RTG False Transition Lineage Repair Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **false transition lineage repair coherence**.

## Done State

```text
fixtures/false-transition-lineage-repair-coherence.valid.json exists
tests/test_false_transition_lineage_repair_coherence.py exists
config/rtg_declared_tasks.json declares false_transition_lineage_repair_coherence_tests
python tests/test_false_transition_lineage_repair_coherence.py passes
python scripts/rtg_dispatcher.py --task false_transition_lineage_repair_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
