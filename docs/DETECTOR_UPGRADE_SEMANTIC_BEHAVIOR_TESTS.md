# RTG Detector Upgrade Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **detector upgrade semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
detector
```

## Done State

```text
fixtures/detector-upgrade-semantic-behavior.valid.json exists
tests/test_detector_upgrade_semantic_behavior.py exists
config/rtg_declared_tasks.json declares detector_upgrade_semantic_behavior_tests
python tests/test_detector_upgrade_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task detector_upgrade_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
