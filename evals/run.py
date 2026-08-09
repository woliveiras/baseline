#!/usr/bin/env python3
"""Codex-first paired evaluation runner. Dry-run is the safe default."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from verifiers import snapshot, verify


ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("control", "core", "focal", "broad", "current", "proposed")
TASK_FIELDS = {
    "id", "fixture", "focal_skill", "prompt", "verifier", "mutation_policy", "secondary_review"
}


def load_tasks() -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for path in sorted((ROOT / "evals" / "tasks").glob("*.json")):
        task = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(task, dict) or not TASK_FIELDS.issubset(task):
            raise ValueError(f"task is missing required fields: {path}")
        tasks.append(task)
    return tasks


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def safe_relative(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"fixture path escapes workspace: {raw}")
    return path


def materialize(case: dict[str, str], destination: Path) -> None:
    for relative, content in case.items():
        path = destination / safe_relative(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def copy_skills(source_root: Path, workspace: Path, names: list[str]) -> None:
    skill_root = workspace / ".agents" / "skills"
    skill_root.mkdir(parents=True, exist_ok=True)
    for name in names:
        source = source_root / "skills" / name
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"variant references an absent skill: {source}")
        shutil.copytree(source, skill_root / name)


def configure(variant: str, task: dict[str, Any], workspace: Path, source_root: Path) -> dict[str, Any]:
    all_skills = sorted(path.name for path in (source_root / "skills").iterdir() if path.is_dir())
    includes_contract = variant in {"core", "focal", "current", "proposed"}
    if includes_contract:
        shutil.copy2(source_root / "AGENTS.md", workspace / "AGENTS.md")

    selected: list[str] = []
    if variant == "focal":
        selected = [task["focal_skill"]]
    elif variant in {"broad", "current", "proposed"}:
        selected = all_skills
    if selected:
        copy_skills(source_root, workspace, selected)

    return {
        "contract": includes_contract,
        "skills": selected,
        "workflow_enforcement": "declarative",
        "note": "Lifecycle hooks are not distributed; trials exercise AGENTS and skills.",
    }


def parse_events(stdout: str) -> tuple[int, dict[str, int], bool]:
    count = 0
    usage: dict[str, int] = {}
    completed_turn = False
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        count += 1
        if not isinstance(event, dict):
            continue
        if event.get("type") == "turn.completed":
            completed_turn = True
        candidates = [event.get("usage")]
        item = event.get("item")
        if isinstance(item, dict):
            candidates.append(item.get("usage"))
        for candidate in candidates:
            if isinstance(candidate, dict):
                for key, value in candidate.items():
                    if isinstance(value, int) and "token" in key:
                        usage[key] = max(usage.get(key, 0), value)
    return count, usage, completed_turn


def apply_process_checks(
    verification: dict[str, Any],
    *,
    exit_code: int,
    timed_out: bool,
    answer: str,
    completed_turn: bool,
) -> dict[str, Any]:
    checks = [
        {
            "id": "codex-process",
            "pass": exit_code == 0 and not timed_out,
            "detail": "completed" if exit_code == 0 and not timed_out else "timeout" if timed_out else f"exit_code={exit_code}",
        },
        {
            "id": "final-response",
            "pass": bool(answer.strip()),
            "detail": "non-empty" if answer.strip() else "missing or empty",
        },
        {
            "id": "codex-turn-completed",
            "pass": completed_turn,
            "detail": "turn.completed observed" if completed_turn else "turn.completed absent",
        },
    ]
    verification["checks"].extend(checks)
    if any(not item["pass"] for item in checks):
        verification["status"] = "fail"
    return verification


def build_command(
    codex: str,
    workspace: Path,
    output: Path,
    prompt: str,
    model: str | None,
    reasoning_effort: str | None,
) -> list[str]:
    command = [
        codex,
        "exec",
        "--json",
        "--ephemeral",
        "--ignore-user-config",
        "--sandbox",
        "workspace-write",
        "--skip-git-repo-check",
        "-o",
        str(output),
        "-C",
        str(workspace),
    ]
    if model:
        command.extend(["--model", model])
    if reasoning_effort:
        command.extend(["-c", f'model_reasoning_effort="{reasoning_effort}"'])
    command.append(prompt)
    return command


def execute(
    run: dict[str, Any],
    task: dict[str, Any],
    catalog: dict[str, Any],
    rubric: dict[str, Any],
    codex: str,
    current_root: Path,
    proposed_root: Path | None,
    timeout: int,
    model: str | None,
    reasoning_effort: str | None,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="baseline-eval-") as tmp:
        workspace = Path(tmp)
        fixture = catalog.get(task["fixture"])
        if not isinstance(fixture, dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in fixture.items()):
            raise ValueError(f"invalid fixture: {task['fixture']}")
        materialize(fixture, workspace)
        source_root = proposed_root if run["variant"] == "proposed" else current_root
        if source_root is None:
            raise ValueError("the proposed variant requires --proposed-root")
        configuration = configure(run["variant"], task, workspace, source_root)
        before = snapshot(workspace)
        final_message = workspace / ".baseline-final.txt"
        command = build_command(codex, workspace, final_message, task["prompt"], model, reasoning_effort)

        started = time.monotonic()
        timed_out = False
        try:
            completed = subprocess.run(
                command,
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout,
            )
            exit_code = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            exit_code = 124
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        seconds = round(time.monotonic() - started, 3)
        answer = final_message.read_text(encoding="utf-8", errors="replace") if final_message.exists() else ""
        verification = verify(task, workspace, before)
        event_count, usage, completed_turn = parse_events(stdout)
        apply_process_checks(
            verification,
            exit_code=exit_code,
            timed_out=timed_out,
            answer=answer,
            completed_turn=completed_turn,
        )
        return {
            **run,
            "source_root": str(source_root),
            "configuration": configuration,
            "command": command,
            "exit_code": exit_code,
            "timed_out": timed_out,
            "seconds": seconds,
            "event_count": event_count,
            "usage": usage,
            "verification": verification,
            "secondary_rubric": rubric if task["secondary_review"] else None,
            "answer": answer,
            "raw": stdout + ("\n" if stdout and stderr else "") + stderr,
        }


def build_matrix(
    tasks: list[dict[str, Any]],
    variants: list[str],
    repetitions: int,
    seed: int,
) -> list[dict[str, Any]]:
    runs = [
        {
            "run_id": f"{task['id']}:{variant}:{repetition}",
            "task": task["id"],
            "variant": variant,
            "repetition": repetition,
            "focal_skill": task["focal_skill"],
            "verifier": task["verifier"],
        }
        for task in tasks
        for variant in variants
        for repetition in range(1, repetitions + 1)
    ]
    random.Random(seed).shuffle(runs)
    return runs


def valid_root(path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not (resolved / "AGENTS.md").is_file() or not (resolved / "skills").is_dir():
        raise ValueError(f"{label} is not a Baseline root: {resolved}")
    return resolved


def root_fingerprint(root: Path) -> str:
    paths = [root / "AGENTS.md"] + sorted(path for path in (root / "skills").rglob("*") if path.is_file())
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def codex_version(codex: str) -> str:
    try:
        result = subprocess.run([codex, "--version"], text=True, capture_output=True, check=False, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"
    return result.stdout.strip() if result.returncode == 0 else "unavailable"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="list the randomized matrix without model calls")
    mode.add_argument("--execute", action="store_true", help="run Codex calls; may consume quota")
    parser.add_argument("--variant", choices=VARIANTS, action="append")
    parser.add_argument("--task", action="append")
    parser.add_argument("--repetitions", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--model")
    parser.add_argument("--reasoning-effort")
    parser.add_argument("--codex", default=shutil.which("codex") or "codex")
    parser.add_argument("--current-root", type=Path, default=ROOT)
    parser.add_argument("--proposed-root", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--allow-needs-review",
        action="store_true",
        help="return zero when deterministic checks pass but secondary review is pending",
    )
    args = parser.parse_args()

    if args.repetitions < 1 or args.timeout < 1:
        parser.error("--repetitions and --timeout must be positive")
    current_root = valid_root(args.current_root, "current root")
    proposed_root = valid_root(args.proposed_root, "proposed root") if args.proposed_root else None
    current_fingerprint = root_fingerprint(current_root)
    proposed_fingerprint = root_fingerprint(proposed_root) if proposed_root else None
    tasks = load_tasks()
    if args.task:
        requested = set(args.task)
        tasks = [task for task in tasks if task["id"] in requested]
        missing = requested - {task["id"] for task in tasks}
        if missing:
            parser.error(f"unknown tasks: {', '.join(sorted(missing))}")
    variants = list(dict.fromkeys(args.variant or VARIANTS))
    if args.execute and "proposed" in variants:
        if proposed_root is None:
            parser.error("--proposed-root is required when executing the proposed variant")
        if proposed_root == current_root:
            parser.error("--proposed-root must differ from --current-root")
        if proposed_fingerprint == current_fingerprint:
            parser.error("current and proposed roots must have different AGENTS.md or skill content")
    matrix = build_matrix(tasks, variants, args.repetitions, args.seed)

    if not args.execute:
        print(json.dumps({
            "mode": "dry-run",
            "seed": args.seed,
            "repetitions": args.repetitions,
            "current_root": str(current_root),
            "current_fingerprint": current_fingerprint,
            "proposed_root": str(proposed_root) if proposed_root else None,
            "proposed_fingerprint": proposed_fingerprint,
            "runs": matrix,
        }, indent=2))
        return 0

    catalog = load_json(ROOT / "evals" / "fixtures" / "catalog.json")
    rubric = load_json(ROOT / "evals" / "rubrics" / "secondary.json")
    by_id = {task["id"]: task for task in tasks}
    results = []
    for run in matrix:
        result = execute(
            run,
            by_id[run["task"]],
            catalog,
            rubric,
            args.codex,
            current_root,
            proposed_root,
            args.timeout,
            args.model,
            args.reasoning_effort,
        )
        results.append(result)
        print(json.dumps({
            "run_id": result["run_id"],
            "seconds": result["seconds"],
            "status": result["verification"]["status"],
            "exit_code": result["exit_code"],
        }))

    summary = {
        status: sum(result["verification"]["status"] == status for result in results)
        for status in ("pass", "needs-review", "fail")
    }
    payload = {
        "version": 1,
        "seed": args.seed,
        "repetitions": args.repetitions,
        "model": args.model,
        "reasoning_effort": args.reasoning_effort,
        "codex_version": codex_version(args.codex),
        "current_root": str(current_root),
        "current_fingerprint": current_fingerprint,
        "proposed_root": str(proposed_root) if proposed_root else None,
        "proposed_fingerprint": proposed_fingerprint,
        "timeout": args.timeout,
        "summary": summary,
        "runs": results,
    }
    output = args.output or ROOT / "evals" / "results" / f"run-{time.time_ns()}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(output)

    if summary["fail"]:
        return 1
    if summary["needs-review"] and not args.allow_needs_review:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
