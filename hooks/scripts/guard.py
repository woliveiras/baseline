#!/usr/bin/env python3
"""Local Codex hook for narrow mechanical Tuxedo guardrails."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


BLOCKED_PATTERNS = (
    (re.compile(r"(^|[;&|]\s*)rm\s+-[^\n]*r[^\n]*f[^\n]*(?:\s/\s*$|\s/~?\s*$|\$HOME|\$\{HOME\})", re.I), "broad recursive deletion"),
    (re.compile(r"\bgit\s+reset\s+--hard\b", re.I), "history and worktree destruction"),
    (re.compile(r"\bgit\s+clean\s+-[^\s]*[fdx][^\s]*", re.I), "unrecoverable Git cleanup"),
    (re.compile(r"\b(?:mkfs|diskutil\s+erase|dd\s+if=).+", re.I), "disk destruction"),
)

PROTECTED_PATTERNS = (
    ("push", re.compile(r"\bgit\s+push\b", re.I)),
    ("release", re.compile(r"\b(?:gh\s+release|npm\s+publish|cargo\s+publish|twine\s+upload)\b", re.I)),
    ("deploy", re.compile(r"\b(?:deploy|vercel\s+--prod|gcloud\s+.*deploy|kubectl\s+apply)\b", re.I)),
    ("production", re.compile(r"\b(?:production|--prod\b|prod:)\b", re.I)),
    ("destructive", re.compile(r"\b(?:terraform\s+destroy|kubectl\s+delete|drop\s+(?:database|table)|delete\s+from)\b", re.I)),
)


class GuardError(Exception):
    pass


def deny(reason: str, event: str = "PreToolUse") -> int:
    if event == "Stop":
        print(json.dumps({"decision": "block", "reason": reason}, separators=(",", ":")))
    else:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }, separators=(",", ":")))
    return 2


def read_payload() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise GuardError("Tuxedo hook input is malformed; protected operation denied.") from exc
    if not isinstance(value, dict):
        raise GuardError("Tuxedo hook input must be a JSON object; protected operation denied.")
    return value


def safe_cwd(payload: dict[str, Any]) -> Path:
    raw = payload.get("cwd")
    if not isinstance(raw, str) or not raw:
        raise GuardError("Tuxedo hook input has no valid cwd; protected operation denied.")
    path = Path(raw).resolve()
    if not path.is_dir():
        raise GuardError("Tuxedo hook cwd is not an existing directory; protected operation denied.")
    return path


def load_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GuardError(f"Required {label} is absent: {path.relative_to(path.parents[1])}.") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise GuardError(f"Required {label} is malformed.") from exc
    if not isinstance(value, dict) or value.get("version") != 1:
        raise GuardError(f"Required {label} must be a version 1 JSON object.")
    return value


def command_hash(command: str) -> str:
    return hashlib.sha256(command.encode("utf-8")).hexdigest()


def authorize(cwd: Path, operation: str, command: str) -> None:
    receipt = load_object(cwd / ".tuxedo" / "authority.json", "authority receipt")
    grants = receipt.get("grants")
    if not isinstance(grants, list):
        raise GuardError("Authority receipt grants must be an array.")
    digest = command_hash(command)
    for grant in grants:
        if isinstance(grant, dict) and grant.get("operation") == operation and grant.get("command_sha256") == digest:
            return
    raise GuardError(f"Protected {operation} command lacks an exact SHA-256 authority grant.")


def resolve_inside(cwd: Path, raw: str) -> Path:
    candidate = (cwd / raw).resolve()
    try:
        candidate.relative_to(cwd)
    except ValueError as exc:
        raise GuardError(f"Receipt artifact escapes the project: {raw}.") from exc
    return candidate


def validate_receipts(cwd: Path, trigger: str) -> None:
    policy_path = cwd / ".tuxedo" / "policy.json"
    if not policy_path.exists():
        return
    policy = load_object(policy_path, "Tuxedo policy")
    required = policy.get("require_receipts_on", [])
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise GuardError("Tuxedo policy require_receipts_on must be an array of strings.")
    if trigger not in required:
        return
    receipt_raw = policy.get("receipt_path", ".tuxedo/receipts.json")
    if not isinstance(receipt_raw, str) or not receipt_raw:
        raise GuardError("Tuxedo policy receipt_path must be a non-empty string.")
    receipt = load_object(resolve_inside(cwd, receipt_raw), "completion receipt")
    for key in ("spec", "behavior_matrix", "evidence"):
        if not isinstance(receipt.get(key), str) or not receipt[key]:
            raise GuardError(f"Completion receipt is missing {key}.")
    hashes = receipt.get("artifact_hashes")
    if not isinstance(hashes, dict) or not hashes:
        raise GuardError("Completion receipt artifact_hashes must be a non-empty object.")
    for required_path in (receipt["spec"], receipt["behavior_matrix"], receipt["evidence"]):
        if required_path not in hashes:
            raise GuardError(f"Completion receipt does not hash required artifact: {required_path}.")
    for raw, expected in sorted(hashes.items()):
        if not isinstance(raw, str) or not re.fullmatch(r"[0-9a-f]{64}", expected or ""):
            raise GuardError("Completion receipt contains an invalid artifact path or SHA-256 hash.")
        path = resolve_inside(cwd, raw)
        try:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            raise GuardError(f"Receipt artifact is absent or unreadable: {raw}.") from exc
        if actual != expected:
            raise GuardError(f"Completion receipt is stale for artifact: {raw}.")


def pre_tool(payload: dict[str, Any]) -> int:
    if payload.get("hook_event_name") != "PreToolUse" or payload.get("tool_name") != "Bash":
        raise GuardError("Tuxedo pre-tool hook received an unexpected event or tool.")
    tool_input = payload.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not command.strip():
        raise GuardError("Tuxedo pre-tool hook received no valid command.")
    cwd = safe_cwd(payload)
    for pattern, reason in BLOCKED_PATTERNS:
        if pattern.search(command):
            raise GuardError(f"Blocked {reason}; use a recoverable, explicitly scoped alternative.")
    for operation, pattern in PROTECTED_PATTERNS:
        if pattern.search(command):
            authorize(cwd, operation, command)
            break
    if re.search(r"\bgit\s+commit\b", command, re.I):
        validate_receipts(cwd, "commit")
    return 0


def stop(payload: dict[str, Any]) -> int:
    if payload.get("hook_event_name") != "Stop":
        raise GuardError("Tuxedo stop hook received an unexpected event.")
    validate_receipts(safe_cwd(payload), "stop")
    return 0


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"pre-tool", "stop"}:
        print("usage: guard.py pre-tool|stop", file=sys.stderr)
        return 2
    event = "Stop" if sys.argv[1] == "stop" else "PreToolUse"
    try:
        payload = read_payload()
        return stop(payload) if event == "Stop" else pre_tool(payload)
    except GuardError as exc:
        return deny(str(exc), event)


if __name__ == "__main__":
    raise SystemExit(main())
