# RTG Authority Delegation Chain Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **authority delegation chain semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
authority
```

## Done State

```text
fixtures/authority-delegation-chain-semantic-behavior.valid.json exists
tests/test_authority_delegation_chain_semantic_behavior.py exists
config/rtg_declared_tasks.json declares authority_delegation_chain_semantic_behavior_tests
python tests/test_authority_delegation_chain_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task authority_delegation_chain_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
