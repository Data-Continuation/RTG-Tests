# RTG State Lineage Repair Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **state lineage repair semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
state
```

## Done State

```text
fixtures/state-lineage-repair-semantic-behavior.valid.json exists
tests/test_state_lineage_repair_semantic_behavior.py exists
config/rtg_declared_tasks.json declares state_lineage_repair_semantic_behavior_tests
python tests/test_state_lineage_repair_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task state_lineage_repair_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
