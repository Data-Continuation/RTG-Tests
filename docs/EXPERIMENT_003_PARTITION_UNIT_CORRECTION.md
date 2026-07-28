# Experiment 003 Partition-Unit Correction

## Status

`STOPPED_BEFORE_MODEL_FIT`

The first sealed split remains immutable evidence, but it is superseded for model fitting because its partition unit was too fine-grained for publisher-defined composite analysis objects.

## Trigger

The calibration-row receipt prepared 12 calibration records and 5 validation records while preserving locked-test sealing. Mapping coverage was `0.15384615384615385`, below the preregistered minimum of `0.70`.

No model was fitted. No locked-test content was opened.

## Finding

Figure 3 represents one analysis object through four aligned arrays:

- `nbar`
- `expfidelity`
- `errornbar`
- `errorsexpfidelity`

Assigning those source records independently can separate predictor, target, and uncertainty components across partitions. Recombining them across partitions would create leakage. Dropping them reduces coverage below the admissible threshold.

## Required correction

A fresh manifest must assign partitions to the complete publisher-defined composite object before element expansion. Every expanded element inherits the composite partition.

The original manifest and all receipts remain retained and reconstructable. They must not be rewritten, deleted, or used for fitting.

## Advancement boundary

Calibration-only fitting remains prohibited until the new composite manifest:

1. passes deterministic integrity checks;
2. preserves locked-test sealing;
3. produces calibration and validation records;
4. reaches mapping coverage of at least `0.70`;
5. passes all baseline constructability gates.
