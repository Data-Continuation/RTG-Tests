# RTG Governance Output Quarantine Binding Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **governance output quarantine binding semantic behavior**.

## Mechanism Group

```text
governance
```

## Done State

```text
fixtures/governance-output-quarantine-binding-semantic-behavior.valid.json exists
tests/test_governance_output_quarantine_binding_semantic_behavior.py exists
config/rtg_declared_tasks.json declares governance_output_quarantine_binding_semantic_behavior_tests
python tests/test_governance_output_quarantine_binding_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task governance_output_quarantine_binding_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
