# RTG Multi Entity Recoverability Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **multi entity recoverability semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
multi
```

## Done State

```text
fixtures/multi-entity-recoverability-semantic-behavior.valid.json exists
tests/test_multi_entity_recoverability_semantic_behavior.py exists
config/rtg_declared_tasks.json declares multi_entity_recoverability_semantic_behavior_tests
python tests/test_multi_entity_recoverability_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task multi_entity_recoverability_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
