# RTG False Transition Semantic Behavior Tests

## Purpose

This semantic-differentiation test gives **false transition semantic behavior** its own mechanism-specific classifier instead of reusing the broad cross-layer template.

## Done State

```text
fixtures/false-transition-semantic-behavior.valid.json exists
tests/test_false_transition_semantic_behavior.py exists
config/rtg_declared_tasks.json declares false_transition_semantic_behavior_tests
python tests/test_false_transition_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task false_transition_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

False-transition behavior distinguishes spoofing, contradiction, unsupported overclaim, and valid evidence.

## Why This Matters

This test begins the next RTG phase:

```text
broad executable grammar
→ differentiated mechanism behavior
```

## Non-Claim

This test does not prove final RTG mathematics.

It makes one RTG mechanism more specific and falsifiable.
