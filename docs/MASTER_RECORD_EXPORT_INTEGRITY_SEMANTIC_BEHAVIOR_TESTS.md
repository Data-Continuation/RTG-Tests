# RTG Master Record Export Integrity Semantic Behavior Hotfix Tests

## Purpose

This hotfix replaces the semantic-next-50 test file for **master record export integrity semantic behavior** with deterministic, self-contained execution.

## Mechanism Group

```text
export
```

## Done State

```text
fixtures/master-record-export-integrity-semantic-behavior.valid.json exists
tests/test_master_record_export_integrity_semantic_behavior.py exists
config/rtg_declared_tasks.json declares master_record_export_integrity_semantic_behavior_tests
python tests/test_master_record_export_integrity_semantic_behavior.py passes
python scripts/rtg_dispatcher.py --task master_record_export_integrity_semantic_behavior_tests passes
python scripts/rtg_dispatcher.py --task all passes in GitHub Actions
```

## Core Rule

The declared task must execute cleanly under GitHub Actions and preserve its mechanism-specific state vocabulary.

## Non-Claim

This hotfix does not add new RTG task count.
