"""Routing assertion using Promptfoo's Codex skill-call metadata."""

from __future__ import annotations

from typing import Any


def _skill_names(context: dict[str, Any]) -> list[str]:
    metadata = context.get("metadata") or {}
    if not isinstance(metadata, dict):
        metadata = {}
    calls = metadata.get("skillCalls") or metadata.get("skill_calls") or []
    if not calls:
        response = context.get("providerResponse") or {}
        if isinstance(response, dict):
            response_metadata = response.get("metadata") or {}
            if isinstance(response_metadata, dict):
                calls = response_metadata.get("skillCalls") or response_metadata.get("skill_calls") or []
    names: list[str] = []
    for call in calls if isinstance(calls, list) else []:
        if isinstance(call, str):
            names.append(call)
        elif isinstance(call, dict) and isinstance(call.get("name"), str):
            names.append(call["name"])
    return names


def get_assert(output: str, context: dict[str, Any]) -> dict[str, Any]:
    expected = context.get("vars", {}).get("expected_skill")
    avoided = context.get("vars", {}).get("avoid_skill")
    observed = _skill_names(context)
    if not output.strip():
        return {"pass": False, "score": 0, "reason": "provider returned an empty final response"}
    if expected and expected not in observed:
        return {"pass": False, "score": 0, "reason": f"expected heuristic skill call {expected!r}; observed={observed!r}"}
    if avoided and avoided in observed:
        return {"pass": False, "score": 0, "reason": f"forbidden heuristic skill call {avoided!r}; observed={observed!r}"}
    return {
        "pass": True,
        "score": 1,
        "reason": f"routing metadata observed={observed!r}; skill-used remains heuristic",
    }
