# RTG Uncertainty-Class Separation Layer Addendum

## Purpose

This addendum summarizes the uncertainty-class separation layer added after the green authority-bound emission baseline.

## Files Added or Replaced

```text
config/rtg_declared_tasks.json
docs/UNCERTAINTY_CLASS_SEPARATION_TESTS.md
fixtures/uncertainty-classes.valid.json
tests/test_uncertainty_class_separation.py
```

## Dispatcher Task Added

```text
uncertainty_class_separation_tests
```

The task runs:

```bash
python tests/test_uncertainty_class_separation.py
```

## Verification

Run:

```bash
python tests/test_uncertainty_class_separation.py
python scripts/rtg_dispatcher.py --task uncertainty_class_separation_tests
python scripts/rtg_dispatcher.py --task all
```

Expected outputs include:

```text
RTG uncertainty-class separation tests passed.
RTG repo dispatcher completed.
```

## What Changed

Before this layer:

```text
false transitions and unknown unknowns were discussed conceptually
```

After this layer:

```text
false transitions and unknown unknowns are separate executable governance categories
```

## Governance Split

```text
false_transition → block / reject / quarantine / require_replay
unknown_unknown  → defer / lower_confidence / preserve_anomaly / widen_observer_window / mark_provisional
```

## Non-Claim

This layer does not prove RTG.

It creates the first machine-checkable separation between invalid apparent transitions and unmodeled transition-affecting conditions.
