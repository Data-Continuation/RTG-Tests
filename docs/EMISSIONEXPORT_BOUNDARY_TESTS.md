# RTG Emission-export boundary Tests

## Purpose

This document defines a provisional executable RTG test layer for **emission-export boundary**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: emission-export boundary
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/emission-export-boundary.valid.json exists
tests/test_emission_export_boundary.py exists
config/rtg_declared_tasks.json declares emission_export_boundary_tests
python tests/test_emission_export_boundary.py passes
python scripts/rtg_dispatcher.py --task emission_export_boundary_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **emission-export boundary** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
