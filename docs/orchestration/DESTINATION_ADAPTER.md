# Governed destination adapter

RTG-Tests accepts only dispatch envelopes that bind a work contract to this repository and declare the `governed_research_execution` capability.

## Required checks

1. `destination.repository` equals `Data-Continuation/RTG-Tests`.
2. `destination.capability` equals `governed_research_execution`.
3. `contract_sha256` and `envelope_sha256` are present.
4. `work_id` identifies a registered Experiment 003 workload.
5. Execution remains bounded by the referenced preregistration and stop conditions.

## Return receipt

The destination emits a receipt containing:

- work ID;
- destination repository;
- result;
- evidence references;
- passed acceptance checks;
- triggered stop conditions;
- deterministic receipt SHA-256.

The destination cannot declare orchestration completion directly. It returns evidence to `master-records/orchestration`, which performs the governed state transition and continuation routing.
