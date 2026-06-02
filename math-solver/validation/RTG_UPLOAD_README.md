# RTG Math-Solver Upload Package

Generated: `2026-06-02T17:24:13Z`

Target repository:

```text
GCAT-BCAT-Engine/workflows
```

Upload these files to the exact target paths:

```text
math_solver/validation/rtg_instruction_artifact.json
math_solver/validation/problem_spec_rtg_instruction.yml
math_solver/validation/candidate_vectors/rtg/rtg_candidate_vectors.json
math_solver/validation/rtg_upload_manifest.json
math_solver/validation/RTG_UPLOAD_README.md
```

Run the existing validation workflow pattern:

```text
.github/workflows/validation_run_inline.yml
```

Suggested workflow inputs:

```text
run_id=RTG-381-SOLVER-INSTRUCTION-001
budget_ceiling=10.00
```

## Claim Boundary

This package requests candidate generation and reconstruction support.

It does not claim autonomous theorem proving.

It does not claim final mathematical correctness without human or formal verification.

Returned artifacts must be ingested back into RTG before any publication claim is advanced.
