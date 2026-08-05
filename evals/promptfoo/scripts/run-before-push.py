#!/usr/bin/env python3
"""Maintainer-only Promptfoo orchestration and the canonical pre-push gate."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = Path(__file__).resolve().parent
PROMPTFOO_ROOT = ROOT / "evals" / "promptfoo"
PROMPTFOO = ROOT / "node_modules" / ".bin" / "promptfoo"
PNPM = shutil.which("pnpm") or "pnpm"
SYNTHETIC_CANARY = "TUXEDO_SYNTHETIC_CANARY_7b4f1c"
CONFIGS = (
    PROMPTFOO_ROOT / "promptfooconfig.yaml",
    PROMPTFOO_ROOT / "routing-config.yaml",
    PROMPTFOO_ROOT / "security-config.yaml",
    PROMPTFOO_ROOT / "smoke-config.yaml",
    PROMPTFOO_ROOT / "compare-config.yaml",
    PROMPTFOO_ROOT / "redteam-config.yaml",
)


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load evaluation module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PREPARE = _load_module("tuxedo_prepare_workspaces", SCRIPT_DIR / "prepare-workspaces.py")


def _redact(value: str) -> str:
    value = value.replace(SYNTHETIC_CANARY, "[synthetic-canary-redacted]")
    value = re.sub(r"(?i)(auth\.json|OPENAI_API_KEY|CODEX_API_KEY)\s*[:=]\s*[^\s,}]+", r"\1=[redacted]", value)
    return value


def _run(command: list[str], *, timeout: int = 300, env: dict[str, str] | None = None, label: str) -> subprocess.CompletedProcess[str]:
    print(f"[tuxedo] {label}")
    result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, check=False, timeout=timeout)
    if result.returncode:
        detail = _redact((result.stdout + "\n" + result.stderr).strip())[-4000:]
        raise RuntimeError(f"{label} failed with exit code {result.returncode}\n{detail}")
    return result


def _git_status() -> str:
    return subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True, check=True).stdout


def _git_diff_check() -> None:
    _run(["git", "diff", "--check"], label="git diff --check")


def _validate_local_outputs(generated: Path, results: Path) -> None:
    """Validate ignored output directories without deleting prior evidence.

    Generated probes are review inputs and may remain between runs. Results are
    append-only local reports. Neither directory is a fixture source, so only
    their file types and directory shape are checked here.
    """
    if not generated.is_dir() or not results.is_dir():
        raise RuntimeError("Promptfoo generated/results directories are missing")
    generated_unexpected = [
        path.name for path in generated.iterdir()
        if path.name != ".gitkeep" and (not path.is_file() or path.suffix not in {".yaml", ".yml", ".json"})
    ]
    if generated_unexpected:
        raise RuntimeError(f"generated/ contains unsupported entries: {generated_unexpected}")
    results_unexpected = [
        path.name for path in results.iterdir()
        if path.name != ".gitkeep" and (not path.is_file() or path.suffix != ".json")
    ]
    if results_unexpected:
        raise RuntimeError(f"results/ contains unsupported entries: {results_unexpected}")
    print(f"[tuxedo] ignored output directories valid: generated={len(generated_unexpected)} unexpected, results={len(list(results.glob('*.json')))} reports")


def _validate_fixture_catalog() -> None:
    catalog = json.loads((ROOT / "evals" / "fixtures" / "catalog.json").read_text(encoding="utf-8"))
    for fixture_name, fixture in catalog.items():
        if not isinstance(fixture, dict):
            raise RuntimeError(f"fixture is not an object: {fixture_name}")
        for relative, content in fixture.items():
            path = Path(relative)
            if path.is_absolute() or ".." in path.parts or not isinstance(content, str):
                raise RuntimeError(f"unsafe or non-text fixture entry: {fixture_name}/{relative}")
    _validate_local_outputs(PROMPTFOO_ROOT / "generated", PROMPTFOO_ROOT / "results")
    print("[tuxedo] fixture and ignored-directory cleanliness")


def _discover_validator(kind: str) -> Path | None:
    env_name = f"TUXEDO_{kind.upper()}_VALIDATOR"
    configured = os.environ.get(env_name)
    candidates: list[Path] = []
    if configured:
        candidates.append(Path(configured).expanduser())
    roots: list[Path] = []
    for variable in ("TUXEDO_CODEX_SKILLS_ROOT", "CODEX_SKILLS_ROOT", "CODEX_HOME"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value).expanduser())
    roots.append(Path.home() / ".codex")
    relative = {
        "plugin": Path("skills/.system/plugin-creator/scripts/validate_plugin.py"),
        "skill": Path("skills/.system/skill-creator/scripts/quick_validate.py"),
    }[kind]
    validator_suffix = relative.relative_to("skills/.system")
    relative_without_skills = Path(".system") / relative.relative_to("skills")
    for root in roots:
        candidates.append(root / relative)
        candidates.append(root / relative_without_skills)
        candidates.append(root / validator_suffix)
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.is_file():
            return resolved
    return None


def _official_validators() -> None:
    plugin_validator = _discover_validator("plugin")
    skill_validator = _discover_validator("skill")
    if plugin_validator is None or skill_validator is None:
        raise RuntimeError(
            "official plugin/skill validator unavailable; install the Codex system skills or set "
            "TUXEDO_PLUGIN_VALIDATOR and TUXEDO_SKILL_VALIDATOR to executable validator paths"
        )
    validator_python = os.environ.get("TUXEDO_VALIDATOR_PYTHON", sys.executable)
    validator_command = shutil.which(validator_python) or validator_python
    validator_executable = Path(validator_command).expanduser()
    if not validator_executable.is_file():
        raise RuntimeError(
            f"TUXEDO_VALIDATOR_PYTHON does not point to a Python executable: {validator_python}"
        )
    _run([str(validator_executable), str(plugin_validator), str(ROOT)], timeout=120, label="official plugin validator")
    for skill in sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir()):
        _run([str(validator_executable), str(skill_validator), str(skill)], timeout=120, label=f"official skill validator: {skill.name}")


def _promptfoo_validate() -> None:
    if not PROMPTFOO.is_file():
        raise RuntimeError("Promptfoo is not installed; run pnpm install --frozen-lockfile in the maintainer checkout")
    for config in CONFIGS:
        _run([PNPM, "exec", "promptfoo", "validate", "config", "-c", str(config)], timeout=120, label=f"Promptfoo config validation: {config.name}")


def _python_and_shell_checks() -> None:
    _run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], timeout=180, label="Tuxedo unit tests")
    _run([sys.executable, "evals/run.py", "--dry-run"], timeout=120, label="legacy runner dry-run")
    for path in sorted(ROOT.rglob("*.sh")):
        if ".git" not in path.parts and "node_modules" not in path.parts:
            _run(["sh", "-n", str(path)], timeout=30, label=f"shell syntax: {path.relative_to(ROOT)}")


def _codex_version(codex_home: Path) -> str:
    result = subprocess.run(
        [os.environ.get("TUXEDO_EVAL_CODEX_PATH", "codex"), "--version"],
        env=PREPARE.evaluation_environment(codex_home),
        text=True,
        capture_output=True,
        check=False,
        timeout=15,
    )
    if result.returncode:
        raise RuntimeError("the configured Codex binary could not report its version")
    return result.stdout.strip()


def _promptfoo_version() -> str:
    package = json.loads((ROOT / "node_modules" / "promptfoo" / "package.json").read_text(encoding="utf-8"))
    return str(package["version"])


def _iter_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_dicts(child)


def _validate_raw_result(raw: Any) -> list[dict[str, Any]]:
    rows = [item for item in _iter_dicts(raw) if isinstance(item.get("response"), dict)]
    if not rows:
        raise RuntimeError("Promptfoo returned no provider responses")
    failures: list[str] = []
    for index, row in enumerate(rows):
        response = row.get("response") or {}
        if response.get("error") or response.get("errorMessage"):
            failures.append(f"row {index}: provider error")
        output = response.get("output")
        if not isinstance(output, str) or not output.strip():
            failures.append(f"row {index}: empty provider output")
        raw = response.get("raw")
        if isinstance(raw, str):
            try:
                raw = json.loads(raw)
            except json.JSONDecodeError:
                raw = None
        if isinstance(raw, dict):
            if raw.get("turnCompleted") is False or raw.get("turn_completed") is False:
                failures.append(f"row {index}: Codex turn did not complete")
            events = raw.get("events")
            if isinstance(events, list) and not any(
                isinstance(event, dict) and event.get("type") == "turn.completed" for event in events
            ):
                failures.append(f"row {index}: event stream has no completed turn")
        for item in _iter_dicts(row):
            if item.get("pass") is False:
                failures.append(f"row {index}: assertion failed")
            if item.get("success") is False:
                failures.append(f"row {index}: provider/test marked unsuccessful")
    if failures:
        raise RuntimeError("Promptfoo result validation failed: " + "; ".join(failures[:12]))
    return rows


def _safe_metadata(row: dict[str, Any]) -> dict[str, Any]:
    response = row.get("response") if isinstance(row.get("response"), dict) else {}
    metadata = response.get("metadata") if isinstance(response, dict) else {}
    if not isinstance(metadata, dict):
        metadata = {}
    calls = metadata.get("skillCalls") or []
    observed: list[dict[str, str]] = []
    for call in calls if isinstance(calls, list) else []:
        if isinstance(call, dict):
            observed.append({"name": str(call.get("name", "")), "source": str(call.get("source", ""))})
    return {"skills_observed": observed}


def _report(raw: dict[str, Any], rows: list[dict[str, Any]], manifest: dict[str, Any], suite: str, repeat: int, seconds: float, codex_home: Path) -> dict[str, Any]:
    report_rows: list[dict[str, Any]] = []
    for row in rows:
        response = row.get("response") if isinstance(row.get("response"), dict) else {}
        grading = row.get("gradingResult") if isinstance(row.get("gradingResult"), dict) else {}
        report_rows.append({
            "test_id": str(row.get("testCaseId") or row.get("id") or row.get("description") or "unknown"),
            "provider": str(row.get("provider") or row.get("providerId") or "unknown"),
            "status": "pass" if row.get("success", True) else "fail",
            "duration_ms": response.get("latencyMs") or row.get("latencyMs"),
            "tokens": response.get("tokenUsage") or row.get("tokenUsage") or {},
            "deterministic_checks": grading.get("componentResults", []),
            "secondary_scores": {"score": grading.get("score")} if "score" in grading else {},
            "observed": _safe_metadata(row),
        })
    return {
        "version": 1,
        "suite": suite,
        "condition_fingerprints": {
            "current": manifest.get("current_fingerprint"),
            "proposed": manifest.get("proposed_fingerprint"),
        },
        "model": "gpt-5.2-codex",
        "reasoning": "low" if suite == "smoke" else "medium",
        "codex_version": _codex_version(codex_home),
        "promptfoo_version": _promptfoo_version(),
        "seed": int(os.environ.get("TUXEDO_EVAL_SEED", "0")),
        "repetitions": repeat,
        "duration_seconds": round(seconds, 3),
        "privacy": {"shared": False, "remote_redteam_generation": False, "raw_responses_saved": False},
        "summary": {"provider_responses": len(rows), "status": "pass"},
        "runs": report_rows,
        "limitations": [
            "skill-used and metadata.skillCalls are Codex SDK heuristics",
            "deterministic verifiers have precedence over secondary judgments",
            "results are scoped to the recorded model, Codex version, tasks, fixtures, and conditions",
        ],
    }


def _check_workspace_clean(manifest: dict[str, Any]) -> None:
    root = Path(str(manifest["workspace_root"]))
    for key, conditions in (manifest.get("workspaces") or {}).items():
        for condition, entry in conditions.items():
            workspace = Path(str(entry["path"]))
            if root not in workspace.parents or not workspace.is_dir():
                raise RuntimeError(f"workspace escaped the disposable root: {key}/{condition}")
            for outside in entry.get("outside_files", []):
                path = Path(str(outside["path"]))
                if not path.is_file():
                    raise RuntimeError(f"outside sentinel disappeared: {path}")
                if hashlib.sha256(path.read_bytes()).hexdigest() != outside["sha256"]:
                    raise RuntimeError(f"outside sentinel changed: {path}")


def run_promptfoo(suite: str, config: Path, *, current_root: Path = ROOT, proposed_root: Path | None = None, repeat: int = 1, timeout: int = 1800, codex_home: Path | None = None) -> Path:
    codex_home = codex_home or PREPARE.preflight_codex_home()
    workspace_root = Path(tempfile.mkdtemp(prefix=f"tuxedo-promptfoo-{suite}-"))
    keep = os.environ.get("TUXEDO_EVAL_KEEP_WORKSPACES") == "1"
    raw_path = workspace_root / "promptfoo-raw.json"
    manifest: dict[str, Any] | None = None
    started = time.monotonic()
    try:
        manifest = PREPARE.prepare(suite, workspace_root / "workspaces", current_root, proposed_root)
        env = PREPARE.evaluation_environment(codex_home)
        env.update({
            "TUXEDO_EVAL_WORKSPACE_ROOT": str(workspace_root / "workspaces"),
            "TUXEDO_EVAL_MANIFEST": str(manifest["manifest_path"]),
            "PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION": "true",
            "PROMPTFOO_DISABLE_SHARE": "true",
        })
        command = [
            PNPM, "exec", "promptfoo", "eval", "-c", str(config), "--no-cache", "--no-share", "--no-write",
            "--max-concurrency", "1", "--repeat", str(repeat), "--no-progress-bar", "-o", str(raw_path),
        ]
        result = _run(command, timeout=timeout, env=env, label=f"Promptfoo provider suite: {suite}")
        if not raw_path.is_file():
            raise RuntimeError("Promptfoo completed without producing a result file")
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        rows = _validate_raw_result(raw)
        _check_workspace_clean(manifest)
        report = _report(raw, rows, manifest, suite, repeat, time.monotonic() - started, codex_home)
        output = PROMPTFOO_ROOT / "results" / f"{suite}-{time.time_ns()}.json"
        output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(f"[tuxedo] {suite}: {len(rows)} provider responses, {report['duration_seconds']}s, result={output.relative_to(ROOT)}")
        return output
    finally:
        raw_path.unlink(missing_ok=True)
        if not keep:
            shutil.rmtree(workspace_root, ignore_errors=True)
        else:
            print(f"[tuxedo] preserved debug workspace: {workspace_root}")


def _run_skills() -> None:
    run_promptfoo("routing", PROMPTFOO_ROOT / "routing-config.yaml")
    run_promptfoo("behavior", PROMPTFOO_ROOT / "promptfooconfig.yaml")


def _run_compare() -> None:
    raw = os.environ.get("TUXEDO_EVAL_PROPOSED_ROOT")
    if not raw:
        raise RuntimeError("TUXEDO_EVAL_PROPOSED_ROOT is required for eval:compare")
    run_promptfoo("compare", PROMPTFOO_ROOT / "compare-config.yaml", proposed_root=Path(raw), repeat=3)


def _redteam(command_name: str) -> None:
    if command_name == "review":
        path = PROMPTFOO_ROOT / "generated" / "redteam.yaml"
        if not path.is_file():
            raise RuntimeError("no generated probes found; run eval:redteam:generate explicitly first")
        lines = path.read_text(encoding="utf-8").splitlines()
        print(f"[tuxedo] generated probe file: {path.relative_to(ROOT)} ({len(lines)} sanitized lines)")
        for line in lines[:40]:
            print(_redact(line[:240]))
        return

    codex_home = PREPARE.preflight_codex_home()
    env = PREPARE.evaluation_environment(codex_home)
    env["PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION"] = "true"
    env["PROMPTFOO_DISABLE_SHARE"] = "true"
    config = PROMPTFOO_ROOT / "redteam-config.yaml"
    if command_name == "generate":
        output = PROMPTFOO_ROOT / "generated" / "redteam.yaml"
        _run([
            PNPM, "exec", "promptfoo", "redteam", "generate", "-c", str(config), "-o", str(output), "--no-cache",
            "--no-progress-bar", "--strict", "--plugins", "coding-agent:core", "--num-tests", "10",
        ], timeout=1800, env=env, label="Promptfoo red-team probe generation (explicit, local-only)")
        print(f"[tuxedo] generated probes at {output.relative_to(ROOT)}; review before execution")
    elif command_name == "full":
        _run([
            PNPM, "exec", "promptfoo", "redteam", "run", "-c", str(config), "--no-cache", "--no-progress-bar", "--strict",
        ], timeout=3600, env=env, label="Promptfoo full red-team scan (explicit, expensive)")
def verify_push() -> None:
    before = _git_status()
    codex_home = PREPARE.preflight_codex_home()
    _official_validators()
    _python_and_shell_checks()
    _promptfoo_validate()
    _validate_fixture_catalog()
    run_promptfoo("routing", PROMPTFOO_ROOT / "routing-config.yaml", codex_home=codex_home)
    run_promptfoo("behavior", PROMPTFOO_ROOT / "promptfooconfig.yaml", codex_home=codex_home)
    run_promptfoo("security", PROMPTFOO_ROOT / "security-config.yaml", codex_home=codex_home)
    _git_diff_check()
    after = _git_status()
    if after != before:
        raise RuntimeError("evaluation modified the checkout; before/after git status differ")
    print("[tuxedo] verify:push passed; checkout status unchanged")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=("smoke", "skills", "security", "compare", "redteam-generate", "redteam-review", "redteam-full", "verify-push"), required=True)
    args = parser.parse_args(argv)
    try:
        if args.suite == "smoke":
            run_promptfoo("smoke", PROMPTFOO_ROOT / "smoke-config.yaml")
        elif args.suite == "skills":
            _run_skills()
        elif args.suite == "security":
            run_promptfoo("security", PROMPTFOO_ROOT / "security-config.yaml")
        elif args.suite == "compare":
            _run_compare()
        elif args.suite == "redteam-generate":
            _redteam("generate")
        elif args.suite == "redteam-review":
            _redteam("review")
        elif args.suite == "redteam-full":
            _redteam("full")
        else:
            verify_push()
        return 0
    except RuntimeError as exc:
        print(f"[tuxedo] {_redact(str(exc))}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
