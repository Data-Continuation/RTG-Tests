# RTG Zeno Pressure Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **zeno pressure semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/zeno-pressure-semantic-behavior.valid.json exists
tests/test_zeno_pressure_semantic_behavior.py exists
config/rtg_declared_tasks.json declares zeno_pressure_semantic_behavior_tests
python tests/test_zeno_pressure_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task zeno_pressure_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Zeno-pressure behavior identifies repeated near-commit attempts that consume transition opportunity without stabilizing.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
