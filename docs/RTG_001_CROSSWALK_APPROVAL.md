# RTG-001 Crosswalk Approval

## Purpose

This layer approves a controlled crosswalk from the returned workflow artifact to the RTG-001 ingestion path.

The returned real artifact reports:

```text
EXT-002-FIXED
```

The RTG case is:

```text
RTG-001
```

The mismatch is preserved and must not be hidden.

## Inputs

```text
evidence/rtg_001/normalized_ingestion_candidate.json
evidence/rtg_001/crosswalk_policy.json
```

## Outputs

```text
evidence/rtg_001/crosswalk_approval.json
evidence/rtg_001/rtg_001_wrapped_real_artifact_receipt.json
```

## Allowed Claim After Approval

```text
crosswalk_approved: true
wrapped_receipt_created: true
artifact_returned: true
actual_solver_cost_receipt_detected: true
```

## Still Blocked

```text
artifact_ingested_as_rtg_001: false
rtg_state_updated_from_real_artifact: false
final_correctness_claimed: false
autonomous_theorem_proving_claimed: false
```

## Next Build Requirement

Use the wrapped real artifact receipt to create a real RTG-001 ingestion path that records:

```text
artifact_ingested_as_rtg_001: true
```

only after the crosswalk approval file exists and validates.
