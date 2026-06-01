# RTG False Transition Replay Spoof Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **false transition replay spoof semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
false
```

## Done State

```text
fixtures/false-transition-replay-spoof-semantic-behavior.valid.json exists
tests/test_false_transition_replay_spoof_semantic_behavior.py exists
config/rtg_declared_tasks.json declares false_transition_replay_spoof_semantic_behavior_tests
python tests/test_false_transition_replay_spoof_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task false_transition_replay_spoof_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
