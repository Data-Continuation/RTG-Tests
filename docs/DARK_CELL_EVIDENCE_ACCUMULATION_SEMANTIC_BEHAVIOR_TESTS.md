# RTG Dark Cell Evidence Accumulation Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **dark cell evidence accumulation semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
dark
```

## Done State

```text
fixtures/dark-cell-evidence-accumulation-semantic-behavior.valid.json exists
tests/test_dark_cell_evidence_accumulation_semantic_behavior.py exists
config/rtg_declared_tasks.json declares dark_cell_evidence_accumulation_semantic_behavior_tests
python tests/test_dark_cell_evidence_accumulation_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task dark_cell_evidence_accumulation_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
