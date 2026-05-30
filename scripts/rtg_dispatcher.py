#!/usr/bin/env python3
"""Repo-local dispatcher for declared RTG test tasks.

This dispatcher intentionally runs only commands declared in
config/rtg_declared_tasks.json.

It does not call other repositories, mutate repository contents, or use secrets.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "config" / "rtg_declared_tasks.json"

ALLOWED_EXECUTABLES = {"python", "python3"}


@dataclass(frozen=True)
class Task:
    name: str
    description: str
    enabled: bool
    command: list[str]


def load_registry() -> dict[str, Any]:
    if not TASKS_PATH.exists():
        raise SystemExit(f"Missing task registry: {TASKS_PATH.relative_to(ROOT)}")

    with TASKS_PATH.open("r", encoding="utf-8") as handle:
        registry = json.load(handle)

    if not isinstance(registry, dict):
        raise SystemExit("Task registry must be a JSON object.")

    if registry.get("posture") != "repo-local-only":
        raise SystemExit("Task registry posture must be repo-local-only.")

    return registry


def parse_tasks(registry: dict[str, Any]) -> dict[str, Task]:
    raw_tasks = registry.get("tasks")

    if not isinstance(raw_tasks, list) or not raw_tasks:
        raise SystemExit("Task registry must contain a non-empty tasks list.")

    tasks: dict[str, Task] = {}

    for index, raw_task in enumerate(raw_tasks):
        if not isinstance(raw_task, dict):
            raise SystemExit(f"Task at index {index} must be an object.")

        name = raw_task.get("name")
        description = raw_task.get("description")
        enabled = raw_task.get("enabled")
        command = raw_task.get("command")

        if not isinstance(name, str) or not name:
            raise SystemExit(f"Task at index {index} has invalid name.")

        if name in tasks:
            raise SystemExit(f"Duplicate task name: {name}")

        if not isinstance(description, str):
            raise SystemExit(f"Task {name} has invalid description.")

        if not isinstance(enabled, bool):
            raise SystemExit(f"Task {name} has invalid enabled value.")

        if not isinstance(command, list) or not command:
            raise SystemExit(f"Task {name} has invalid command.")

        if not all(isinstance(part, str) and part for part in command):
            raise SystemExit(f"Task {name} command must contain only non-empty strings.")

        if command[0] not in ALLOWED_EXECUTABLES:
            raise SystemExit(
                f"Task {name} uses unsupported executable {command[0]!r}. "
                f"Allowed: {sorted(ALLOWED_EXECUTABLES)}"
            )

        tasks[name] = Task(
            name=name,
            description=description,
            enabled=enabled,
            command=command,
        )

    return tasks


def selected_tasks(tasks: dict[str, Task], requested_task: str) -> list[Task]:
    enabled_tasks = [task for task in tasks.values() if task.enabled]

    if requested_task == "all":
        return enabled_tasks

    task = tasks.get(requested_task)
    if task is None:
        valid = ", ".join(["all", *sorted(tasks)])
        raise SystemExit(f"Unknown task: {requested_task}. Valid tasks: {valid}")

    if not task.enabled:
        raise SystemExit(f"Task is declared but disabled: {requested_task}")

    return [task]


def run_task(task: Task, dry_run: bool) -> None:
    command_text = " ".join(task.command)
    print(f"::group::{task.name}")
    print(f"description: {task.description}")
    print(f"command: {command_text}")

    if dry_run:
        print("dry_run: true")
        print(f"::endgroup::")
        return

    result = subprocess.run(task.command, cwd=ROOT, text=True)

    if result.returncode != 0:
        print(f"::endgroup::")
        raise SystemExit(result.returncode)

    print(f"status: passed")
    print(f"::endgroup::")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run declared RTG repo-local tasks.")
    parser.add_argument("--task", default="all", help="Declared task name or 'all'.")
    parser.add_argument("--dry-run", action="store_true", help="Print selected tasks without running.")
    parser.add_argument("--list", action="store_true", help="List declared tasks and exit.")
    args = parser.parse_args()

    registry = load_registry()
    tasks = parse_tasks(registry)

    if args.list:
        for task in tasks.values():
            status = "enabled" if task.enabled else "disabled"
            print(f"{task.name}\t{status}\t{task.description}")
        return

    for task in selected_tasks(tasks, args.task):
        run_task(task, args.dry_run)

    print("RTG repo dispatcher completed.")


if __name__ == "__main__":
    main()
