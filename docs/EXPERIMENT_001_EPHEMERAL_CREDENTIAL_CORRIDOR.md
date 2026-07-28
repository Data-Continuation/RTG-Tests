# Experiment 001 — Ephemeral Credential Corridor

**Formalism:** Relational Transition Geometry (RTG) + Transition Table (TT)  
**Posture:** falsifiable computational experiment; no physical or quantum claim  
**Primary question:** Does the RTG representation predict or explain any measurable event beyond an ordinary event-driven credential evaluator?

## Hypothesis

A credential-evaluation operator exists only when a protected transition requires review. A measurable heartbeat mismatch or dependency condition creates review necessity; the evaluator instantiates, evaluates the credential, emits ALLOW or DENY, records ingestion, and expires.

The RTG-specific claim is not merely that an event-driven function starts on demand. The proposed measurable event profile is:

```text
baseline coherence
→ ΔHB emergence
→ threshold crossing
→ evaluator instantiation
→ decision
→ destination ingestion
→ transport/monitoring closure
→ evaluator expiration
→ bounded residual or reconciliation
```

## Variables

For event `e`:

- `delta_hb`: weighted heartbeat mismatch magnitude.
- `necessity`: normalized review necessity in `[0,1]`.
- `threshold_hb`: minimum heartbeat mismatch required by the experimental policy.
- `threshold_necessity`: minimum necessity required by the experimental policy.
- `operator_instantiated`: whether the evaluator existed.
- `decision`: `ALLOW`, `DENY`, or `NONE`.
- `ingested`: whether the decision payload was ingested at the destination.
- `operator_expired`: whether the temporary evaluator ceased to exist after its bounded task.
- `closure_recorded`: whether ingestion closed the transport and monitoring loop.
- `null_triggered`: whether a conventional event-driven null model would instantiate the same evaluator.

## RTG activation rule

```text
operator_instantiated =
  delta_hb >= threshold_hb
  AND necessity >= threshold_necessity
  AND destination_requires_review
```

The Transition Table then evaluates credential validity, authority scope, freshness, destination identity, and policy.

## Null model

The primary null model is conventional event-driven access control:

```text
null_triggered = destination_requires_review
```

The null model does not require a heartbeat field, necessity field, amorphous intersection, or governed transition distance.

## Falsification condition

The distinct RTG interpretation fails this experiment when any of the following hold:

1. RTG activation and outcomes cannot be defined before observing the result.
2. `delta_hb` and `necessity` add no out-of-sample predictive information beyond the ordinary request event and policy inputs.
3. Apparent path compression disappears after preprocessing, caching, queueing, and hidden preparation are counted.
4. The claimed lineage or closure record is only a label inserted after the decision.
5. The evaluator remains active without bounded necessity, contradicting the ephemeral-operator claim.
6. A successful decision is treated as transport-complete before destination ingestion.

## Success condition for this stage

This experiment succeeds only as a formal implementation when:

- activation variables are recorded before instantiation;
- all events produce terminal records, including non-instantiation and timeout;
- successful transport closes at ingestion;
- evaluator expiration is independently observable;
- RTG and null predictions are reported side by side;
- no claim of physical, quantum, or cosmological validation is made.

## Dataset schema

Each JSON fixture contains:

```json
{
  "event_id": "string",
  "delta_hb": 0.0,
  "necessity": 0.0,
  "threshold_hb": 0.0,
  "threshold_necessity": 0.0,
  "destination_requires_review": true,
  "credential_valid": true,
  "authority_valid": true,
  "freshness_valid": true,
  "destination_identity_valid": true,
  "expected": {
    "operator_instantiated": true,
    "decision": "ALLOW",
    "ingested": true,
    "operator_expired": true,
    "closure_recorded": true,
    "null_triggered": true
  }
}
```

## Advancement rule

Experiment 001 does not validate quantum bridges, wormholes, cosmic fibers, or new physics. It establishes whether the core variables are definable, bounded, machine-testable, and distinguishable from a conventional trigger model. Physical interpretation remains prohibited until later levels produce preregistered predictions against accepted physical null models.
