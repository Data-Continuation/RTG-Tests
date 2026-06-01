# RTG Export Boundary Recipient Class Semantic Behavior Tests

## Purpose

This semantic-differentiation hotfix test adds mechanism-specific behavior for **export boundary recipient class semantic behavior**.

## Mechanism Group

```text
export
```

## Done State

```text
fixtures/export-boundary-recipient-class-semantic-behavior.valid.json exists
tests/test_export_boundary_recipient_class_semantic_behavior.py exists
config/rtg_declared_tasks.json declares export_boundary_recipient_class_semantic_behavior_tests
python tests/test_export_boundary_recipient_class_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task export_boundary_recipient_class_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

This hotfix keeps the intended semantic-differentiated state vocabulary while making the test execution path deterministic and self-contained.

## Non-Claim

This test does not prove final RTG mathematics.
