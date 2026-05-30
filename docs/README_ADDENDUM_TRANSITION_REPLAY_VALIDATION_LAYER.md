# RTG Transition-Replay Validation Layer Addendum

## Purpose

This addendum summarizes the transition-replay validation layer added after the green observer-identity coupling baseline.

## Files Added or Replaced

```text
config/rtg_declared_tasks.json
docs/TRANSITION_REPLAY_VALIDATION_TESTS.md
fixtures/transition-replay-validation.valid.json
tests/test_transition_replay_validation.py
```

## Dispatcher Task Added

```text
transition_replay_validation_tests
```

The task runs:

```bash
python tests/test_transition_replay_validation.py
```

## Verification

Run:

```bash
python tests/test_transition_replay_validation.py
python scripts/rtg_dispatcher.py --task transition_replay_validation_tests
python scripts/rtg_dispatcher.py --task all
```

Expected outputs include:

```text
RTG transition-replay validation tests passed.
RTG repo dispatcher completed.
```

## Governance Split

```text
valid_replay              → accept_state_evidence
receipt_consistent        → accept_with_receipt_basis
replay_required           → defer_require_replay
receipt_conflict          → quarantine_receipt_conflict
invalid_replay            → reject_invalid_replay
unreplayable_provisional  → mark_provisional_preserve_anomaly
```

## Non-Claim

This layer does not prove RTG.

It creates the first machine-checkable replay/receipt consistency gate for transition claims.
