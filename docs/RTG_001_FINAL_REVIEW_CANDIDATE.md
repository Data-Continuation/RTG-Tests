# RTG-001 Final Review Candidate

## Purpose

This layer creates the final review candidate object for RTG-001 after the review packet exists.

It creates:

```text
candidates/rtg_001/rtg_001_final_review_candidate.json
candidates/rtg_001/RTG_001_FINAL_REVIEW_CANDIDATE.md
```

## Candidate Status

```text
ready_for_human_or_formal_review_pending_real_artifact_receipt
```

## Review Route

```text
route_to_review
```

## Decision Options

```text
approve_as_boundary_valid_scaffold
request_real_artifact_ingestion
route_to_replay
route_to_quarantine
route_to_solver_iteration
reject_claim_as_premature
```

## Required Evidence Before Final Claim

```text
external-full-results artifact exists
real ext2_report.json parsed
actual solver cost receipt recorded
claim boundary preserved after real artifact ingestion
human or formal review completed
```

## Claim Boundary

Allowed:

```text
final_review_candidate_created
ready_for_review
```

Still blocked:

```text
artifact_returned
artifact_ingested_from_real_artifact
rtg_state_updated_from_real_artifact
autonomous_theorem_proving_claimed
final_correctness_claimed
```
