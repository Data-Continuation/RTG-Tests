# RTG Dead Basis Testing Doctrine

## Purpose

This document defines the RTG testing rule needed for RTG-001 and all future solver-handoff tests.

A **dead basis** is a test foundation that still exists, may still run, and may even pass, but no longer produces meaningful transition power.

```text
dead_basis
= a basis set of tests, fixtures, tasks, candidate vectors, or assumptions
  that no longer distinguishes, routes, validates, rejects, emits, receives,
  learns from, or updates a real transition.
```

## RTG-001 Risk

The central risk discovered during RTG-001 is:

```text
Data-Continuation/RTG-Tests keeps testing itself
while GCAT-BCAT-Engine/workflows is never invoked.
```

That creates a false-transition path:

```text
local RTG test passed
→ system claims solver pipeline was tested
→ math-solver never ran
```

This repo must block that claim.

## Live Basis Target

A live RTG basis for RTG-001 is the complete boundary:

```text
Data-Continuation/RTG-Tests
→ governed RTG request / problem spec
→ GCAT-BCAT-Engine/workflows
→ math_solver/validation
→ GitHub Actions / Ubuntu runner
→ Anthropic reasoning phase where required
→ returned artifacts
→ RTG ingestion
→ RTG state update
```

## Allowed Claims by State

```text
contract_ready:
  RTG knows the target workflow and expected artifact set.

handoff_installed_in_execution_repo:
  GCAT-BCAT-Engine/workflows has RTG-001 installed.

workflow_dispatch_attempted:
  GitHub Actions dispatch has evidence.

artifact_returned:
  external-full-results exists.

artifact_ingested:
  RTG parsed ext2_*.json and preserved the claim boundary.

rtg_state_updated:
  RTG wrote a receipt-chain/state update from returned evidence.
```

## Blocked Claims Until Evidence Exists

```text
math_solver_executed
anthropic_api_called
ubuntu_sandbox_validation_performed
artifact_returned
artifact_ingested
rtg_state_updated
autonomous_theorem_proving_claimed
final_correctness_claimed
```

## Live-Basis Rule

A local test is live only if it identifies or constrains the real transition boundary.

A local test is dead if it only proves:

```text
pytest_passed: yes
json_file_exists: yes
task_declared: yes
```

## RTG-001 Implementation Rule

RTG-001 must treat local connectivity and ingestion fixtures as scaffolding only.

The real solver claim requires returned artifact evidence from:

```text
GCAT-BCAT-Engine/workflows
external-full-results
  ext2_phase1.json
  ext2_sources.json
  ext2_phase3.json
  ext2_report.json
```
