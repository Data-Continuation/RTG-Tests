# Experiment 003 Calibration-Row Preparation

This stage converts only publisher-schema-authorized Figure 3 and Figure 4 experimental records into calibration and validation rows.

It does not fit any model, compute outcome summaries, tune parameters, or expose locked-test content.

## Partition rule

Each expanded array element inherits the partition of its source manifest record. Records from different partitions are never joined to reconstruct a complete array set.

This is particularly important for Figure 3, whose predictor, target, and uncertainty arrays are separate source records. If those required arrays do not coexist within the same allowed partition, the parser returns no Figure 3 records for that partition and the readiness decision may be `STOP_REQUIRED`.

## Included data

- Figure 3 experimental mean-photon-number and teleportation-fidelity arrays, including measurement uncertainties.
- Figure 4 experimental delay and teleportation-fidelity pairs, including published target uncertainty when present.

Theoretical and simulated curves remain excluded. Figure 2 remains outside this scalar prediction task.

## Fail-closed conditions

The stage rejects execution when:

- any locked-test row contains canonical text;
- the manifest identity differs from the locked schema;
- an allowed-partition row is unexpectedly sealed;
- Figure 3 arrays within one partition have unequal lengths;
- a target lies outside the locked interval `[0, 1]`.

The emitted receipt records partition counts, mapping coverage, sealed locked-test metadata count, state, and a canonical SHA-256 digest.
