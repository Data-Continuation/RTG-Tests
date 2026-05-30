# RTG Authority-Bound Emission Tests

## Purpose

This document defines the first executable authority-bound emission layer for Relative Transition Geometry.

The goal is to test a stricter rule:

> A transition may be visible, classified, stabilized, and emission-ready, but still not emit unless the observer has the correct authority class for that transition.

This layer connects observer-window behavior, stabilization-emission thresholds, and admissibility authority.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: authority-bound emission
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/authority-bound-emission.valid.json exists
tests/test_authority_bound_emission.py exists
config/rtg_declared_tasks.json declares authority_bound_emission_tests
python tests/test_authority_bound_emission.py passes
python scripts/rtg_dispatcher.py --task authority_bound_emission_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Principle

> Emission authority is not inferred from visibility. It must be explicitly satisfied.

## Provisional Authority Classes

This layer uses the following provisional authority classes:

```text
none
observer
reviewer
maintainer
quorum
root
```

Authority is ordered from weakest to strongest:

```text
none < observer < reviewer < maintainer < quorum < root
```

## Transition Classes

Each transition declares the minimum authority class required for emission.

```text
informational     → observer
classification    → reviewer
repo_change       → maintainer
quarantine        → quorum
root_override     → root
```

## Emission Outcomes

The provisional authority-bound emission outcomes are:

```text
not_visible
not_ready
authority_insufficient
authority_satisfied
overclaimed_authority
```

## Behavior Rules

### not_visible

The transition cannot emit if visibility is below threshold.

### not_ready

The transition cannot emit if stabilization, confidence, evidence, or emission readiness is below threshold.

### authority_insufficient

The transition is visible and ready, but the observer authority class is weaker than the required authority class.

### authority_satisfied

The transition is visible, ready, and authority is sufficient.

### overclaimed_authority

The transition claims emission while authority is insufficient.

## Non-Claim

These tests do not prove final RTG authority mathematics.

They establish the first machine-checkable rule that emission authority must be explicit and cannot be inferred from observation alone.

## Why This Matters

This layer protects RTG from a critical governance failure:

```text
visible ≠ authorized
stable ≠ authorized
confident ≠ authorized
```

It also prepares RTG for commit-time admissibility behavior where a transition can be known, stable, and still unable to affect the ecosystem without the required authority boundary.
