#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, importlib.util, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_loop(manifest_path: Path, solver_results_path: Path, output_path: Path) -> Path:
    dispatch_mod = load_module("dispatch", ROOT / "scripts" / "build_rtg_math_solver_dispatch_packet.py")
    contract_mod = load_module("contract", ROOT / "scripts" / "validate_rtg_math_solver_interface_contract.py")
    status_mod = load_module("status", ROOT / "scripts" / "track_rtg_math_solver_execution_status.py")
    return_mod = load_module("return_mod", ROOT / "scripts" / "return_rtg_solver_results.py")

    work = output_path.parent
    work.mkdir(parents=True, exist_ok=True)
    dispatch_path = work / "rtg_math_solver_dispatch_packet.json"
    contract_path = work / "rtg_math_solver_interface_contract.json"
    status_path = work / "rtg_math_solver_execution_status.json"
    returned_path = work / "rtg_solver_result_return.json"

    dispatch_mod.build_packet(manifest_path, dispatch_path)
    contract_mod.validate_contract(dispatch_path, contract_path)
    status_mod.track(dispatch_path, status_path, solver_results_path, dispatched=True, failed=False)
    return_mod.return_results(status_path, solver_results_path, returned_path)

    dispatch = json.loads(dispatch_path.read_text(encoding="utf-8"))
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    status = json.loads(status_path.read_text(encoding="utf-8"))
    returned = json.loads(returned_path.read_text(encoding="utf-8"))

    loop = {
        "schema_version": "1.0",
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_repo": "Data-Continuation/RTG-Tests",
        "loop_surface": "rtg_end_to_end_solver_loop",
        "loop_steps": [
            "dispatch_packet_created",
            "interface_contract_validated",
            "execution_status_observed",
            "solver_result_returned",
        ],
        "loop_status": "solver_loop_ready_for_ingestion" if (
            contract.get("summary", {}).get("contract_posture") == "interface_contract_valid"
            and status.get("execution_status") == "solver_results_available"
            and returned.get("return_status") == "return_ready_for_ingestion"
        ) else "solver_loop_review",
        "artifacts": {
            "dispatch_packet": dispatch_path.as_posix(),
            "interface_contract": contract_path.as_posix(),
            "execution_status": status_path.as_posix(),
            "solver_result_return": returned_path.as_posix(),
        },
        "summary": {
            "case_count": dispatch.get("case_count", 0),
            "result_count": returned.get("result_count", 0),
            "loop_posture": "solver_loop_ready_for_ingestion" if returned.get("return_status") == "return_ready_for_ingestion" else "solver_loop_review",
        },
        "receipt": {
            "manifest_sha256": sha256_file(manifest_path),
            "solver_results_sha256": sha256_file(solver_results_path),
            "dispatch_packet_sha256": sha256_file(dispatch_path),
            "contract_sha256": sha256_file(contract_path),
            "execution_status_sha256": sha256_file(status_path),
            "solver_result_return_sha256": sha256_file(returned_path),
        },
    }
    output_path.write_text(json.dumps(loop, indent=2) + "\n", encoding="utf-8")
    return output_path

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", required=True)
    p.add_argument("--solver-results", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    print("Wrote RTG end-to-end solver loop: " + str(run_loop(Path(a.manifest), Path(a.solver_results), Path(a.output))))

if __name__ == "__main__":
    main()
