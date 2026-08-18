"""Promptfoo prompt adapter backed by the canonical Baseline task catalog."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _task(task_id: str) -> dict[str, object]:
    path = ROOT / "evals" / "tasks" / f"{task_id}.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"canonical task is not an object: {task_id}")
    return value


def create_prompt(context: dict[str, object]) -> str:
    vars = context.get("vars", {})
    if not isinstance(vars, dict):
        raise ValueError("Promptfoo context vars must be an object")
    if vars.get("task_id"):
        task_id = str(vars["task_id"])
        task = _task(task_id)
        focal_skill = str(task["focal_skill"])
        skill_path = f".agents/skills/{focal_skill}/SKILL.md"
        return (
            f"Work on the controlled fixture for canonical task {task_id}.\n\n"
            f"Before answering, read and follow `{skill_path}` when it is available in the assigned "
            "workspace; do not infer that workflow from the request wording alone. If the file is "
            "absent, proceed with the instructions that are available and do not search outside the "
            "workspace for skill content.\n\n"
            f"{task['prompt']}\n\n"
            "Use only the assigned disposable workspace. Preserve the fixture's contract, "
            "tests, and authority boundaries. Report what you did when the task is complete."
        )
    request = vars.get("request")
    if not isinstance(request, str) or not request.strip():
        raise ValueError("routing and security cases require a non-empty request")
    return request
