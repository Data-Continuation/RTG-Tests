# RTG Supersession ordering Tests

## Purpose

This document defines a provisional executable RTG test layer for **supersession ordering**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: supersession ordering
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/supersession-ordering.valid.json exists
tests/test_supersession_ordering.py exists
config/rtg_declared_tasks.json declares supersession_ordering_tests
python tests/test_supersession_ordering.py passes
python scripts/rtg_dispatcher.py --task supersession_ordering_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **supersession ordering** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
