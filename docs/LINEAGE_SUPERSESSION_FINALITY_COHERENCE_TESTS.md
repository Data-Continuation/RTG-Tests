# RTG Lineage Supersession Finality Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **lineage supersession finality coherence**.

## Done State

```text
fixtures/lineage-supersession-finality-coherence.valid.json exists
tests/test_lineage_supersession_finality_coherence.py exists
config/rtg_declared_tasks.json declares lineage_supersession_finality_coherence_tests
python tests/test_lineage_supersession_finality_coherence.py passes
python scripts/rtg_dispatcher.py --task lineage_supersession_finality_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
