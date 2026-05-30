# RTG Confidence regrade Tests

## Purpose

This document defines a provisional executable RTG test layer for **confidence regrade**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: confidence regrade
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/confidence-regrade.valid.json exists
tests/test_confidence_regrade.py exists
config/rtg_declared_tasks.json declares confidence_regrade_tests
python tests/test_confidence_regrade.py passes
python scripts/rtg_dispatcher.py --task confidence_regrade_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **confidence regrade** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
