# RTG Transition-Replay Validation Tests

## Purpose

This document defines the first executable transition-replay validation layer for Relative Transition Geometry.

The goal is to test the rule:

```text
A transition claim must be replayable or receipt-consistent before it can be treated as valid state evidence.
```

This layer connects false-transition handling, contradictory receipts, invalid replay, and governed emission.

## Assumptions

```text
Repository: Data-Continuation/RTG-Tests
Formalism: Relative Transition Geometry
Maturity: draft / speculative / provisional executable testing
Layer: transition-replay validation
Dispatcher: repo-local only
```

## Done State

This layer is done when:

```text
fixtures/transition-replay-validation.valid.json exists
tests/test_transition_replay_validation.py exists
config/rtg_declared_tasks.json declares transition_replay_validation_tests
python tests/test_transition_replay_validation.py passes
python scripts/rtg_dispatcher.py --task transition_replay_validation_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Principle

> A transition claim is not valid state evidence merely because it was observed, classified, or emitted.

It must be:

```text
replayable
or
receipt-consistent
```

## Replay States

```text
valid_replay
receipt_consistent
replay_required
receipt_conflict
invalid_replay
unreplayable_provisional
```

## Governance Outputs

```text
valid_replay              → accept_state_evidence
receipt_consistent        → accept_with_receipt_basis
replay_required           → defer_require_replay
receipt_conflict          → quarantine_receipt_conflict
invalid_replay            → reject_invalid_replay
unreplayable_provisional  → mark_provisional_preserve_anomaly
```

## Non-Claim

These tests do not prove final RTG replay mathematics.

They establish the first machine-checkable replay/receipt consistency gate for transition claims.
