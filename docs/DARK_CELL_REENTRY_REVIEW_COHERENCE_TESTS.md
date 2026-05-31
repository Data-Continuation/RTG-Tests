# RTG Dark Cell Reentry Review Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence test for **dark cell reentry review coherence**.

## Done State

```text
fixtures/dark-cell-reentry-review-coherence.valid.json exists
tests/test_dark_cell_reentry_review_coherence.py exists
config/rtg_declared_tasks.json declares dark_cell_reentry_review_coherence_tests
python tests/test_dark_cell_reentry_review_coherence.py passes
python scripts/rtg_dispatcher.py --task dark_cell_reentry_review_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This test checks identity/authority, replay/receipt, lineage/export, risk, confidence, finality gating, and maturity boundary posture.

## Non-Claim

This test does not prove final RTG mathematics.
