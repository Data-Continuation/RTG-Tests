# RTG Governance-output consistency Tests

## Purpose

This document defines a provisional executable RTG test layer for **governance-output consistency**.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: governance-output consistency
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/governance-output-consistency.valid.json exists
tests/test_governance_output_consistency.py exists
config/rtg_declared_tasks.json declares governance_output_consistency_tests
python tests/test_governance_output_consistency.py passes
python scripts/rtg_dispatcher.py --task governance_output_consistency_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This layer makes **governance-output consistency** machine-checkable rather than merely conceptual.

## Non-Claim

This test does not prove RTG.

It adds a provisional executable constraint that can be revised as the formalism matures.
