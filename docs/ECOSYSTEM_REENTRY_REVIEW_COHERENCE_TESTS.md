# RTG Ecosystem Reentry Review Coherence Tests

## Purpose

This document defines a provisional executable RTG cross-layer coherence task for **ecosystem reentry review coherence**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer type: cross-layer coherence next-31
Layer: ecosystem reentry review coherence
Dispatcher: repo-local only
```

## Done State

```text
fixtures/ecosystem-reentry-review-coherence.valid.json exists
tests/test_ecosystem_reentry_review_coherence.py exists
config/rtg_declared_tasks.json declares ecosystem_reentry_review_coherence_tests
python tests/test_ecosystem_reentry_review_coherence.py passes
python scripts/rtg_dispatcher.py --task ecosystem_reentry_review_coherence_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This task verifies that authority, lineage, replay, risk, and a task-specific secondary condition remain coherent as a combined transition packet.

## Non-Claim

This task does not prove final RTG mathematics. It adds one provisional executable coherence constraint that can be revised as the formalism matures.
