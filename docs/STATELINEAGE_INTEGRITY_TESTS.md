# RTG State-lineage integrity Tests

## Purpose

This document defines a provisional executable RTG test layer for **state-lineage integrity**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: state-lineage integrity
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/state-lineage-integrity.valid.json exists
tests/test_state_lineage_integrity.py exists
config/rtg_declared_tasks.json declares state_lineage_integrity_tests
python tests/test_state_lineage_integrity.py passes
python scripts/rtg_dispatcher.py --task state_lineage_integrity_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **state-lineage integrity** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
