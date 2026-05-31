# RTG Dark Cell Color Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **dark cell color semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/dark-cell-color-semantic-behavior.valid.json exists
tests/test_dark_cell_color_semantic_behavior.py exists
config/rtg_declared_tasks.json declares dark_cell_color_semantic_behavior_tests
python tests/test_dark_cell_color_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task dark_cell_color_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Dark-cell behavior is driven by evidence density, observer coverage, and classification stability.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
