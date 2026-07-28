# Experiment 003 Calibration Readiness Gate

## Result

`STOP_REQUIRED`

The integrity, semantic-mapping, and calibration-contract stages are valid, but the current mapping registry does not yet bind the source files to exact ordered columns or designate a prediction target. Model fitting at this point would require analyst discretion after source access and could create outcome-dependent features.

## Blocking gap

Before calibration begins, the repository must contain an executable schema registry that fixes, for each data file:

- the ordered column names and units;
- header and missing-value handling;
- the prediction target;
- the source columns used by each RTG observable;
- deterministic transforms;
- duplicate-row behavior.

The schema must be derived from publisher descriptions and committed before calibration or validation outcomes are calculated.

## Preserved locks

- locked-test content remains sealed;
- no RTG parameters have been fitted;
- no baseline parameters have been fitted;
- no performance statistics have been computed;
- all physical and instantaneous-transport claims remain prohibited.

This stop is an admissibility success: the pipeline refused to convert a conceptual mapping into a fitted result without reconstructable column-level authority.
