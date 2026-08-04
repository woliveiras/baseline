#!/usr/bin/env python3
"""Mechanical completion gates for the Tuxedo spec-driven workflow."""

from __future__ import annotations

import hashlib
import json
import re
import shlex
import sys
from pathlib import Path
from typing import Any


SHA256 = re.compile(r"[0-9a-f]{64}")


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
    return 0


def read_payload() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise GuardError("Tuxedo hook input is malformed; workflow gate denied.") from exc
    if not isinstance(value, dict):
        raise GuardError("Tuxedo hook input must be a JSON object; workflow gate denied.")
    return value


def safe_cwd(payload: dict[str, Any]) -> Path:
    raw = payload.get("cwd")
    if not isinstance(raw, str) or not raw:
        raise GuardError("Tuxedo hook input has no valid cwd; workflow gate denied.")
    path = Path(raw).resolve()
    if not path.is_dir():
        raise GuardError("Tuxedo hook cwd is not an existing directory; workflow gate denied.")
    return path


def load_object(path: Path, label: str, version: int) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GuardError(f"Required {label} is absent: {path}.") from exc
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise GuardError(f"Required {label} is malformed: {path}.") from exc
    if not isinstance(value, dict) or value.get("version") != version:
        raise GuardError(f"Required {label} must be a version {version} JSON object.")
    return value


def resolve_inside(cwd: Path, raw: str) -> Path:
    if not raw or Path(raw).is_absolute():
        raise GuardError(f"Receipt artifact path must be project-relative: {raw!r}.")
    candidate = (cwd / raw).resolve()
    try:
        candidate.relative_to(cwd)
    except ValueError as exc:
        raise GuardError(f"Receipt artifact escapes the project: {raw}.") from exc
    return candidate


def file_hash(path: Path, label: str) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise GuardError(f"{label} is absent or unreadable: {path}.") from exc


def validate_hash_map(cwd: Path, value: Any, label: str, *, nonempty: bool) -> dict[str, str]:
    if not isinstance(value, dict) or (nonempty and not value):
        suffix = " and non-empty" if nonempty else ""
        raise GuardError(f"{label} must be an object{suffix}.")
    checked: dict[str, str] = {}
    for raw, expected in sorted(value.items()):
        if not isinstance(raw, str) or not isinstance(expected, str) or not SHA256.fullmatch(expected):
            raise GuardError(f"{label} contains an invalid path or SHA-256 hash.")
        actual = file_hash(resolve_inside(cwd, raw), label)
        if actual != expected:
            raise GuardError(f"{label} is stale for artifact: {raw}.")
        checked[raw] = expected
    return checked


