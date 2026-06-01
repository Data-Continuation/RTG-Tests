# RTG Semantic Claim Density Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **semantic claim density semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
semantic
```

## Done State

```text
fixtures/semantic-claim-density-semantic-behavior.valid.json exists
tests/test_semantic_claim_density_semantic_behavior.py exists
config/rtg_declared_tasks.json declares semantic_claim_density_semantic_behavior_tests
python tests/test_semantic_claim_density_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task semantic_claim_density_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
