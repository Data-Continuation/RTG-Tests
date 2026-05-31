# RTG Cross-Layer Coherence Next 25 Addendum

## Purpose

This addendum summarizes the next 25 RTG cross-layer coherence tests added after the corrected 33-test baseline.

## Canonical Config Correction Preserved

```text
fixture_smoke_tests -> python tests/test_rtg_fixtures.py
```

## New Test Layers

- `identity_surface_replay_coherence_tests` → `tests/test_identity_surface_replay_coherence.py`
- `observer_authority_receipt_coherence_tests` → `tests/test_observer_authority_receipt_coherence.py`
- `lineage_export_coherence_tests` → `tests/test_lineage_export_coherence.py`
- `receipt_confidence_regrade_coherence_tests` → `tests/test_receipt_confidence_regrade_coherence.py`
- `anomaly_supersession_coherence_tests` → `tests/test_anomaly_supersession_coherence.py`
- `quarantine_export_coherence_tests` → `tests/test_quarantine_export_coherence.py`
- `dark_cell_detector_gap_coherence_tests` → `tests/test_dark_cell_detector_gap_coherence.py`
- `zeno_stabilization_export_coherence_tests` → `tests/test_zeno_stabilization_export_coherence.py`
- `authority_quorum_packet_coherence_tests` → `tests/test_authority_quorum_packet_coherence.py`
- `observer_window_lineage_coherence_tests` → `tests/test_observer_window_lineage_coherence.py`
- `coupling_anomaly_retention_coherence_tests` → `tests/test_coupling_anomaly_retention_coherence.py`
- `replay_supersession_order_coherence_tests` → `tests/test_replay_supersession_order_coherence.py`
- `confidence_authority_escalation_coherence_tests` → `tests/test_confidence_authority_escalation_coherence.py`
- `emission_quarantine_release_coherence_tests` → `tests/test_emission_quarantine_release_coherence.py`
- `detector_coverage_supersession_coherence_tests` → `tests/test_detector_coverage_supersession_coherence.py`
- `receipt_chain_anomaly_coherence_tests` → `tests/test_receipt_chain_anomaly_coherence.py`
- `governance_packet_replay_coherence_tests` → `tests/test_governance_packet_replay_coherence.py`
- `observer_replay_dark_cell_coherence_tests` → `tests/test_observer_replay_dark_cell_coherence.py`
- `multi_observer_consensus_coherence_tests` → `tests/test_multi_observer_consensus_coherence.py`
- `temporal_order_replay_coherence_tests` → `tests/test_temporal_order_replay_coherence.py`
- `authority_supersession_quarantine_coherence_tests` → `tests/test_authority_supersession_quarantine_coherence.py`
- `detector_dark_confidence_regrade_coherence_tests` → `tests/test_detector_dark_confidence_regrade_coherence.py`
- `emission_packet_receipt_export_coherence_tests` → `tests/test_emission_packet_receipt_export_coherence.py`
- `unknown_unknown_review_loop_coherence_tests` → `tests/test_unknown_unknown_review_loop_coherence.py`
- `full_ecosystem_commit_coherence_tests` → `tests/test_full_ecosystem_commit_coherence.py`

## Verification

Run:

```bash
python tests/test_identity_surface_replay_coherence.py
python tests/test_observer_authority_receipt_coherence.py
python tests/test_lineage_export_coherence.py
python tests/test_receipt_confidence_regrade_coherence.py
python tests/test_anomaly_supersession_coherence.py
python tests/test_quarantine_export_coherence.py
python tests/test_dark_cell_detector_gap_coherence.py
python tests/test_zeno_stabilization_export_coherence.py
python tests/test_authority_quorum_packet_coherence.py
python tests/test_observer_window_lineage_coherence.py
python tests/test_coupling_anomaly_retention_coherence.py
python tests/test_replay_supersession_order_coherence.py
python tests/test_confidence_authority_escalation_coherence.py
python tests/test_emission_quarantine_release_coherence.py
python tests/test_detector_coverage_supersession_coherence.py
python tests/test_receipt_chain_anomaly_coherence.py
python tests/test_governance_packet_replay_coherence.py
python tests/test_observer_replay_dark_cell_coherence.py
python tests/test_multi_observer_consensus_coherence.py
python tests/test_temporal_order_replay_coherence.py
python tests/test_authority_supersession_quarantine_coherence.py
python tests/test_detector_dark_confidence_regrade_coherence.py
python tests/test_emission_packet_receipt_export_coherence.py
python tests/test_unknown_unknown_review_loop_coherence.py
python tests/test_full_ecosystem_commit_coherence.py
python scripts/rtg_dispatcher.py --task all
```
