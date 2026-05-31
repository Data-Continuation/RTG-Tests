# RTG Quarantine Release Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **quarantine release semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/quarantine-release-semantic-behavior.valid.json exists
tests/test_quarantine_release_semantic_behavior.py exists
config/rtg_declared_tasks.json declares quarantine_release_semantic_behavior_tests
python tests/test_quarantine_release_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task quarantine_release_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

Quarantine release requires risk decay, replay repair, authority restoration, and no unresolved anomaly.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