def map_digest(value: dict[str, str]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def object_digest(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_patterns(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise GuardError(f"{label} must be an array of project-relative glob patterns.")
    for pattern in value:
        path = Path(pattern)
        if path.is_absolute() or ".." in path.parts:
            raise GuardError(f"{label} contains an unsafe glob pattern: {pattern}.")
    return value


def enumerate_scope(cwd: Path, value: Any, label: str) -> set[str]:
    if not isinstance(value, dict):
        raise GuardError(f"{label} scope must be an object.")
    includes = validate_patterns(value.get("include"), f"{label} include")
    excludes = validate_patterns(value.get("exclude", []), f"{label} exclude")
    selected: set[str] = set()
    excluded: set[str] = set()
    for pattern in includes:
        for path in cwd.glob(pattern):
            if path.is_file():
                resolved = resolve_inside(cwd, path.relative_to(cwd).as_posix())
                selected.add(resolved.relative_to(cwd).as_posix())
    for pattern in excludes:
        for path in cwd.glob(pattern):
            if path.is_file():
                resolved = resolve_inside(cwd, path.relative_to(cwd).as_posix())
                excluded.add(resolved.relative_to(cwd).as_posix())
    return selected - excluded


def validate_tree(
    cwd: Path,
    value: Any,
    label: str,
    *,
    required: bool,
    scope: Any,
) -> dict[str, str]:
    hashes = validate_hash_map(cwd, value, label, nonempty=required)
    if scope is None:
        if required or hashes:
            raise GuardError(f"{label} requires a configured tree scope.")
        return hashes
    expected_paths = enumerate_scope(cwd, scope, label)
    declared_paths = set(hashes)
    missing = sorted(expected_paths - declared_paths)
    unexpected = sorted(declared_paths - expected_paths)
    if missing:
        raise GuardError(f"{label} omits scoped artifact: {missing[0]}.")
    if unexpected:
        raise GuardError(f"{label} contains artifact outside its scope: {unexpected[0]}.")
    return hashes


def documentation_digest(documentation: dict[str, Any], artifacts: dict[str, str]) -> str:
    paths = documentation["artifacts"]
    value = {
        "decision": documentation["decision"],
        "rationale": documentation["rationale"],
        "artifact_hashes": {path: artifacts[path] for path in sorted(paths)},
    }
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_documentation(value: Any, artifacts: dict[str, str]) -> tuple[dict[str, Any], str]:
    if not isinstance(value, dict):
        raise GuardError("Completion receipt documentation must be an object.")
    decision = value.get("decision")
    rationale = value.get("rationale")
    paths = value.get("artifacts")
    if decision not in {"required", "not-required"}:
        raise GuardError("Documentation decision must be required or not-required.")
    if not isinstance(rationale, str) or not rationale.strip():
        raise GuardError("Documentation decision requires a non-empty rationale.")
    if not isinstance(paths, list) or not all(isinstance(path, str) and path for path in paths):
        raise GuardError("Documentation artifacts must be an array of project-relative paths.")
    if len(paths) != len(set(paths)):
        raise GuardError("Documentation artifacts must not contain duplicates.")
    if decision == "required" and not paths:
        raise GuardError("Required documentation must name at least one hashed artifact.")
    for path in paths:
        if path not in artifacts:
            raise GuardError(f"Documentation artifact is not covered by artifact_hashes: {path}.")
    normalized = {"decision": decision, "rationale": rationale, "artifacts": paths}
    return normalized, documentation_digest(normalized, artifacts)


def validate_test_evidence(value: Any, test_digest: str, *, required: bool) -> tuple[str | None, str | None]:
    if value is None and not required:
        return None, None
    if not isinstance(value, dict) or set(value) != {"fail_first", "passing"}:
        raise GuardError("Test evidence must contain fail_first and passing records.")
    expected_fields = {
        "fail_first": {"test_tree", "command", "observed_failure"},
        "passing": {"test_tree", "command", "observed_result"},
    }
    normalized: dict[str, dict[str, str]] = {}
    for phase, fields in expected_fields.items():
        record = value.get(phase)
        if not isinstance(record, dict) or set(record) != fields:
            raise GuardError(f"Test evidence {phase} record is incomplete.")
        if record.get("test_tree") != test_digest:
            raise GuardError(f"Test evidence {phase} record is stale for the current test tree.")
        for field in fields - {"test_tree"}:
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise GuardError(f"Test evidence {phase} {field} must be non-empty.")
        normalized[phase] = record
    return object_digest(normalized["fail_first"]), object_digest(normalized)


def validate_review(
    cwd: Path,
    path: str,
    phase: str,
    expected_inputs: dict[str, str],
    expected_outputs: dict[str, str],
) -> None:
    review = load_object(resolve_inside(cwd, path), f"{phase} review", 1)
    if review.get("phase") != phase or review.get("status") != "approved":
        raise GuardError(f"{phase} review must identify its phase and have approved status.")
    if review.get("input_hashes") != expected_inputs:
        raise GuardError(f"{phase} review inputs are incomplete or stale.")
    if review.get("output_hashes", {}) != expected_outputs:
        raise GuardError(f"{phase} review outputs are incomplete or stale.")
    if not isinstance(review.get("findings"), list):
        raise GuardError(f"{phase} review findings must be an array.")
    context = review.get("context")
    if not isinstance(context, dict):
        raise GuardError(f"{phase} review must declare its context exposure.")
    if phase == "spec" and (context.get("tests_exposed") is not False or context.get("implementation_exposed") is not False):
        raise GuardError("Spec review must declare tests and implementation unexposed.")
    if phase == "tests" and context.get("implementation_exposed") is not False:
        raise GuardError("Test review must declare implementation unexposed.")


def validate_receipts(cwd: Path, trigger: str) -> None:
    policy_path = cwd / ".tuxedo" / "policy.json"
    if not policy_path.exists():
        return
    policy = load_object(policy_path, "Tuxedo policy", 1)
    required_on = policy.get("require_receipts_on", [])
    if not isinstance(required_on, list) or not all(item in {"commit", "stop"} for item in required_on):
        raise GuardError("Tuxedo policy require_receipts_on must contain only commit and stop.")
    if trigger not in required_on:
        return

    receipt_raw = policy.get("receipt_path", ".tuxedo/receipts.json")
    if not isinstance(receipt_raw, str):
        raise GuardError("Tuxedo policy receipt_path must be a project-relative string.")
    receipt = load_object(resolve_inside(cwd, receipt_raw), "completion receipt", 2)

    for key in ("spec", "behavior_matrix", "evidence"):
        if not isinstance(receipt.get(key), str) or not receipt[key]:
            raise GuardError(f"Completion receipt is missing {key}.")

    artifact_hashes = validate_hash_map(
        cwd, receipt.get("artifact_hashes"), "Completion artifact hashes", nonempty=True
    )
    for path in (receipt["spec"], receipt["behavior_matrix"], receipt["evidence"]):
        if path not in artifact_hashes:
            raise GuardError(f"Completion receipt does not hash required artifact: {path}.")

    trees = receipt.get("trees")
    if not isinstance(trees, dict) or set(trees) != {"tests", "implementation"}:
        raise GuardError("Completion receipt trees must contain tests and implementation.")
    required_trees = policy.get("required_trees", ["tests", "implementation"])
    if not isinstance(required_trees, list) or not set(required_trees).issubset({"tests", "implementation"}):
        raise GuardError("Tuxedo policy required_trees contains an unsupported tree.")
    tree_scopes = policy.get("tree_scopes")
    if not isinstance(tree_scopes, dict) or not set(tree_scopes).issubset({"tests", "implementation"}):
        raise GuardError("Tuxedo policy tree_scopes must contain only tests and implementation.")
    test_hashes = validate_tree(
        cwd,
        trees["tests"],
        "Test tree",
        required="tests" in required_trees,
        scope=tree_scopes.get("tests"),
    )
    implementation_hashes = validate_tree(
        cwd,
        trees["implementation"],
        "Implementation tree",
        required="implementation" in required_trees,
        scope=tree_scopes.get("implementation"),
    )
    overlap = sorted(set(test_hashes) & set(implementation_hashes))
    allow_overlap = policy.get("allow_tree_overlap", False)
    if not isinstance(allow_overlap, bool):
        raise GuardError("Tuxedo policy allow_tree_overlap must be boolean.")
    if overlap and not allow_overlap:
        raise GuardError(f"Test and implementation tree scopes overlap: {overlap[0]}.")
    test_digest = map_digest(test_hashes)
    implementation_digest = map_digest(implementation_hashes)

    fail_first_digest, test_evidence_digest = validate_test_evidence(
        receipt.get("test_evidence"),
        test_digest,
        required="tests" in required_trees or bool(test_hashes),
    )

    documentation, docs_digest = validate_documentation(receipt.get("documentation"), artifact_hashes)

    reviews = receipt.get("reviews")
    if not isinstance(reviews, dict) or set(reviews) != {"spec", "tests", "code"}:
        raise GuardError("Completion receipt reviews must contain spec, tests, and code.")
    if not all(isinstance(path, str) and path for path in reviews.values()):
        raise GuardError("Completion review paths must be non-empty strings.")
    for path in reviews.values():
        if path not in artifact_hashes:
            raise GuardError(f"Completion receipt does not hash review artifact: {path}.")

    spec_hash = artifact_hashes[receipt["spec"]]
    matrix_hash = artifact_hashes[receipt["behavior_matrix"]]
    evidence_hash = artifact_hashes[receipt["evidence"]]
    spec_review_hash = artifact_hashes[reviews["spec"]]
    test_review_hash = artifact_hashes[reviews["tests"]]

    validate_review(
        cwd,
        reviews["spec"],
        "spec",
        {"spec": spec_hash},
        {"behavior_matrix": matrix_hash},
    )
    validate_review(
        cwd,
        reviews["tests"],
        "tests",
        {
            "spec": spec_hash,
            "behavior_matrix": matrix_hash,
            "tests": test_digest,
            "spec_review": spec_review_hash,
            "fail_first": fail_first_digest,
        },
        {},
    )
    validate_review(
        cwd,
        reviews["code"],
        "code",
        {
            "spec": spec_hash,
            "behavior_matrix": matrix_hash,
            "tests": test_digest,
            "implementation": implementation_digest,
            "evidence": evidence_hash,
            "test_review": test_review_hash,
            "test_evidence": test_evidence_digest,
            "documentation": docs_digest,
        },
        {},
    )


def is_direct_git_commit(command: str) -> bool:
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError:
        return False
    return len(tokens) >= 2 and Path(tokens[0]).name == "git" and tokens[1] == "commit"


def pre_tool(payload: dict[str, Any]) -> int:
    if payload.get("hook_event_name") != "PreToolUse" or payload.get("tool_name") != "Bash":
        raise GuardError("Tuxedo pre-tool hook received an unexpected event or tool.")
    tool_input = payload.get("tool_input")
    command = tool_input.get("command") if isinstance(tool_input, dict) else None
    if not isinstance(command, str) or not command.strip():
        raise GuardError("Tuxedo pre-tool hook received no valid command.")
    if is_direct_git_commit(command):
        validate_receipts(safe_cwd(payload), "commit")
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
