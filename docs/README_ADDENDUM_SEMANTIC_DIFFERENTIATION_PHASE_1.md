# RTG Semantic Differentiation Phase 1 Addendum

## New Tasks

- `observer_window_semantic_behavior_tests` → `tests/test_observer_window_semantic_behavior.py`
- `authority_boundary_semantic_behavior_tests` → `tests/test_authority_boundary_semantic_behavior.py`
- `false_transition_semantic_behavior_tests` → `tests/test_false_transition_semantic_behavior.py`
- `unknown_unknown_semantic_behavior_tests` → `tests/test_unknown_unknown_semantic_behavior.py`
- `zeno_pressure_semantic_behavior_tests` → `tests/test_zeno_pressure_semantic_behavior.py`
- `dark_cell_color_semantic_behavior_tests` → `tests/test_dark_cell_color_semantic_behavior.py`
- `quarantine_release_semantic_behavior_tests` → `tests/test_quarantine_release_semantic_behavior.py`
- `confidence_regrade_semantic_behavior_tests` → `tests/test_confidence_regrade_semantic_behavior.py`
- `supersession_lineage_semantic_behavior_tests` → `tests/test_supersession_lineage_semantic_behavior.py`
- `emission_export_semantic_behavior_tests` → `tests/test_emission_export_semantic_behavior.py`
- `multi_entity_boundary_semantic_behavior_tests` → `tests/test_multi_entity_boundary_semantic_behavior.py`
- `purpose_convergence_boundary_semantic_behavior_tests` → `tests/test_purpose_convergence_boundary_semantic_behavior.py`

## Expected Declared Task Count

```text
262 executable RTG tests
+ 1 registry integrity test
+ 1 dispatcher self-check
= 264 declared tasks total
```

## Canonical Paths Preserved

```text
fixture_smoke_tests → python tests/test_rtg_fixtures.py
registry_task_file_integrity_tests → python tests/test_registry_task_file_integrity.py
dispatcher_self_check → python scripts/verify_rtg_dispatcher.py
```
