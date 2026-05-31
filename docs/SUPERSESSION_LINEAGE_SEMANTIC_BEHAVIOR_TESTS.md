# RTG Supersession Lineage Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **supersession lineage semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/supersession-lineage-semantic-behavior.valid.json exists
tests/test_supersession_lineage_semantic_behavior.py exists
config/rtg_declared_tasks.json declares supersession_lineage_semantic_behavior_tests
python tests/test_supersession_lineage_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task supersession_lineage_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Supersession-lineage behavior depends on parent continuity, newer timestamp, stronger receipt, and non-conflicting authority.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
