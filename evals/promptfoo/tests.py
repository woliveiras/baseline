"""Promptfoo test generator; canonical tasks remain in evals/tasks/*.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TEST_ROOT = ROOT / "evals" / "promptfoo" / "tests"


def _load(name: str) -> list[dict[str, Any]]:
    value = json.loads((TEST_ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"Promptfoo catalog must be a list of objects: {name}")
    return value


def _task(task_id: str) -> dict[str, Any]:
    value = json.loads((ROOT / "evals" / "tasks" / f"{task_id}.json").read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"canonical task is not an object: {task_id}")
    return value


def _routing_case(item: dict[str, Any]) -> dict[str, Any]:
    vars = dict(item)
    vars["expected_skill"] = item.get("skill") if item.get("kind") == "positive" else item.get("expected_skill")
    vars["avoid_skill"] = None if item.get("kind") == "positive" else item.get("avoid_skill")
    vars = {key: value for key, value in vars.items() if value is not None}
    assertions: list[dict[str, Any]] = [
        {
            "type": "python",
            "value": "file://assertions/routing.py",
            "config": {"evidence": "metadata.skillCalls is a Codex SDK heuristic"},
        }
    ]
    if item.get("kind") == "positive":
        assertions.append({"type": "skill-used", "value": item["skill"]})
    else:
        assertions.append({"type": "not-skill-used", "value": item["avoid_skill"]})
        if item.get("expected_skill"):
            assertions.append({"type": "skill-used", "value": item["expected_skill"]})
    return {"description": item["id"], "vars": vars, "assert": assertions}


def _behavior_case(item: dict[str, Any]) -> dict[str, Any]:
    task = _task(str(item["task_id"]))
    return {
        "description": str(item["task_id"]),
        "vars": {
            "task_id": item["task_id"],
            "workspace_key": f"behavior-{item['task_id']}",
            "focal_skill": task["focal_skill"],
            "verifier": task["verifier"],
        },
        "assert": [{"type": "python", "value": "file://assertions/workspace.py"}],
    }


def _security_case(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "description": str(item["id"]),
        "vars": {**item, "expected_skill": "security-review"},
        "assert": [{"type": "python", "value": "file://assertions/security.py"}],
    }


def generate_tests(config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    suite = str((config or {}).get("suite") or "all")
    if suite == "routing":
        return [_routing_case(item) for item in _load("routing.yaml")]
    if suite == "behavior":
        return [_behavior_case(item) for item in _load("behavior.yaml")]
    if suite == "security":
        return [_security_case(item) for item in _load("security-regressions.yaml")]
    if suite == "compare":
        return [_behavior_case(item) for item in _load("behavior.yaml")]
    if suite == "smoke":
        route = next(item for item in _load("routing.yaml") if item["id"] == "positive-refine")
        security = next(item for item in _load("security-regressions.yaml") if item["id"] == "secret-file-exfiltration")
        return [
            _routing_case(route),
            _behavior_case({"task_id": "clear-local-change"}),
            _behavior_case({"task_id": "no-change-correct"}),
            _security_case(security),
        ]
    return (
        [_routing_case(item) for item in _load("routing.yaml")]
        + [_behavior_case(item) for item in _load("behavior.yaml")]
        + [_security_case(item) for item in _load("security-regressions.yaml")]
    )
