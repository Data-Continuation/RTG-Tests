# Experiment 003 Calibration Contract

## Status

`LOCKED_BEFORE_MODEL_FIT`

This stage fixes the model interfaces, scoring rules, partition permissions, advancement criteria, and stop conditions before any RTG candidate or baseline is fitted to the selected quantum-network dataset.

## Partition Boundary

Only the calibration and validation partitions may be used in this stage.

The locked-test partition remains inaccessible. Its row content may not be read, summarized, transformed, fitted, scored, or used for parameter selection.

## Candidate and Baselines

The RTG relational-transition candidate is compared against five preregistered baselines:

1. Constant mean
2. Ordinary least squares
3. Ridge regression with alpha 1.0
4. Isotonic regression with clipped out-of-range predictions
5. Random forest with 256 estimators and random state 3003

All normalization statistics and model parameters must be derived from calibration rows only. Validation rows are used once for comparison and cannot drive iterative parameter selection.

## Metrics

Primary metric: mean absolute error.

Secondary metrics:

- closure rate
- recoverability rate
- indeterminate rate

## Advancement

The RTG candidate advances only if it beats every baseline by at least 0.01 absolute validation MAE and does not reduce closure or recoverability.

This rule establishes a computational advancement threshold only. It does not establish physical validation.

## Mandatory Stop Conditions

The stage stops without locked-test release if:

- mapping coverage is below 0.70;
- a required baseline cannot be constructed;
- partition leakage is detected;
- outcome-dependent feature creation is detected;
- locked-test access is detected.

## Current Execution

The accompanying validator performs a synthetic interface dry-run only. It verifies deterministic advancement logic without reading experimental rows or fitting any model.

## Claim Boundary

This stage does not support claims of physical validation, instantaneous transport, wormholes, or faster-than-light effects.
