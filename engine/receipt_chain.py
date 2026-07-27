"""Deterministic JSONL receipt-chain helpers for provisional RTG tests."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Iterable, Mapping

GENESIS_HASH = "0" * 64


def canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def chain_receipt(payload: Mapping[str, Any], previous_hash: str = GENESIS_HASH) -> dict[str, Any]:
    if len(previous_hash) != 64:
        raise ValueError("previous_hash must be a 64-character hexadecimal digest")
    canonical_payload = canonical_json(payload)
    material = f"{previous_hash}:{canonical_payload}"
    receipt_hash = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return {
        "receipt_version": "rtg-chain-v0.1",
        "hash_algorithm": "sha256",
        "previous_hash": previous_hash,
        "canonical_payload": canonical_payload,
        "receipt_hash": receipt_hash,
    }


def build_receipt_chain(payloads: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    previous_hash = GENESIS_HASH
    for payload in payloads:
        receipt = chain_receipt(payload, previous_hash)
        receipts.append(receipt)
        previous_hash = receipt["receipt_hash"]
    return receipts


def verify_receipt_chain(receipts: Iterable[Mapping[str, Any]]) -> bool:
    previous_hash = GENESIS_HASH
    for receipt in receipts:
        if receipt.get("previous_hash") != previous_hash:
            return False
        canonical_payload = receipt.get("canonical_payload")
        if not isinstance(canonical_payload, str):
            return False
        material = f"{previous_hash}:{canonical_payload}"
        expected = hashlib.sha256(material.encode("utf-8")).hexdigest()
        if receipt.get("receipt_hash") != expected:
            return False
        previous_hash = expected
    return True


def receipts_to_jsonl(receipts: Iterable[Mapping[str, Any]]) -> str:
    return "\n".join(canonical_json(receipt) for receipt in receipts) + "\n"
