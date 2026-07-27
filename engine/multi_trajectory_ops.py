"""Executable operators for provisional multi-trajectory RTG tests.

These functions are deterministic reference operators, not proof claims.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable, List, Mapping, Sequence


SIGNIFICANCE_CLASSES = {"active", "supporting", "latent", "discardable"}


def weighted_significance(components: Mapping[str, float], weights: Mapping[str, float]) -> float:
    """Return the bounded weighted significance score for one transition."""
    score = sum(float(components.get(name, 0.0)) * float(weight) for name, weight in weights.items())
    return max(0.0, min(1.0, round(score, 12)))


def classify_transition(score: float, threshold: float, supporting: bool = False, latent: bool = False) -> str:
    """Classify one transition under a contextual threshold."""
    if score >= threshold:
        return "active"
    if supporting:
        return "supporting"
    if latent:
        return "latent"
    return "discardable"


def constellation_activation(member_scores: Sequence[float], member_weights: Sequence[float], threshold: float) -> Dict[str, Any]:
    """Evaluate whether individually weak transitions activate collectively."""
    if len(member_scores) != len(member_weights):
        raise ValueError("member_scores and member_weights must have equal length")
    aggregate = round(sum(float(s) * float(w) for s, w in zip(member_scores, member_weights)), 12)
    return {
        "aggregate": aggregate,
        "threshold": float(threshold),
        "activated": aggregate >= threshold,
        "individually_subthreshold": all(float(score) < threshold for score in member_scores),
    }


def relational_density(nodes: Sequence[str], couplings: Sequence[Mapping[str, Any]]) -> float:
    """Return undirected edge density over a bounded transition region."""
    unique_nodes = set(nodes)
    count = len(unique_nodes)
    if count < 2:
        return 0.0
    possible = count * (count - 1) / 2
    edges = {
        tuple(sorted((str(edge["source"]), str(edge["target"]))))
        for edge in couplings
        if edge.get("source") in unique_nodes and edge.get("target") in unique_nodes and edge.get("source") != edge.get("target")
    }
    return round(len(edges) / possible, 12)


def transition_block_state(
    nodes: Sequence[str],
    couplings: Sequence[Mapping[str, Any]],
    formation_threshold: float,
    goal_resolved: bool = False,
    expired: bool = False,
    current_coupling_minimum: float = 0.0,
) -> Dict[str, Any]:
    """Form or dissolve a transition block using relational closure conditions."""
    density = relational_density(nodes, couplings)
    formed = density >= formation_threshold and not expired
    dissolved = bool(goal_resolved or expired or density < current_coupling_minimum)
    return {
        "density": density,
        "formed": formed and not dissolved,
        "dissolved": dissolved,
        "reason": (
            "goal_resolved" if goal_resolved else
            "expired" if expired else
            "coupling_below_minimum" if density < current_coupling_minimum else
            "formed" if formed else
            "insufficient_density"
        ),
    }


def decision_signature(decisions: Iterable[Mapping[str, Any]]) -> str:
    """Create a stable signature for decision-relevant outputs."""
    canonical = json.dumps(list(decisions), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def compression_is_decision_preserving(
    original_decisions: Iterable[Mapping[str, Any]],
    compressed_decisions: Iterable[Mapping[str, Any]],
) -> bool:
    """Return true only when compression leaves decision outputs unchanged."""
    return decision_signature(original_decisions) == decision_signature(compressed_decisions)


def deterministic_receipt(payload: Mapping[str, Any]) -> Dict[str, Any]:
    """Create a deterministic, replayable receipt from canonical JSON."""
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return {
        "receipt_version": "rtg-mt-v0.1",
        "hash_algorithm": "sha256",
        "canonical_payload": canonical,
        "receipt_hash": digest,
    }
