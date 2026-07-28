# Experiment 003 — Integrity Ingestion and Sealed Partition Manifest

## Status

`SOURCE_INTEGRITY_AND_PARTITION_SEAL_IMPLEMENTED`

This stage retrieves the six files selected in `RTG-EXP-003-DATASET-001`, verifies the publisher-provided byte counts and MD5 checksums, computes SHA-256 digests, canonicalizes text deterministically, and assigns each data row to the preregistered 60/20/20 partition rule.

The selected Zenodo record publishes six files totaling 2.9 kB and provides an MD5 checksum for each file. The record is version v1, published June 15, 2021, and licensed under CC BY 4.0.

## Allowed operations

- retrieve the six named files from the locked Zenodo record;
- verify file byte counts and MD5 checksums;
- compute source and canonical-text SHA-256 digests;
- normalize UTF-8 text and line endings;
- remove blank and comment-only lines from the data-row stream;
- normalize internal whitespace for stable row identity;
- assign partitions using the locked SHA-256 bucket rule;
- emit a sealed, machine-readable manifest.

## Prohibited operations

- computing outcome distributions or summary statistics;
- fitting RTG variables or thresholds;
- fitting any baseline model;
- changing row assignments after seeing values or results;
- publishing canonical content for locked-test rows;
- making physical-validation, instantaneous-transport, wormhole, or faster-than-light claims.

## Canonical row key

```text
record_doi
+ LF + file_name
+ LF + zero_based_data_row_index
+ LF + canonical_row_text
```

The first eight bytes of the SHA-256 digest are interpreted as an unsigned big-endian integer and reduced modulo 10:

```text
0–5 = calibration
6–7 = validation
8–9 = locked_test
```

## Locked-test sealing

The manifest includes the file name, row index, row-key digest, partition bucket, partition label, and canonical-row digest for every row. For locked-test rows, `canonical_row_text` is set to `null` and `sealed` is set to `true`.

This permits independent verification of partition identity without exposing the locked-test content during model construction.

## Generated artifact

```text
results/experiment-003-sealed-split-manifest.json
```

The manifest records:

- all six verified source files;
- source and canonical SHA-256 digests;
- canonical data-row counts;
- every immutable row assignment;
- partition counts;
- analysis and claim locks;
- a manifest-level SHA-256 digest.

## Execution

```bash
python tests/test_experiment_003_integrity_ingestion.py
python tools/ingest_experiment_003_source.py
```

## Advancement condition

The experiment may advance to parsing and semantic field mapping only after the integrity-ingestion workflow completes successfully and the sealed manifest is retained as a workflow artifact.

Advancement does not authorize test-partition access or outcome analysis.
