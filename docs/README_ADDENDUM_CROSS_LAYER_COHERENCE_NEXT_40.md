# RTG Cross-Layer Coherence Next 40 Addendum

## Purpose

This bundle adds the next run of 40 RTG cross-layer coherence tasks after the 121 declared-task green baseline.

## New Tasks

- `admissibility_pressure_replay_packet_coherence_tests` → `tests/test_admissibility_pressure_replay_packet_coherence.py`
- `authority_receipt_decay_coherence_tests` → `tests/test_authority_receipt_decay_coherence.py`
- `cell_shell_coupling_export_coherence_tests` → `tests/test_cell_shell_coupling_export_coherence.py`
- `classification_quarantine_replay_loop_coherence_tests` → `tests/test_classification_quarantine_replay_loop_coherence.py`
- `commit_finality_reversal_boundary_coherence_tests` → `tests/test_commit_finality_reversal_boundary_coherence.py`
- `confidence_drift_detector_upgrade_coherence_tests` → `tests/test_confidence_drift_detector_upgrade_coherence.py`
- `consensus_receipt_hash_repair_coherence_tests` → `tests/test_consensus_receipt_hash_repair_coherence.py`
- `dark_cell_master_record_export_coherence_tests` → `tests/test_dark_cell_master_record_export_coherence.py`
- `deferred_state_lineage_repair_coherence_tests` → `tests/test_deferred_state_lineage_repair_coherence.py`
- `detector_identity_surface_packet_coherence_tests` → `tests/test_detector_identity_surface_packet_coherence.py`
- `emission_authority_demotion_coherence_tests` → `tests/test_emission_authority_demotion_coherence.py`
- `export_quorum_receipt_coherence_tests` → `tests/test_export_quorum_receipt_coherence.py`
- `false_positive_detector_replay_coherence_tests` → `tests/test_false_positive_detector_replay_coherence.py`
- `governance_output_reversal_coherence_tests` → `tests/test_governance_output_reversal_coherence.py`
- `identity_surface_quarantine_release_coherence_tests` → `tests/test_identity_surface_quarantine_release_coherence.py`
- `lineage_packet_receipt_gap_coherence_tests` → `tests/test_lineage_packet_receipt_gap_coherence.py`
- `master_record_reentry_authority_coherence_tests` → `tests/test_master_record_reentry_authority_coherence.py`
- `multi_observer_detector_disagreement_coherence_tests` → `tests/test_multi_observer_detector_disagreement_coherence.py`
- `observer_window_confidence_decay_coherence_tests` → `tests/test_observer_window_confidence_decay_coherence.py`
- `packet_evidence_density_quarantine_coherence_tests` → `tests/test_packet_evidence_density_quarantine_coherence.py`
- `provisional_commit_export_coherence_tests` → `tests/test_provisional_commit_export_coherence.py`
- `quarantine_supersession_replay_coherence_tests` → `tests/test_quarantine_supersession_replay_coherence.py`
- `receipt_chain_reversal_coherence_tests` → `tests/test_receipt_chain_reversal_coherence.py`
- `replay_detector_coverage_gap_coherence_tests` → `tests/test_replay_detector_coverage_gap_coherence.py`
- `risk_pressure_quorum_escalation_coherence_tests` → `tests/test_risk_pressure_quorum_escalation_coherence.py`
- `root_boundary_reentry_review_coherence_tests` → `tests/test_root_boundary_reentry_review_coherence.py`
- `semantic_claim_false_transition_coherence_tests` → `tests/test_semantic_claim_false_transition_coherence.py`
- `shadow_transition_detector_upgrade_coherence_tests` → `tests/test_shadow_transition_detector_upgrade_coherence.py`
- `source_identity_receipt_export_coherence_tests` → `tests/test_source_identity_receipt_export_coherence.py`
- `stabilization_pressure_lineage_coherence_tests` → `tests/test_stabilization_pressure_lineage_coherence.py`
- `state_evidence_authority_decay_coherence_tests` → `tests/test_state_evidence_authority_decay_coherence.py`
- `supersession_master_record_export_coherence_tests` → `tests/test_supersession_master_record_export_coherence.py`
- `temporal_order_quarantine_reentry_coherence_tests` → `tests/test_temporal_order_quarantine_reentry_coherence.py`
- `transition_packet_confidence_floor_coherence_tests` → `tests/test_transition_packet_confidence_floor_coherence.py`
- `unknown_unknown_anomaly_resolution_coherence_tests` → `tests/test_unknown_unknown_anomaly_resolution_coherence.py`
- `validity_chain_quorum_finality_coherence_tests` → `tests/test_validity_chain_quorum_finality_coherence.py`
- `zeno_pressure_quarantine_boundary_coherence_tests` → `tests/test_zeno_pressure_quarantine_boundary_coherence.py`
- `observer_identity_receipt_drift_coherence_tests` → `tests/test_observer_identity_receipt_drift_coherence.py`
- `ecosystem_packet_continuity_coherence_tests` → `tests/test_ecosystem_packet_continuity_coherence.py`
- `full_rtg_admissibility_stack_coherence_tests` → `tests/test_full_rtg_admissibility_stack_coherence.py`

## Expected Declared Task Count

```text
160 executable RTG tests
+ 1 dispatcher self-check
= 161 declared tasks total
```

## Canonical Path Preserved

```text
fixture_smoke_tests → python tests/test_rtg_fixtures.py
```
