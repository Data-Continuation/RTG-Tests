# RTG Observer Window Nested Aperture Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **observer window nested aperture semantic behavior**.

## Mechanism Group

```text
observer
```

## Done State

```text
fixtures/observer-window-nested-aperture-semantic-behavior.valid.json exists
tests/test_observer_window_nested_aperture_semantic_behavior.py exists
config/rtg_declared_tasks.json declares observer_window_nested_aperture_semantic_behavior_tests
python tests/test_observer_window_nested_aperture_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task observer_window_nested_aperture_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
