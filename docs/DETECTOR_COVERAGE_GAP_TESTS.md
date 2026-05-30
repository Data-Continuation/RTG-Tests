# RTG Detector coverage gap Tests

## Purpose

This document defines a provisional executable RTG test layer for **detector coverage gap**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: detector coverage gap
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/detector-coverage-gap.valid.json exists
tests/test_detector_coverage_gap.py exists
config/rtg_declared_tasks.json declares detector_coverage_gap_tests
python tests/test_detector_coverage_gap.py passes
python scripts/rtg_dispatcher.py --task detector_coverage_gap_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **detector coverage gap** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
