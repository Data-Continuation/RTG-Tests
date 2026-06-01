# RTG Supersession Authority Conflict Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **supersession authority conflict semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
authority
```

## Done State

```text
fixtures/supersession-authority-conflict-semantic-behavior.valid.json exists
tests/test_supersession_authority_conflict_semantic_behavior.py exists
config/rtg_declared_tasks.json declares supersession_authority_conflict_semantic_behavior_tests
python tests/test_supersession_authority_conflict_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task supersession_authority_conflict_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
