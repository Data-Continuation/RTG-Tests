# RTG Detector Coverage Threshold Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **detector coverage threshold semantic behavior**.

## Mechanism Group

```text
detector
```

## Done State

```text
fixtures/detector-coverage-threshold-semantic-behavior.valid.json exists
tests/test_detector_coverage_threshold_semantic_behavior.py exists
config/rtg_declared_tasks.json declares detector_coverage_threshold_semantic_behavior_tests
python tests/test_detector_coverage_threshold_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task detector_coverage_threshold_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
