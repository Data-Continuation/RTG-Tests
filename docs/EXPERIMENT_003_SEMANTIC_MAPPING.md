# Experiment 003 — Semantic Mapping and Baseline Contracts

## Status

`LOCKED_BEFORE_MODEL_FIT`

This stage defines how publisher fields may be converted into RTG observables and competing baseline inputs. It does not fit a model, inspect locked-test outcomes, or establish a physical claim.

## Partition access

Only calibration and validation partitions may be used. The locked-test partition remains sealed. Any implementation that reads locked-test row content before the release condition is procedurally invalid.

## RTG observables

The mapping registry fixes ten observables: phase, cadence, authority, lineage, route, destination, necessity, weighted mismatch, closure, and recoverability. Each value is bounded in `[0,1]` and must be produced by a documented transformation.

Missing required observables yield `INDETERMINATE`. They are not silently imputed and may not be converted into favorable activation decisions.

## Normalization

Continuous scaling is fit on calibration rows only. Validation and future locked-test values use those calibration parameters and are clipped to `[0,1]`. A degenerate calibration column maps to zero for every non-missing value.

## Baselines

Five baseline classes are fixed before model fitting:

1. Intercept-only constant mean.
2. Ordinary least squares.
3. Ridge regression with validation-selected regularization.
4. Isotonic regression.
5. Random forest using a bounded preregistered validation grid.

## Scoring and advancement

Mean absolute error is primary. Root mean squared error and Spearman rank correlation are secondary.

RTG advances only if validation MAE improves over every baseline by at least `0.01` absolute while closure and recoverability are not worse. The study stops before test release if mapping coverage is below `0.70` or a required baseline class cannot be constructed from published fields.

## Claim boundary

This stage makes no claim of physical validation, instantaneous transport, wormholes, or faster-than-light behavior.
