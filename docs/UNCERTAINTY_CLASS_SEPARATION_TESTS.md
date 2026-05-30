# RTG Uncertainty-Class Separation Tests

## Purpose

This document defines the first executable uncertainty-class separation layer for Relative Transition Geometry.

The goal is to encode a consequential distinction:

```text
false transition ≠ unknown unknown
```

A false transition is a problem with a transition claim.

An unknown unknown is a limitation of the current observer/model/window.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: uncertainty-class separation
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/uncertainty-classes.valid.json exists
tests/test_uncertainty_class_separation.py exists
config/rtg_declared_tasks.json declares uncertainty_class_separation_tests
python tests/test_uncertainty_class_separation.py passes
python scripts/rtg_dispatcher.py --task uncertainty_class_separation_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Principle

> A false transition is not merely unknown. An unknown unknown is not necessarily false.

## Classes

```text
false_transition
unknown_unknown
```

## False Transition

A false transition is an apparent, claimed, or detected transition that fails governed validity.

Expected governance:

```text
block
reject
quarantine
require_replay
```

## Unknown Unknown

An unknown unknown is an unmodeled or external factor that may affect transition conditions but is not yet visible to the current observer/model/window.

Expected governance:

```text
defer
lower_confidence
preserve_anomaly
widen_observer_window
mark_provisional
```

## Critical Distinction

```text
false_transition = bad or invalid transition claim
unknown_unknown  = model limitation or hidden condition
```

## Prohibited Collapse

The system must not collapse these into one bucket called uncertain.

```text
treating unknown unknowns as false transitions → over-blocks reality
treating false transitions as unknown unknowns → lets invalid state changes slip through
```

## Non-Claim

These tests do not prove final RTG uncertainty mathematics.

They establish the first machine-checkable rule that false-transition handling and unknown-unknown handling must remain separate.
