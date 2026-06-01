# RTG Governance Output Consistency Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **governance output consistency semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
semantic
```

## Done State

```text
fixtures/governance-output-consistency-semantic-behavior.valid.json exists
tests/test_governance_output_consistency_semantic_behavior.py exists
config/rtg_declared_tasks.json declares governance_output_consistency_semantic_behavior_tests
python tests/test_governance_output_consistency_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task governance_output_consistency_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
