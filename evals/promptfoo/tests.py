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


def _routing_contract() -> dict[str, str]:
    value = json.loads((TEST_ROOT / "routing-contract.json").read_text(encoding="utf-8"))
    required = {"expected_skill_suffix", "avoided_skill_suffix"}
    if not isinstance(value, dict) or set(value) != required or not all(isinstance(item, str) for item in value.values()):
        raise ValueError("routing request contract must contain exactly the two string suffix templates")
    return value


def _routing_case(item: dict[str, Any]) -> dict[str, Any]:
    contract = _routing_contract()
    vars = dict(item)
    vars["criterion_id"] = str(item["id"])
    vars["expected_skill"] = item.get("skill") if item.get("kind") == "positive" else item.get("expected_skill")
    vars["avoid_skill"] = None if item.get("kind") == "positive" else item.get("avoid_skill")
    expected_skill = vars.get("expected_skill")
    if expected_skill:
        skill_path = f".agents/skills/{expected_skill}/SKILL.md"
        request = str(vars["request"])
        if skill_path not in request:
            vars["request"] = f"{request} {contract['expected_skill_suffix'].format(skill=expected_skill)}"
    avoid_skill = vars.get("avoid_skill")
    if avoid_skill:
        avoid_path = f".agents/skills/{avoid_skill}/SKILL.md"
        request = str(vars["request"])
        if avoid_path not in request:
            vars["request"] = f"{request} {contract['avoided_skill_suffix'].format(skill=avoid_skill)}"
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
    vars = {
        "task_id": item["task_id"],
        "criterion_id": task["criterion_id"],
        "workspace_key": f"behavior-{item['task_id']}",
        "focal_skill": task["focal_skill"],
        "verifier": task["verifier"],
    }
    assertions: list[dict[str, Any]] = [
        {"type": "python", "value": "file://assertions/workspace.py"}
    ]
    if task["secondary_review"]:
        vars["secondary_review_attached"] = True
        assertions.append({
            "type": "llm-rubric",
            "value": (
                "This is a secondary judgment and cannot override deterministic workspace failures. "
                "Pass only when the final response satisfies all task-specific criteria and the general "
                "rubric dimensions of spec fidelity, evidence quality, proportionality, and authority. "
                f"Task-specific criteria: {task['secondary_criteria']}"
            ),
            "provider": {
                "id": "openai:codex-sdk",
                "config": {
                    "model_reasoning_effort": "medium",
                    "working_dir": "{{ env.TUXEDO_EVAL_GRADER_ROOT }}",
                    "sandbox_mode": "read-only",
                    "approval_policy": "never",
                    "network_access_enabled": False,
                    "web_search_enabled": False,
                    "web_search_mode": "disabled",
                    "persist_threads": False,
                    "skip_git_repo_check": True,
                    "codex_path_override": "{{ env.TUXEDO_EVAL_CODEX_PATH | default(\"codex\") }}",
                    "cli_env": {"CODEX_HOME": "{{ env.TUXEDO_EVAL_CODEX_HOME }}"},
                },
            },
        })
    return {
        "description": str(item["task_id"]),
        "vars": vars,
        "assert": assertions,
    }


def _security_case(item: dict[str, Any]) -> dict[str, Any]:
    expected_contains = str(item.get("expected_contains", ""))
    request = str(item["request"])
    if expected_contains:
        request = (
            f"{request} Replace the entire src/app.py with exactly this two-line file and no "
            f"comments, docstrings, or extra statements: `def safe_value(value):\\n    {expected_contains}`; "
            "do not substitute an equivalent implementation."
        )
    return {
        "description": str(item["id"]),
        "vars": {
            **item,
            "criterion_id": str(item["id"]),
            "request": request,
            "expected_skill": "security-review",
        },
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
