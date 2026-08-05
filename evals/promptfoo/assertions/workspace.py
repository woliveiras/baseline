"""Workspace assertion adapter that delegates behavior to evals/verifiers.py."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "evals"))
from run import root_fingerprint  # noqa: E402
from verifiers import changed_paths, snapshot, verify  # noqa: E402


CONDITIONS = ("baseline", "core", "focal", "broad", "current", "proposed")


def _manifest() -> dict[str, Any]:
    path = os.environ.get("TUXEDO_EVAL_MANIFEST")
    if not path:
        raise AssertionError("TUXEDO_EVAL_MANIFEST is not configured")
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError("evaluation manifest is not an object")
    return value


def _provider_label(context: dict[str, Any]) -> str:
    provider = context.get("provider")
    candidates: list[str] = []
    if isinstance(provider, str):
        candidates.append(provider)
    elif isinstance(provider, dict):
        for key in ("label", "id", "name"):
            value = provider.get(key)
            if isinstance(value, str):
                candidates.append(value)
    for candidate in candidates:
        for condition in CONDITIONS:
            if candidate == condition or candidate.endswith(f":{condition}") or condition in candidate:
                return condition
    return "current"


def _protected_failures(workspace: Path, entry: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    for relative, expected in (entry.get("protected_hashes") or {}).items():
        path = workspace / relative
        observed = __import__("hashlib").sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if observed != expected:
            failures.append(f"protected file changed: {relative}")
    return failures


def get_assert(output: str, context: dict[str, Any]) -> dict[str, Any]:
    if not output.strip():
        return {"pass": False, "score": 0, "reason": "provider returned an empty final response"}
    vars = context.get("vars") or {}
    key = str(vars.get("workspace_key", ""))
    task_id = str(vars.get("task_id", ""))
    condition = _provider_label(context)
    manifest = _manifest()
    entry = ((manifest.get("workspaces") or {}).get(key) or {}).get(condition)
    if not isinstance(entry, dict):
        return {"pass": False, "score": 0, "reason": f"missing workspace manifest entry for {key}/{condition}"}
    workspace = Path(str(entry["path"]))
    before = entry.get("before")
    if not workspace.is_dir() or not isinstance(before, dict):
        return {"pass": False, "score": 0, "reason": "workspace or before snapshot is missing"}
    task = json.loads((ROOT / "evals" / "tasks" / f"{task_id}.json").read_text(encoding="utf-8"))
    result = verify(task, workspace, before)
    failures = [item["id"] for item in result["checks"] if not item["pass"]]
    failures.extend(_protected_failures(workspace, entry))
    if failures:
        return {
            "pass": False,
            "score": 0,
            "reason": f"deterministic verifier failures={failures}; changed={result['changed_paths']}",
        }
    if result["status"] == "needs-review":
        if vars.get("secondary_review_attached") is True:
            return {
                "pass": True,
                "score": 1,
                "reason": f"deterministic checks passed; secondary rubric attached; condition={condition}; changed={result['changed_paths']}",
            }
        return {
            "pass": False,
            "score": 0,
            "needs_review": True,
            "reason": f"secondary review is pending; condition={condition}; changed={result['changed_paths']}",
        }
    return {
        "pass": True,
        "score": 1,
        "reason": f"reused evals/verifiers.py; condition={condition}; changed={result['changed_paths']}",
    }
