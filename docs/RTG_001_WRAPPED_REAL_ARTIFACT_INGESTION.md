# RTG-001 Wrapped Real Artifact Ingestion

## Purpose

This layer is the first RTG-001 stage allowed to record:

```text
artifact_ingested_as_rtg_001: true
```

It consumes the wrapped real artifact receipt created by the crosswalk approval layer.

## Inputs

```text
evidence/rtg_001/crosswalk_approval.json
evidence/rtg_001/rtg_001_wrapped_real_artifact_receipt.json
```

## Output

```text
ingestion/rtg_001/rtg_001_real_artifact_ingestion_result.json
```

## Preserved Evidence

```text
original_reported_run_id: EXT-002-FIXED
target_case_id: RTG-001
actual_cost_receipt.total_cost_usd: 0.0219265
mismatch_hidden: false
direct_ingestion_without_crosswalk_blocked: true
```

## Allowed Claim After This Stage

```text
artifact_returned: true
crosswalk_approved: true
artifact_ingested_as_rtg_001: true
```

## Still Blocked

```text
rtg_state_updated_from_real_artifact: false
final_correctness_claimed: false
autonomous_theorem_proving_claimed: false
```

## Next Build Requirement

Add the real-artifact RTG state update layer that reads:

```text
ingestion/rtg_001/rtg_001_real_artifact_ingestion_result.json
```

and only then records:

```text
rtg_state_updated_from_real_artifact: true
```
