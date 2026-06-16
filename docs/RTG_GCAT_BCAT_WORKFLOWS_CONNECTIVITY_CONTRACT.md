# RTG to GCAT-BCAT Workflows Connectivity Contract

## Purpose

This document defines the source-side RTG contract for requesting solver work from:

```text
GCAT-BCAT-Engine/workflows
```

RTG-Tests is the request and ingestion side. It is not the solver runtime.

## Contract Summary

```text
source_repo: Data-Continuation/RTG-Tests
target_repo: GCAT-BCAT-Engine/workflows
target_execution_layer: math_solver/validation
workflow: .github/workflows/validation_run.yml
trigger: workflow_dispatch
runner: ubuntu-latest
required_secret: ANTHROPIC_API_KEY
run_id: RTG-001
budget_ceiling: 50.00
```

## Expected Artifacts

```text
external-full-results
  ext2_phase1.json
  ext2_sources.json
  ext2_phase3.json
  ext2_report.json
```

## Contract-Ready Claim

This contract allows only:

```text
handoff_contract_ready
```

It does not claim:

```text
workflow_dispatch_attempted
artifact_returned
artifact_ingested
rtg_state_updated
```
