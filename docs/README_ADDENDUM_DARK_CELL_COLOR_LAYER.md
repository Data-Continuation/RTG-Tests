# RTG Dark-Cell Color Layer Addendum

## Purpose

This addendum summarizes the dark-cell color emergence layer added after the green shell-role expectation baseline.

## Files Added or Replaced

```text
config/rtg_declared_tasks.json
docs/DARK_CELL_COLOR_EMERGENCE_TESTS.md
fixtures/dark-cell-color.valid.json
tests/test_dark_cell_color.py
```

## Dispatcher Task Added

```text
dark_cell_color_emergence_tests
```

The task runs:

```bash
python tests/test_dark_cell_color.py
```

## Verification

Run:

```bash
python tests/test_dark_cell_color.py
python scripts/rtg_dispatcher.py --task dark_cell_color_emergence_tests
python scripts/rtg_dispatcher.py --task all
```

Expected outputs include:

```text
RTG dark-cell color emergence tests passed.
RTG repo dispatcher completed.
```

## What Changed

Before this layer:

```text
darkness was a value
color was a metaphor
```

After this layer:

```text
color emergence is a provisional executable governance behavior
```

## Tested Behavior

This layer tests that:

```text
color intensity increases as governed observation accumulates
darkness decreases as governed observation accumulates
emission readiness remains stabilization-bound
color family matches governance posture
stable color requires sufficient emission readiness
```

## Non-Claim

This layer does not prove RTG.

It creates the first machine-checkable behavior for dark transition cells gaining governed color through accumulated admissibility-at-commit style observations.
