# RTG Quarantine release Tests

## Purpose

This document defines a provisional executable RTG test layer for **quarantine release**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: quarantine release
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/quarantine-release.valid.json exists
tests/test_quarantine_release.py exists
config/rtg_declared_tasks.json declares quarantine_release_tests
python tests/test_quarantine_release.py passes
python scripts/rtg_dispatcher.py --task quarantine_release_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **quarantine release** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
