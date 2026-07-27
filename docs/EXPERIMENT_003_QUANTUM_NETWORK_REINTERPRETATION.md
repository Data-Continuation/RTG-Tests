# Experiment 003 — Quantum-Network Reinterpretation

**Experiment ID:** `RTG-EXP-003`  
**Posture:** preregistered reinterpretation only  
**Maturity:** `QUANTUM_REINTERPRETATION_REGISTERED`  
**Physical validation claim:** false

## Purpose

Experiment 003 asks whether the relational quantities developed in Experiments 001 and 002 can be mapped onto an existing quantum-network dataset without changing their definitions after observing outcomes.

This experiment does not test instantaneous matter transport, traversable wormholes, faster-than-light signaling, or a new physical force.

## Allowed source classes

The first dataset must come from one of these classes:

1. quantum teleportation;
2. entanglement swapping;
3. quantum repeater trials;
4. quantum-switch or controlled causal-order trials.

The exact dataset must be public or independently obtainable and must include event-level observations or sufficient aggregate statistics for held-out evaluation.

## Locked RTG variables

Before dataset ingestion, each trial is mapped to:

- `delta_phase`: phase or synchronization mismatch;
- `delta_cadence`: emission/detection timing mismatch;
- `delta_authority`: protocol-control validity mismatch;
- `delta_lineage`: source-to-destination state-lineage mismatch;
- `delta_route`: channel or path availability mismatch;
- `delta_destination`: destination readiness or ingestion mismatch;
- `necessity`: whether a protocol transition is required;
- `weighted_mismatch`: the Experiment 002 quadratic form;
- `corridor_active`: preregistered RTG candidate activation;
- `closure`: destination ingestion and terminal record completion.

Definitions may be refined only before the dataset identifier and analysis split are committed. Any later change creates a new experiment version.

## Primary outcome

The initial target is a conventional operational result such as successful state transfer, entanglement-swapping success, or valid process completion.

No outcome may be named `bridge_detected`, `instantaneous_transfer`, or `wormhole`.

## Baseline models

RTG must be evaluated against at least:

- the source publication's standard model;
- a fidelity/loss-only model;
- a timing-only model;
- a channel-availability model;
- a simple multivariable statistical baseline.

## Data split

A dataset must be divided before model evaluation into:

- training/calibration set: at most 60%;
- validation set: at least 20%;
- locked test set: at least 20%.

The locked test set must not be used to choose weights, thresholds, variables, exclusions, or transformations.

## Success criterion

Experiment 003 advances only if the frozen RTG candidate produces at least one preregistered out-of-sample prediction that:

1. is evaluated on the locked test set;
2. differs from each registered baseline;
3. improves a declared metric or correctly predicts a forbidden/allowed region;
4. survives sensitivity analysis;
5. does not depend on post-hoc exclusions;
6. can be reproduced from the published mapping and data split.

Distinguishability on synthetic fixtures is insufficient.

## Stop conditions

The quantum reinterpretation is stopped or constrained if:

- RTG variables reduce exactly to existing fidelity, loss, timing, or channel variables;
- no out-of-sample improvement or novel restriction appears;
- results disappear under reasonable alternate splits;
- the mapping requires outcome knowledge;
- missing data prevent reconstructable lineage or closure;
- the source dataset does not permit independent reproduction.

## Claim boundary

Permitted after preregistration:

> RTG has a registered protocol for reinterpretation against quantum-network data.

Permitted only after a successful locked test:

> A frozen RTG parameterization produced a specified out-of-sample result on a named quantum-network dataset.

Prohibited:

> RTG has discovered a quantum bridge, instantaneous particle traversal, a wormhole, or faster-than-light signaling.

## Required next artifacts

- `registries/experiment-003-preregistration.json`;
- dataset-selection receipt containing identifier, license, checksum, and selection date;
- immutable train/validation/test split manifest;
- variable-mapping specification;
- baseline implementations;
- analysis script;
- deterministic result record;
- independent reproduction instructions.
