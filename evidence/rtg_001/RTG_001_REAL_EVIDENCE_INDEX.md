# RTG-001 Real Evidence Index

## Evidence Found

Real workflow evidence has been detected by the Publisher watcher.

```text
repo: GCAT-BCAT-Engine/workflows
workflow_run_id: 27597978374
workflow_name: StegVerse External Full Process v2 - Erdos Class
workflow_conclusion: success
artifact_id: 7658749562
artifact_name: external-full-results
artifact_size_in_bytes: 3813
artifact_expired: false
```

## Returned Files

```text
ext2_phase1.json
ext2_sources.json
ext2_phase3.json
ext2_report.json
```

## Actual Cost Receipt From Artifact

```text
reported_run_id: EXT-002-FIXED
total_cost_usd: 0.0219265
total_tokens: 3193
sources_verified: true
phase_1_cost_usd: 0.001906
phase_3_batch_cost_usd: 0.0200205
```

## Boundary Finding

The real artifact is valid workflow evidence, but it is not a direct clean RTG-001 ingestion receipt yet because:

```text
artifact_report_run_id: EXT-002-FIXED
rtg_case_id: RTG-001
claim_boundary field in ext2_report.json: absent
```

Therefore RTG may claim:

```text
artifact_returned: true
actual_solver_cost_receipt_detected: true
```

RTG may not yet claim:

```text
artifact_ingested_as_rtg_001: false
rtg_state_updated_from_real_artifact: false
final_correctness_claimed: false
autonomous_theorem_proving_claimed: false
```

## Next Build Requirement

Add a normalization / crosswalk adapter that maps the returned `EXT-002-FIXED` artifact into an RTG-001 ingestion candidate while preserving the mismatch as evidence, not hiding it.
