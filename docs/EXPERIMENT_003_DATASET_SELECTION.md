# Experiment 003 Dataset Selection Receipt

## Status

```text
receipt: RTG-EXP-003-DATASET-001
state: LOCKED_BEFORE_ANALYSIS
maturity: QUANTUM_REINTERPRETATION_REGISTERED
```

## Selected source

**Dataset:** Data of *Quantum Teleportation between Remote Qubit Memories with Only a Single Photon as a Resource*  
**Publisher:** Zenodo  
**Record DOI:** `10.5281/zenodo.4953982`  
**Related article:** `10.1103/PhysRevLett.126.130502`  
**Version:** v1  
**License:** CC BY 4.0

The source falls within the preregistered `quantum_teleportation` class. It was selected because it is experimental, openly licensed, compact, independently retrievable, and accompanied by publisher-recorded checksums.

Selection did not depend on observed agreement with RTG variables or outcomes.

## Integrity boundary

The receipt records the published MD5 value and byte size for each of six source files. Downloaded material must match those values before preprocessing.

A mismatch produces:

```text
SOURCE_INTEGRITY_FAILURE
```

and prevents analysis.

## Immutable split

Each canonical data row is assigned by:

```text
key = record DOI + LF + filename + LF + zero-based row index + LF + canonical row text
bucket = unsigned_big_endian(SHA-256(key)[0:8]) mod 10
```

Assignments:

```text
0-5 = calibration
6-7 = validation
8-9 = locked test
```

This targets a deterministic 60/20/20 split. No outcome-dependent reassignment, balancing, or stratification is permitted.

## Locked-test release gate

The locked test partition remains unavailable to model selection until all of the following are committed:

1. source-file integrity verification;
2. canonical parsing and row identity rules;
3. RTG variable mappings;
4. preprocessing rules;
5. RTG parameter values learned only from calibration data;
6. baseline implementations and parameters;
7. validation-stage decisions;
8. scoring functions and advancement thresholds.

## Permitted next claim

> A public experimental quantum-teleportation dataset has been selected under a preregistered, checksum-bound, outcome-independent protocol.

## Prohibited claims

This receipt does not establish:

- a novel quantum effect;
- instantaneous transport;
- faster-than-light signaling;
- a microscopic wormhole;
- physical validation of RTG;
- superiority over quantum-information baselines.
