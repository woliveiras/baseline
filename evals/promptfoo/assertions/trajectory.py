"""Fail-closed helpers for structured Codex tool trajectories."""

from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import Any


TRACE_EVENT_TYPES = {
    "command_execution",
    "file_change",
    "mcp_tool_call",
    "web_search",
    "collaboration_tool_call",
    "spawn_agent",
}
TRACE_IGNORED_KEYS = {
    "aggregated_output", "output", "text", "message", "reasoning", "prompt",
    "input", "request", "response", "insights",
}
_SHELLS = {"bash", "dash", "sh", "zsh"}
_UNSAFE_SYNTAX = ("`", "$(", "\n", "\r")
_SEPARATORS = {";", "&&", "||", "|"}
_UNSUPPORTED_SEPARATORS = {"&", ";;", "|&", ";&", ";;&"}


def json_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def trajectory_sources(context: dict[str, Any]) -> list[Any]:
    sources: list[Any] = []
    if context.get("trace") is not None:
        sources.append(context["trace"])
    provider_response = context.get("providerResponse")
    if isinstance(provider_response, dict):
        for key in ("raw", "trace", "traceContext"):
            if provider_response.get(key) is not None:
                sources.append(provider_response[key])
    return [json_value(source) for source in sources]


def structured_events(value: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    if isinstance(value, dict):
        event_type = value.get("type")
        if event_type in TRACE_EVENT_TYPES:
            events.append(value)
        attributes = value.get("attributes")
        if isinstance(attributes, dict):
            command = attributes.get("codex.command")
            if isinstance(command, str):
                events.append({"type": "command_execution", "command": command})
            files = attributes.get("codex.files")
            if isinstance(files, str):
                events.append({
                    "type": "file_change",
                    "changes": [{"path": path.strip()} for path in files.split(",")],
                })
        for key, child in value.items():
            if key not in TRACE_IGNORED_KEYS and key != "attributes":
                events.extend(structured_events(child))
    elif isinstance(value, list):
        for child in value:
            events.extend(structured_events(child))
    return events


def events_from_context(context: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        event
        for source in trajectory_sources(context)
        if source is not None
        for event in structured_events(source)
    ]


def _strip_prefix(tokens: list[str]) -> list[str]:
    current = list(tokens)
    while current and ("=" in current[0] and not current[0].startswith("=")):
        current.pop(0)
    if current and current[0] == "command":
        current.pop(0)
    if current and current[0] == "env":
        current.pop(0)
        while current and (current[0].startswith("-") or "=" in current[0]):
            current.pop(0)
    return current


def command_segments(command: str) -> tuple[list[list[str]], list[str]]:
    """Return recursively unwrapped argv segments plus fail-closed parse errors."""
    violations = [f"unsafe command syntax: {token!r}" for token in _UNSAFE_SYNTAX if token in command]
    if violations:
        return [], violations
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|<>")
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return [], ["unparseable command"]
    filtered: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in {">", ">>"}:
            if filtered and filtered[-1].isdigit():
                filtered.pop()
            if index + 1 >= len(tokens) or tokens[index + 1] != "/dev/null":
                violations.append("unsafe output redirection")
            index += 2
            continue
        if "<" in token or token in {">&", "<&"}:
            violations.append("unsafe input or descriptor redirection")
            index += 1
            continue
        filtered.append(token)
        index += 1
    tokens = filtered
    segments: list[list[str]] = []
    current: list[str] = []
    raw_segments: list[list[str]] = []
    for token in [*tokens, ";"]:
        if token in _UNSUPPORTED_SEPARATORS:
            violations.append(f"unsupported command separator: {token}")
            current = []
        elif token in _SEPARATORS:
            if current:
                raw_segments.append(current)
            current = []
        else:
            current.append(token)
    for raw in raw_segments:
        segment = _strip_prefix(raw)
        if not segment:
            violations.append("command has no executable")
            continue
        if segment[0] == "for":
            if len(segment) < 4 or segment[2] != "in":
                violations.append("unsupported shell for-loop")
            continue
        if segment[0] == "do":
            segment = segment[1:]
            if not segment:
                violations.append("shell do has no command")
                continue
        if segment[0] == "done":
            if len(segment) != 1:
                violations.append("unsupported shell loop terminator")
            continue
        executable = Path(segment[0]).name.lower()
        if executable not in _SHELLS:
            segments.append(segment)
            continue
        arguments = segment[1:]
        command_index = next(
            (index for index, argument in enumerate(arguments) if argument.startswith("-") and "c" in argument[1:]),
            None,
        )
        if command_index is None or command_index + 1 >= len(arguments):
            violations.append(f"non-inspectable shell invocation: {executable}")
            continue
        nested_segments, nested_violations = command_segments(arguments[command_index + 1])
        segments.extend(nested_segments)
        violations.extend(nested_violations)
    if not raw_segments and not violations:
        violations.append("unparseable command")
    return segments, sorted(set(violations))


def resolved_path(token: str, workspace: Path) -> Path | None:
    if not token or token.startswith("-"):
        return None
    candidate = Path(token.split("=", 1)[-1])
    try:
        return candidate.resolve() if candidate.is_absolute() else (workspace / candidate).resolve()
    except OSError:
        return None
