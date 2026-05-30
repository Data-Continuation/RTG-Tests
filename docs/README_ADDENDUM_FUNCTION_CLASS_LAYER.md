# RTG Function-Class Layer Addendum

## Purpose

This addendum summarizes the function-class behavior layer added after the green cell-geometry baseline.

## Files Added or Replaced

```text
config/rtg_declared_tasks.json
docs/FUNCTION_CLASS_BEHAVIOR.md
fixtures/function-classes.valid.json
tests/test_function_classes.py
```

## Dispatcher Task Added

```text
function_class_behavior_tests
```

The task runs:

```bash
python tests/test_function_classes.py
```

## Verification

Run:

```bash
python tests/test_function_classes.py
python scripts/rtg_dispatcher.py --task function_class_behavior_tests
python scripts/rtg_dispatcher.py --task all
```

Expected outputs include:

```text
RTG function-class behavior tests passed.
RTG repo dispatcher completed.
```

## What Changed

Before this layer:

```text
function_class existed as a label
```

After this layer:

```text
function_class carries provisional executable behavior
```

This is now beyond pure scaffolding.

It remains provisional and not proof-complete.

## Behavior Classes Covered

```text
bounded
slow_growth
steep_growth
singular
dampening
amplifying
bridging
barrier
resonant
```

## Non-Claim

This layer does not prove RTG.

It creates the first machine-checkable behavior profile for RTG function classes.
