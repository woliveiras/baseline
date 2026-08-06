"""Workspace assertion adapter that delegates behavior to evals/verifiers.py."""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "evals"))
from run import root_fingerprint  # noqa: E402
from verifiers import changed_paths, snapshot, verify  # noqa: E402


CONDITIONS = ("baseline", "core", "focal", "broad", "current", "proposed")
_TRACE_IGNORED_KEYS = {
    "aggregated_output", "output", "text", "message", "reasoning", "prompt",
    "input", "request", "response", "insights",
}
_READ_ONLY_COMMANDS = {"cat", "cut", "file", "find", "grep", "head", "jq", "ls", "nl", "pwd", "rg", "sed", "shasum", "sort", "stat", "tail", "true", "uniq", "wc"}
_READ_ONLY_GIT_COMMANDS = {"diff", "log", "ls-files", "ls-tree", "rev-parse", "show", "status"}


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


def _json_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def _trajectory_sources(context: dict[str, Any]) -> list[Any]:
    sources: list[Any] = []
    if context.get("trace") is not None:
        sources.append(context["trace"])
    provider_response = context.get("providerResponse")
    if isinstance(provider_response, dict):
        for key in ("raw", "trace", "traceContext"):
            if provider_response.get(key) is not None:
                sources.append(provider_response[key])
    return [_json_value(source) for source in sources]


def _structured_events(value: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if isinstance(value, dict):
        if value.get("type") in {"command_execution", "file_change", "mcp_tool_call", "web_search"}:
            events.append(value)
        attributes = value.get("attributes")
        if isinstance(attributes, dict) and isinstance(attributes.get("codex.command"), str):
            events.append({"type": "command_execution", "command": attributes["codex.command"]})
        for key, child in value.items():
            if key not in _TRACE_IGNORED_KEYS and key != "attributes":
                events.extend(_structured_events(child))
    elif isinstance(value, list):
        for child in value:
            events.extend(_structured_events(child))
    return events


def _command_segments(command: str) -> list[list[str]]:
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return []
    segments: list[list[str]] = []
    current: list[str] = []
    for token in [*tokens, ";"]:
        if token in {";", "&&", "||", "|"}:
            if current:
                while current and (current[0] in {"env", "sudo", "command", "time"} or ("=" in current[0] and not current[0].startswith("="))):
                    current = current[1:]
                if current:
                    segments.append(current)
            current = []
        else:
            current.append(token)
    return segments


def _read_only_trajectory(context: dict[str, Any]) -> tuple[list[str], bool]:
    events = [event for source in _trajectory_sources(context) if source is not None for event in _structured_events(source)]
    if not events:
        return [], False
    violations: list[str] = []
    for event in events:
        if event.get("type") != "command_execution":
            continue
        command = event.get("command")
        if not isinstance(command, str):
            continue
        segments = _command_segments(command)
        if not segments:
            violations.append("unparseable command")
            continue
        pending = list(segments)
        while pending:
            segment = pending.pop(0)
            executable = Path(segment[0]).name.lower()
            arguments = segment[1:]
            if executable in {"bash", "dash", "sh", "zsh"}:
                command_index = next((index for index, arg in enumerate(arguments) if arg.startswith("-") and "c" in arg[1:]), None)
                if command_index is None or command_index + 1 >= len(arguments):
                    violations.append(f"non-read-only shell invocation: {executable}")
                else:
                    nested = _command_segments(arguments[command_index + 1])
                    if nested:
                        pending[0:0] = nested
                    else:
                        violations.append(f"unparseable shell payload: {executable}")
            elif executable == "git":
                subcommand = next((arg for arg in arguments if not arg.startswith("-")), "")
                branch_is_read_only = subcommand == "branch" and any(arg in {"--list", "--show-current"} for arg in arguments)
                if subcommand not in _READ_ONLY_GIT_COMMANDS and not branch_is_read_only:
                    violations.append(f"non-read-only Git command: {subcommand or '<missing>'}")
            elif executable == "sed" and any(arg == "-i" or arg.startswith("-i") for arg in arguments):
                violations.append("mutating sed command")
            elif executable == "find":
                if "-delete" in arguments or any(arg in {"-ok", "-okdir"} for arg in arguments):
                    violations.append("mutating find command")
                execution_index = next((index for index, arg in enumerate(arguments) if arg in {"-exec", "-execdir"}), None)
                if execution_index is not None:
                    nested = [arg for arg in arguments[execution_index + 1:] if arg not in {"{}", "+", ";"}]
                    if nested:
                        pending.insert(0, nested)
                    else:
                        violations.append("unparseable find execution")
            elif executable not in _READ_ONLY_COMMANDS:
                violations.append(f"non-read-only command: {executable}")
    return sorted(set(violations)), True


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
    if task.get("execution_policy") == "read-only-inspection":
        trajectory_failures, trajectory_available = _read_only_trajectory(context)
        if trajectory_failures:
            return {
                "pass": False,
                "score": 0,
                "reason": f"read-only execution policy violated: {trajectory_failures}",
            }
        if not trajectory_available:
            return {
                "pass": False,
                "score": 0,
                "needs_review": True,
                "reason": "needs-review: provider did not expose structured trajectory events for read-only execution policy",
            }
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
