# RTG Observer-Window Layer Addendum

## Purpose

This addendum summarizes the observer-window layer added after the green stabilization-emission baseline.

## Files Added or Replaced

```text
config/rtg_declared_tasks.json
docs/OBSERVER_WINDOW_TESTS.md
fixtures/observer-windows.valid.json
tests/test_observer_windows.py
```

## Dispatcher Task Added

```text
observer_window_tests
```

The task runs:

```bash
python tests/test_observer_windows.py
```

## Verification

Run:

```bash
python tests/test_observer_windows.py
python scripts/rtg_dispatcher.py --task observer_window_tests
python scripts/rtg_dispatcher.py --task all
```

Expected outputs include:

```text
RTG observer-window tests passed.
RTG repo dispatcher completed.
```

## What Changed

Before this layer:

```text
observer-window behavior was conceptual
```

After this layer:

```text
observer windows classify visibility, missed transitions, deferred classifications, emittable classifications, and overclaims
```

## Tested Behavior

This layer tests:

```text
missed observations
seen but unclassified observations
classified but deferred observations
classified and emittable observations
overclaimed observations
emission requires authority, confidence, and evidence
```

## Non-Claim

This layer does not prove RTG or inference-window theory.

It creates the first machine-checkable observer-window behavior for RTG.
