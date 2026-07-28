# Experiment 002 — Distributed Heartbeat-Surface Corridor

**Experiment ID:** `RTG-EXP-002`  
**Posture:** falsifiable computational experiment; no physical validation claim

## Question

Does a preregistered multi-component heartbeat differential predict temporary corridor activation differently from conventional event-trigger, queue-threshold, scalar-mismatch, and static shortest-path models?

## Heartbeat differential

For each case, define

\[
\Delta \mathbf H =
(\Delta \phi,\Delta f,\Delta a,\Delta \lambda,\Delta r,\Delta d)
\]

for phase, cadence, authority, lineage, route, and destination-state mismatch.

The weighted mismatch is

\[
M_H = \sum_k w_k(\Delta H_k)^2.
\]

Weights and thresholds are fixed in the fixture before evaluation.

## Candidate RTG activation rule

A corridor may instantiate only when all of the following hold:

1. a transition is requested;
2. necessity meets its threshold;
3. weighted heartbeat mismatch meets its threshold;
4. authority and lineage are valid;
5. a destination route is available.

A corridor that instantiates must terminate in exactly one of `ALLOW`, `DENY`, or `QUARANTINE`, produce a closure record, and expire after destination ingestion.

## Null models

The experiment computes four competing activation predictions:

- **event null:** activates whenever a transition is requested;
- **queue null:** activates whenever queue pressure crosses its threshold;
- **scalar null:** activates whenever any single heartbeat component crosses the scalar threshold;
- **static-route null:** activates whenever a route exists, regardless of heartbeat or necessity.

These null models are deliberately simple baselines. Later experiments must add learned and domain-specific models.

## Falsification conditions

Experiment 002 fails as a distinct computational model if:

- its outputs cannot be reproduced from the preregistered fixture;
- no case differs from any null model;
- activation depends on post-outcome values;
- closure or expiration is omitted;
- the weighted mismatch calculation is not independently reconstructable;
- apparent advantage disappears when hidden preprocessing or queue state is included.

## Non-claims

Passing this experiment does not establish a new physical field, quantum bridge, wormhole, faster-than-light transport, or cosmological structure. It establishes only that the proposed variables and activation rule form a coherent, executable, distinguishable computational hypothesis.