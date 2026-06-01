# RTG Multi Entity Authority Asymmetry Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **multi entity authority asymmetry semantic behavior**.

## Mechanism Group

```text
multi
```

## Done State

```text
fixtures/multi-entity-authority-asymmetry-semantic-behavior.valid.json exists
tests/test_multi_entity_authority_asymmetry_semantic_behavior.py exists
config/rtg_declared_tasks.json declares multi_entity_authority_asymmetry_semantic_behavior_tests
python tests/test_multi_entity_authority_asymmetry_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task multi_entity_authority_asymmetry_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
