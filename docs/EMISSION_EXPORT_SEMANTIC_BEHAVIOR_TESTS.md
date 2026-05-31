# RTG Emission Export Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **emission export semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/emission-export-semantic-behavior.valid.json exists
tests/test_emission_export_semantic_behavior.py exists
config/rtg_declared_tasks.json declares emission_export_semantic_behavior_tests
python tests/test_emission_export_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task emission_export_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Emission/export behavior separates local emission, export eligibility, redaction requirement, and export block.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
