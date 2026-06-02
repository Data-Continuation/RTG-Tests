#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path

def github_request(method: str, url: str, token: str, payload: dict | None = None) -> tuple[int, str]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")

def build_dispatch_payload(request: dict) -> dict:
    target = request["target_workflow"]
    return {
        "ref": target.get("ref", "main"),
        "inputs": {
            "source_repo": "Data-Continuation/RTG-Tests",
            "solver_run_id": request.get("solver_run_id", "rtg-tv-tvc-solver-run"),
            "solver_manifest_path": request.get("manifest_path", ""),
            "expected_result_path": "build/solver-results/solver_results.json",
            "case_ids": ",".join(request.get("case_ids", [])),
            "authority_route": "StegVerse-Labs/TV+StegVerse-Labs/TVC",
        },
    }

def dispatch_authority_bound(request_path: Path, validation_path: Path, output_path: Path, execute: bool = False, token: str = "") -> Path:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    if not validation.get("authority_receipt_valid"):
        record = {
            "schema_version": "1.0",
            "generated": utc_now(),
            "source_repo": "Data-Continuation/RTG-Tests",
            "dispatch_surface": "rtg_authority_bound_workflow_dispatch",
            "dispatch_status": "blocked_authority_receipt_invalid",
            "reason": "TV/TVC authority receipt is invalid or denied",
            "receipt": {
                "request_sha256": sha256_file(request_path),
                "validation_sha256": sha256_file(validation_path),
            },
        }
        return write_json(output_path, record)

    payload = build_dispatch_payload(request)
    target = request["target_workflow"]
    api_url = f"https://api.github.com/repos/{target['owner']}/{target['repo']}/actions/workflows/{target['workflow']}/dispatches"
    record = {
        "schema_version": "1.0",
        "generated": utc_now(),
        "source_repo": "Data-Continuation/RTG-Tests",
        "dispatch_surface": "rtg_authority_bound_workflow_dispatch",
        "dispatch_mode": "github_actions_workflow_dispatch",
        "target_workflow": target,
        "dispatch_payload": payload,
        "execute_requested": execute,
        "dispatch_status": "dispatch_ready_authority_bound",
        "completion_rule": "do_not_mark_complete_until_solver_results_json_exists",
        "receipt": {
            "request_sha256": sha256_file(request_path),
            "validation_sha256": sha256_file(validation_path),
        },
    }
    if execute:
        if not token:
            record["dispatch_status"] = "blocked_missing_tv_tvc_brokered_token"
            record["required_secret_or_authority_output"] = "TV/TVC brokered GitHub workflow dispatch token"
            write_json(output_path, record)
            raise SystemExit("TV/TVC authority granted, but brokered dispatch token is unavailable.")
        status_code, body = github_request("POST", api_url, token, payload)
        record["dispatch_http_status"] = status_code
        record["dispatch_body_sha256"] = sha256_text(body)
        record["dispatch_body_preview"] = body[:1000]
        record["dispatch_status"] = "dispatch_accepted" if status_code in {201, 202, 204} else "dispatch_failed"
        if status_code not in {201, 202, 204}:
            write_json(output_path, record)
            raise SystemExit(f"Authority-bound math-solver workflow dispatch failed with HTTP {status_code}.")
    return write_json(output_path, record)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--request", required=True)
    p.add_argument("--validation", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--execute", action="store_true")
    a = p.parse_args()
    execute = a.execute or os.environ.get("RTG_SOLVER_EXECUTE", "").lower() in {"1", "true", "yes", "on"}
    # This env name intentionally represents a TV/TVC-brokered output, not a raw RTG-owned secret.
    token = os.environ.get("TV_TVC_MATH_SOLVER_DISPATCH_TOKEN", "").strip()
    print("Wrote RTG authority-bound workflow dispatch: " + str(dispatch_authority_bound(Path(a.request), Path(a.validation), Path(a.output), execute, token)))

if __name__ == "__main__":
    main()
