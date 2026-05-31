#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "config" / "rtg_declared_tasks.json"
def main():
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    tasks = registry.get("tasks")
    if not isinstance(tasks, list) or not tasks: raise AssertionError("registry tasks must be non-empty")
    names, by_name = [], {}
    for task in tasks:
        for field in ["name","description","enabled","command"]:
            if field not in task: raise AssertionError(f"task missing {field}")
        if not isinstance(task["enabled"], bool): raise AssertionError(f"{task['name']} enabled must be boolean")
        command = task["command"]
        if not isinstance(command, list) or len(command) != 2: raise AssertionError(f"{task['name']} command shape invalid")
        if command[0] != "python": raise AssertionError(f"{task['name']} command must start with python")
        rel = command[1]
        if rel.startswith("/") or ".." in Path(rel).parts: raise AssertionError(f"{task['name']} command path unsafe")
        if not (rel.startswith("tests/") or rel.startswith("scripts/")): raise AssertionError(f"{task['name']} command path must start with tests/ or scripts/")
        if not (ROOT / rel).exists(): raise AssertionError(f"{task['name']} references missing file: {rel}")
        if task["name"].endswith("_tests") and not rel.startswith("tests/"): raise AssertionError(f"{task['name']} must reference tests/")
        names.append(task["name"]); by_name[task["name"]] = task
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes: raise AssertionError(f"duplicate task names: {dupes}")
    if by_name.get("fixture_smoke_tests", {}).get("command") != ["python","tests/test_rtg_fixtures.py"]: raise AssertionError("fixture_smoke_tests canonical path drift")
    if (ROOT / "tests" / "test_fixture_smoke.py").exists(): raise AssertionError("undocumented fixture smoke compatibility path exists")
    if by_name.get("dispatcher_self_check", {}).get("command") != ["python","scripts/verify_rtg_dispatcher.py"]: raise AssertionError("dispatcher self-check path drift")
    print("RTG registry task file integrity tests passed.")
if __name__ == "__main__":
    main()
