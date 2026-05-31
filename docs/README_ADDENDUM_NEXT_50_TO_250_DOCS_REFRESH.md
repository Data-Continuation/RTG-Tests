# RTG Next 50 to 250 + Documentation Refresh Addendum

## Purpose

This bundle adds 50 RTG cross-layer coherence tests and refreshes repo documentation for the 250-test milestone.

## New Tasks

- `admissibility_gradient_observer_window_coherence_tests` → `tests/test_admissibility_gradient_observer_window_coherence.py`
- `authority_transfer_receipt_chain_coherence_tests` → `tests/test_authority_transfer_receipt_chain_coherence.py`
- `cell_boundary_quarantine_finality_coherence_tests` → `tests/test_cell_boundary_quarantine_finality_coherence.py`
- `classification_density_master_record_coherence_tests` → `tests/test_classification_density_master_record_coherence.py`
- `commit_receipt_detector_gap_coherence_tests` → `tests/test_commit_receipt_detector_gap_coherence.py`
- `confidence_floor_export_boundary_coherence_tests` → `tests/test_confidence_floor_export_boundary_coherence.py`
- `consensus_replay_supersession_coherence_tests` → `tests/test_consensus_replay_supersession_coherence.py`
- `dark_cell_admissibility_pressure_coherence_tests` → `tests/test_dark_cell_admissibility_pressure_coherence.py`
- `deferred_review_lineage_export_coherence_tests` → `tests/test_deferred_review_lineage_export_coherence.py`
- `detector_capability_identity_surface_coherence_tests` → `tests/test_detector_capability_identity_surface_coherence.py`
- `emission_latency_receipt_integrity_coherence_tests` → `tests/test_emission_latency_receipt_integrity_coherence.py`
- `export_authority_replay_repair_coherence_tests` → `tests/test_export_authority_replay_repair_coherence.py`
- `false_transition_detector_consensus_coherence_tests` → `tests/test_false_transition_detector_consensus_coherence.py`
- `governance_packet_confidence_floor_coherence_tests` → `tests/test_governance_packet_confidence_floor_coherence.py`
- `identity_authority_maturity_boundary_coherence_tests` → `tests/test_identity_authority_maturity_boundary_coherence.py`
- `lineage_drift_quarantine_review_coherence_tests` → `tests/test_lineage_drift_quarantine_review_coherence.py`
- `master_record_confidence_regrade_coherence_tests` → `tests/test_master_record_confidence_regrade_coherence.py`
- `multi_observer_receipt_density_coherence_tests` → `tests/test_multi_observer_receipt_density_coherence.py`
- `observer_class_detector_upgrade_coherence_tests` → `tests/test_observer_class_detector_upgrade_coherence.py`
- `packet_finality_reversal_coherence_tests` → `tests/test_packet_finality_reversal_coherence.py`
- `provisional_export_quorum_coherence_tests` → `tests/test_provisional_export_quorum_coherence.py`
- `quarantine_authority_decay_coherence_tests` → `tests/test_quarantine_authority_decay_coherence.py`
- `receipt_hash_detector_reentry_coherence_tests` → `tests/test_receipt_hash_detector_reentry_coherence.py`
- `replay_window_maturity_boundary_coherence_tests` → `tests/test_replay_window_maturity_boundary_coherence.py`
- `risk_pressure_lineage_supersession_coherence_tests` → `tests/test_risk_pressure_lineage_supersession_coherence.py`
- `root_boundary_transition_packet_coherence_tests` → `tests/test_root_boundary_transition_packet_coherence.py`
- `semantic_claim_maturity_filter_coherence_tests` → `tests/test_semantic_claim_maturity_filter_coherence.py`
- `shadow_transition_receipt_gap_coherence_tests` → `tests/test_shadow_transition_receipt_gap_coherence.py`
- `source_target_detector_disagreement_coherence_tests` → `tests/test_source_target_detector_disagreement_coherence.py`
- `stabilization_emission_latency_coherence_tests` → `tests/test_stabilization_emission_latency_coherence.py`
- `state_lineage_authority_reentry_coherence_tests` → `tests/test_state_lineage_authority_reentry_coherence.py`
- `supersession_confidence_floor_coherence_tests` → `tests/test_supersession_confidence_floor_coherence.py`
- `temporal_receipt_replay_repair_coherence_tests` → `tests/test_temporal_receipt_replay_repair_coherence.py`
- `transition_evidence_density_export_coherence_tests` → `tests/test_transition_evidence_density_export_coherence.py`
- `unknown_unknown_confidence_floor_coherence_tests` → `tests/test_unknown_unknown_confidence_floor_coherence.py`
- `validity_chain_master_record_coherence_tests` → `tests/test_validity_chain_master_record_coherence.py`
- `zeno_admissibility_pressure_coherence_tests` → `tests/test_zeno_admissibility_pressure_coherence.py`
- `observer_identity_quorum_finality_coherence_tests` → `tests/test_observer_identity_quorum_finality_coherence.py`
- `ecosystem_replay_packet_integrity_coherence_tests` → `tests/test_ecosystem_replay_packet_integrity_coherence.py`
- `full_commit_authority_receipt_stack_coherence_tests` → `tests/test_full_commit_authority_receipt_stack_coherence.py`
- `admissibility_observation_geometry_coherence_tests` → `tests/test_admissibility_observation_geometry_coherence.py`
- `authority_class_transition_visibility_coherence_tests` → `tests/test_authority_class_transition_visibility_coherence.py`
- `cell_color_receipt_density_coherence_tests` → `tests/test_cell_color_receipt_density_coherence.py`
- `detector_gap_false_negative_coherence_tests` → `tests/test_detector_gap_false_negative_coherence.py`
- `emission_threshold_quarantine_boundary_coherence_tests` → `tests/test_emission_threshold_quarantine_boundary_coherence.py`
- `governance_output_lineage_replay_coherence_tests` → `tests/test_governance_output_lineage_replay_coherence.py`
- `multi_entity_boundary_coupling_coherence_tests` → `tests/test_multi_entity_boundary_coupling_coherence.py`
- `observer_reality_coupling_maturity_coherence_tests` → `tests/test_observer_reality_coupling_maturity_coherence.py`
- `purpose_convergence_boundary_coherence_tests` → `tests/test_purpose_convergence_boundary_coherence.py`
- `rtg_250_milestone_integrity_coherence_tests` → `tests/test_rtg_250_milestone_integrity_coherence.py`

## Expected Declared Task Count

```text
250 executable RTG tests
+ 1 registry integrity test
+ 1 dispatcher self-check
= 252 declared tasks total
```

## Canonical Paths Preserved

```text
fixture_smoke_tests → python tests/test_rtg_fixtures.py
registry_task_file_integrity_tests → python tests/test_registry_task_file_integrity.py
dispatcher_self_check → python scripts/verify_rtg_dispatcher.py
```
