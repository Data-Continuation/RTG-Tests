# RTG Cell Geometry Layer Addendum

## Purpose

This addendum summarizes the first substantive RTG test layer added after the green dispatcher baseline.

## Files Added or Replaced

```text
config/rtg_declared_tasks.json
docs/CELL_GEOMETRY_TESTS.md
fixtures/cell-geometry.valid.json
tests/test_cell_geometry.py
```

## Dispatcher Task Added

```text
cell_geometry_smoke_tests
```

The task runs:

```bash
python tests/test_cell_geometry.py
```

## Verification

Run:

```bash
python tests/test_cell_geometry.py
python scripts/rtg_dispatcher.py --task all
```

Expected outputs include:

```text
RTG cell geometry smoke tests passed.
RTG repo dispatcher completed.
```

## Non-Claim

This layer does not prove RTG.

It only establishes the first coherent local geometry fixture and validates minimal relationships among observability, darkness, confidence, stabilization, and emission readiness.
