#!/usr/bin/env python3
"""Development-only Promptfoo orchestration and explicit evaluation suites."""

from __future__ import annotations

import argparse
import concurrent.futures
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
from typing import Any, Iterable, NamedTuple


ROOT = Path(__file__).resolve().parents[3]
PLUGIN_ROOT = ROOT / "plugins" / "baseline"
SCRIPT_DIR = Path(__file__).resolve().parent
PROMPTFOO_ROOT = ROOT / "evals" / "promptfoo"
PROMPTFOO = ROOT / "node_modules" / ".bin" / "promptfoo"
PNPM = shutil.which("pnpm") or "pnpm"
SYNTHETIC_CANARY = "BASELINE_SYNTHETIC_CANARY_7b4f1c"
CONFIGS = (
    PROMPTFOO_ROOT / "promptfooconfig.yaml",
    PROMPTFOO_ROOT / "routing-config.yaml",
    PROMPTFOO_ROOT / "security-config.yaml",
    PROMPTFOO_ROOT / "smoke-config.yaml",
    PROMPTFOO_ROOT / "compare-config.yaml",
    PROMPTFOO_ROOT / "redteam-config.yaml",
)
PROMPTFOO_ASSERTION_FAILURE_EXIT_CODE = 100
FULL_MAX_WORKERS = 2
GATING_CONDITIONS = {
    "behavior": frozenset({"focal", "current"}),
    "compare": frozenset({"proposed"}),
}
KNOWN_CONDITIONS = ("control", "core", "focal", "broad", "current", "proposed")
FULL_EXECUTION_CONTROLS = {
    "dedicated_codex_home": True,
    "network_access": False,
    "web_search": False,
    "approval_policy": "never",
    "persist_threads": False,
    "promptfoo_cache": False,
    "codex_remote_cache": False,
}


class Shard(NamedTuple):
    name: str
    filter_range: str


class SuiteOutcome(NamedTuple):
    suite: str
    report_path: Path
    status: str
    provider_responses: int
    passed: int
    failed: int
    needs_review: int
    failed_ids: tuple[str, ...]


SHARD_COUNTS = {
    "routing": 2,
    "behavior": 4,
}
SHARD_CATALOGS = {
    "routing": PROMPTFOO_ROOT / "tests" / "routing.yaml",
    "behavior": PROMPTFOO_ROOT / "tests" / "behavior.yaml",
}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load evaluation module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PREPARE = _load_module("baseline_prepare_workspaces", SCRIPT_DIR / "prepare-workspaces.py")


def _suite_shards(suite: str) -> tuple[Shard, ...]:
    requested = SHARD_COUNTS.get(suite)
    catalog_path = SHARD_CATALOGS.get(suite)
    if requested is None or catalog_path is None:
        return ()
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(catalog, list) or not catalog:
        raise RuntimeError(f"{suite} evaluation catalog must be a non-empty list")
    count = min(requested, len(catalog))
    width, remainder = divmod(len(catalog), count)
    shards = []
    start = 0
    for index in range(count):
        end = start + width + (1 if index < remainder else 0)
        shards.append(Shard(f"{index + 1}-of-{count}", f"{start}:{end}"))
        start = end
    return tuple(shards)


def _redact(value: str) -> str:
    value = value.replace(SYNTHETIC_CANARY, "[synthetic-canary-redacted]")
    value = re.sub(r"(?i)(auth\.json|OPENAI_API_KEY|CODEX_API_KEY)\s*[:=]\s*[^\s,}]+", r"\1=[redacted]", value)
    return value


def _run(
    command: list[str],
    *,
    timeout: int = 300,
    env: dict[str, str] | None = None,
    label: str,
    accepted_returncodes: frozenset[int] = frozenset({0}),
) -> subprocess.CompletedProcess[str]:
    print(f"[baseline] {label}")
    try:
        result = subprocess.run(
            command, cwd=ROOT, env=env, text=True, capture_output=True, check=False, timeout=timeout
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"{label} timed out after {timeout} seconds") from exc
    if result.returncode not in accepted_returncodes:
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
    print(f"[baseline] ignored output directories valid: generated={len(generated_unexpected)} unexpected, results={len(list(results.glob('*.json')))} reports")


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
    print("[baseline] fixture and ignored-directory cleanliness")


def _discover_validator(kind: str) -> Path | None:
    env_name = f"BASELINE_{kind.upper()}_VALIDATOR"
    configured = os.environ.get(env_name)
    candidates: list[Path] = []
    if configured:
        candidates.append(Path(configured).expanduser())
    roots: list[Path] = []
    for variable in ("BASELINE_CODEX_SKILLS_ROOT", "CODEX_SKILLS_ROOT", "CODEX_HOME"):
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
            "BASELINE_PLUGIN_VALIDATOR and BASELINE_SKILL_VALIDATOR to executable validator paths"
        )
    validator_executable = sys.executable
    _run(
        [str(validator_executable), str(plugin_validator), str(PLUGIN_ROOT)],
        timeout=120,
        label="official plugin validator",
    )
    for skill in sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir()):
        _run([str(validator_executable), str(skill_validator), str(skill)], timeout=120, label=f"official skill validator: {skill.name}")


def _promptfoo_validate() -> None:
    if not PROMPTFOO.is_file():
        raise RuntimeError("Promptfoo is not installed; run pnpm install --frozen-lockfile in the development checkout")
    for config in CONFIGS:
        _run([PNPM, "exec", "promptfoo", "validate", "config", "-c", str(config)], timeout=120, label=f"Promptfoo config validation: {config.name}")


def _python_and_shell_checks() -> None:
    _run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], timeout=180, label="Baseline unit tests")
    _run([sys.executable, "evals/run.py", "--dry-run"], timeout=120, label="legacy runner dry-run")
    for path in sorted(ROOT.rglob("*.sh")):
        if ".git" not in path.parts and "node_modules" not in path.parts:
            _run(["sh", "-n", str(path)], timeout=30, label=f"shell syntax: {path.relative_to(ROOT)}")


def _codex_version(codex_home: Path) -> str:
    try:
        result = subprocess.run(
            [os.environ.get("BASELINE_EVAL_CODEX_PATH", "codex"), "--version"],
            env=PREPARE.evaluation_environment(codex_home),
            text=True,
            capture_output=True,
            check=False,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("the configured Codex binary could not report its version") from exc
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


def _safe_label(value: Any) -> str:
    return _redact(str(value or ""))[:200]


def _safe_token_usage(value: Any) -> dict[str, int | float]:
    if not isinstance(value, dict):
        return {}
    return {
        str(key): amount
        for key, amount in value.items()
        if isinstance(amount, (int, float)) and not isinstance(amount, bool)
    }


def _safe_component_results(grading: dict[str, Any]) -> list[dict[str, Any]]:
    safe: list[dict[str, Any]] = []
    components = grading.get("componentResults")
    for component in components if isinstance(components, list) else []:
        if not isinstance(component, dict):
            continue
        assertion = component.get("assertion") if isinstance(component.get("assertion"), dict) else {}
        safe.append({
            "pass": component.get("pass"),
            "score": component.get("score"),
            "needs_review": _needs_review(component),
            "result_code": "needs-review" if _needs_review(component) else ("pass" if component.get("pass") is True else "fail"),
            "assertion_type": str(assertion.get("type") or "unknown"),
        })
    return safe


def _needs_review(value: dict[str, Any]) -> bool:
    # Promptfoo maps Python assertion keys to camelCase but older/synthetic
    # exports may still contain the original snake_case spelling.
    return value.get("needs_review") is True or value.get("needsReview") is True


def _row_id(row: dict[str, Any], index: int) -> str:
    test_case = row.get("testCase") if isinstance(row.get("testCase"), dict) else {}
    variables = row.get("vars") if isinstance(row.get("vars"), dict) else {}
    return str(
        row.get("description")
        or test_case.get("description")
        or row.get("testCaseId")
        or row.get("id")
        or variables.get("id")
        or variables.get("task_id")
        or variables.get("workspace_key")
        or f"row-{index}"
    )


def _row_status(row: dict[str, Any]) -> str:
    grading = row.get("gradingResult") if isinstance(row.get("gradingResult"), dict) else {}
    components = grading.get("componentResults") if isinstance(grading.get("componentResults"), list) else []
    if any(
        isinstance(component, dict)
        and component.get("pass") is False
        and not _needs_review(component)
        for component in components
    ):
        return "fail"
    if _needs_review(grading) or any(
        isinstance(component, dict) and _needs_review(component) for component in components
    ):
        return "needs-review"
    if row.get("success") is False or row.get("pass") is False or grading.get("pass") is False:
        return "fail"
    return "pass"


def _gating_run(suite: str, provider: str) -> bool:
    expected = GATING_CONDITIONS.get(suite)
    if expected is None:
        return True
    normalized = provider.lower()
    observed = next((
        condition
        for condition in KNOWN_CONDITIONS
        if normalized == condition or normalized.endswith(f":{condition}") or condition in normalized
    ), None)
    return True if observed is None else observed in expected


def _verdict_status(failed: int, needs_review: int, *, promptfoo_exit_code: int | None = None) -> str:
    if failed:
        return "fail"
    if needs_review:
        return "needs-review"
    if promptfoo_exit_code is not None and promptfoo_exit_code != 0:
        return "fail"
    return "pass"


def _outcomes_status(outcomes: list[SuiteOutcome]) -> str:
    if any(outcome.status == "fail" for outcome in outcomes):
        return "fail"
    if any(outcome.status == "needs-review" for outcome in outcomes):
        return "needs-review"
    return "pass"


def _report(
    rows: list[dict[str, Any]],
    manifest: dict[str, Any],
    suite: str,
    repeat: int,
    seconds: float,
    codex_version: str,
    promptfoo_version: str,
    shard: Shard | None,
    promptfoo_exit_code: int,
) -> dict[str, Any]:
    report_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        response = row.get("response") if isinstance(row.get("response"), dict) else {}
        grading = row.get("gradingResult") if isinstance(row.get("gradingResult"), dict) else {}
        variables = row.get("vars") if isinstance(row.get("vars"), dict) else {}
        status = _row_status(row)
        provider = row.get("provider") or row.get("providerId") or "unknown"
        if isinstance(provider, dict):
            provider = provider.get("label") or provider.get("id") or "unknown"
        provider = _safe_label(provider)
        gating = _gating_run(suite, provider)
        report_rows.append({
            "test_id": _row_id(row, index),
            "criterion_id": _safe_label(variables.get("criterion_id")) if variables.get("criterion_id") else None,
            "provider": provider,
            "gating": gating,
            "status": status,
            "duration_ms": response.get("latencyMs") or row.get("latencyMs"),
            "tokens": _safe_token_usage(response.get("tokenUsage") or row.get("tokenUsage")),
            "result_code": status,
            "deterministic_checks": _safe_component_results(grading),
            "secondary_scores": {"score": grading.get("score")} if "score" in grading else {},
            "observed": _safe_metadata(row),
        })
    counts = {status: sum(run["status"] == status for run in report_rows) for status in ("pass", "fail", "needs-review")}
    gating_counts = {
        status: sum(run["gating"] and run["status"] == status for run in report_rows)
        for status in ("pass", "fail", "needs-review")
    }
    non_gating_nonpass = any(
        not run["gating"] and run["status"] != "pass" for run in report_rows
    )
    status = _verdict_status(gating_counts["fail"], gating_counts["needs-review"])
    if status == "pass" and promptfoo_exit_code != 0 and not non_gating_nonpass:
        status = "fail"
    return {
        "version": 2,
        "suite": suite,
        "shard": {"name": shard.name, "filter_range": shard.filter_range} if shard else None,
        "promptfoo_exit_code": promptfoo_exit_code,
        "condition_fingerprints": {
            "current": manifest.get("current_fingerprint"),
            "proposed": manifest.get("proposed_fingerprint"),
        },
        "model": "codex-cli-default",
        "reasoning": "low" if suite == "smoke" else "medium",
        "codex_version": codex_version,
        "promptfoo_version": promptfoo_version,
        "seed": int(os.environ.get("BASELINE_EVAL_SEED", "0")),
        "repetitions": repeat,
        "duration_seconds": round(seconds, 3),
        "privacy": {"shared": False, "remote_redteam_generation": False, "raw_responses_saved": False},
        "execution_controls": FULL_EXECUTION_CONTROLS,
        "summary": {
            "provider_responses": len(rows),
            "passed": counts["pass"],
            "failed": counts["fail"],
            "needs_review": counts["needs-review"],
            "gating_passed": gating_counts["pass"],
            "gating_failed": gating_counts["fail"],
            "gating_needs_review": gating_counts["needs-review"],
            "status": status,
        },
        "runs": report_rows,
        "limitations": [
            "skill-used and metadata.skillCalls are Codex SDK heuristics",
            "deterministic verifiers have precedence over secondary judgments",
            "results are scoped to the recorded model, Codex version, tasks, fixtures, and conditions",
            "behavior gates focal and current; compare gates proposed; other conditions remain visible comparisons",
        ],
    }


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _write_report(report: dict[str, Any], suite: str, suffix: str = "") -> Path:
    output = PROMPTFOO_ROOT / "results" / f"{suite}{suffix}-{time.time_ns()}.json"
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return output


def _load_raw_result(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Promptfoo result file is missing, unreadable, or malformed") from exc


def _outcome(report: dict[str, Any], path: Path) -> SuiteOutcome:
    summary = report["summary"]
    failed_ids = tuple(
        str(run["test_id"])
        for run in report["runs"]
        if run.get("gating", True) and run.get("status") in {"fail", "needs-review"}
    )
    if summary["status"] != "pass" and not failed_ids:
        failed_ids = (f"promptfoo-exit-{report.get('promptfoo_exit_code', 'unknown')}",)
    return SuiteOutcome(
        str(report["suite"]),
        path,
        str(summary["status"]),
        int(summary["provider_responses"]),
        int(summary["passed"]),
        int(summary["failed"]),
        int(summary["needs_review"]),
        failed_ids,
    )


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


def _new_workspace_root(suite: str) -> Path:
    return Path(tempfile.mkdtemp(prefix=f"baseline-promptfoo-{suite}-")).resolve()


def run_promptfoo(
    suite: str,
    config: Path,
    *,
    current_root: Path = ROOT,
    proposed_root: Path | None = None,
    repeat: int = 1,
    timeout: int = 1800,
    codex_home: Path | None = None,
    shard: Shard | None = None,
    provider_filter: str | None = None,
    case_pattern: str | None = None,
) -> SuiteOutcome:
    if repeat != 1:
        raise RuntimeError(
            "one Promptfoo process cannot repeat a write-capable trial safely; "
            "run independent single-repetition processes instead"
        )
    codex_home = codex_home or PREPARE.preflight_codex_home()
    codex_version = _codex_version(codex_home)
    promptfoo_version = _promptfoo_version()
    workspace_root = _new_workspace_root(suite)
    keep = os.environ.get("BASELINE_EVAL_KEEP_WORKSPACES") == "1"
    raw_path = workspace_root / "promptfoo-raw.json"
    manifest: dict[str, Any] | None = None
    started = time.monotonic()
    try:
        manifest = PREPARE.prepare(suite, workspace_root / "workspaces", current_root, proposed_root)
        env = PREPARE.evaluation_environment(codex_home)
        env.update({
            "BASELINE_EVAL_WORKSPACE_ROOT": str(workspace_root / "workspaces"),
            "BASELINE_EVAL_GRADER_ROOT": str(workspace_root / "grader"),
            "BASELINE_EVAL_MANIFEST": str(manifest["manifest_path"]),
            "PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION": "true",
            "PROMPTFOO_DISABLE_SHARE": "true",
            "PROMPTFOO_CONFIG_DIR": str(workspace_root / "promptfoo-state"),
        })
        (workspace_root / "grader").mkdir()
        (workspace_root / "promptfoo-state").mkdir()
        command = [
            PNPM, "exec", "promptfoo", "eval", "-c", str(config), "--no-cache", "--no-share",
            "--max-concurrency", "1", "--repeat", str(repeat), "--no-progress-bar", "-o", str(raw_path),
        ]
        if shard:
            command.extend(["--filter-range", shard.filter_range])
        if provider_filter:
            command.extend(["--filter-providers", provider_filter])
        if case_pattern:
            command.extend(["--filter-pattern", case_pattern])
        result = _run(
            command,
            timeout=timeout,
            env=env,
            label=f"Promptfoo provider suite: {suite}{f' [{shard.name}]' if shard else ''}",
            accepted_returncodes=frozenset({0, PROMPTFOO_ASSERTION_FAILURE_EXIT_CODE}),
        )
        if not raw_path.is_file():
            raise RuntimeError(
                f"Promptfoo exited with code {result.returncode} without producing a result file"
            )
        raw = _load_raw_result(raw_path)
        rows = _validate_raw_result(raw)
        _check_workspace_clean(manifest)
        report = _report(
            rows,
            manifest,
            suite,
            repeat,
            time.monotonic() - started,
            codex_version,
            promptfoo_version,
            shard,
            result.returncode,
        )
        output = _write_report(report, suite, f"-{shard.name}" if shard else "")
        outcome = _outcome(report, output)
        print(
            f"[baseline] {suite}{f' [{shard.name}]' if shard else ''}: "
            f"{outcome.passed}/{outcome.provider_responses} passed, {report['duration_seconds']}s, "
            f"result={_display_path(output)}"
        )
        return outcome
    finally:
        raw_path.unlink(missing_ok=True)
        shutil.rmtree(workspace_root / "promptfoo-state", ignore_errors=True)
        if not keep:
            shutil.rmtree(workspace_root, ignore_errors=True)
        else:
            print(f"[baseline] preserved debug workspace: {workspace_root}")


def _parse_filter_range(value: str) -> tuple[int, int]:
    start, end = value.split(":", 1)
    return int(start), int(end)


def _aggregate_shards(suite: str, outcomes: list[SuiteOutcome], duration_seconds: float) -> SuiteOutcome:
    reports = [json.loads(outcome.report_path.read_text(encoding="utf-8")) for outcome in outcomes]
    runs = [run for report in reports for run in report["runs"]]
    gating_counts = {
        status: sum(run.get("gating", True) and run.get("status") == status for run in runs)
        for status in ("pass", "fail", "needs-review")
    }
    passed = sum(outcome.passed for outcome in outcomes)
    failed = sum(outcome.failed for outcome in outcomes)
    needs_review = sum(outcome.needs_review for outcome in outcomes)
    shards_not_passing = sum(outcome.status != "pass" for outcome in outcomes)
    aggregate_status = _outcomes_status(outcomes)
    aggregate = {
        "version": 2,
        "suite": suite,
        "condition_fingerprints": reports[0].get("condition_fingerprints"),
        "model": reports[0].get("model"),
        "reasoning": reports[0].get("reasoning"),
        "codex_version": reports[0].get("codex_version"),
        "promptfoo_version": reports[0].get("promptfoo_version"),
        "seed": reports[0].get("seed"),
        "repetitions": reports[0].get("repetitions"),
        "shards": [{"report": _display_path(outcome.report_path), **report["shard"]} for outcome, report in zip(outcomes, reports)],
        "duration_seconds": round(duration_seconds, 3),
        "privacy": {"shared": False, "remote_redteam_generation": False, "raw_responses_saved": False},
        "summary": {
            "provider_responses": sum(outcome.provider_responses for outcome in outcomes),
            "passed": passed,
            "failed": failed,
            "needs_review": needs_review,
            "gating_passed": gating_counts["pass"],
            "gating_failed": gating_counts["fail"],
            "gating_needs_review": gating_counts["needs-review"],
            "shards_not_passing": shards_not_passing,
            "status": aggregate_status,
        },
        "runs": runs,
        "limitations": reports[0]["limitations"],
    }
    output = _write_report(aggregate, suite, "-aggregate")
    result = _outcome(aggregate, output)
    print(f"[baseline] {suite} aggregate: {passed}/{result.provider_responses} passed, result={_display_path(output)}")
    return result


def _aggregate_repetitions(suite: str, outcomes: list[SuiteOutcome], duration_seconds: float) -> SuiteOutcome:
    reports = [json.loads(outcome.report_path.read_text(encoding="utf-8")) for outcome in outcomes]
    if not reports:
        raise RuntimeError(f"cannot aggregate zero independent {suite} repetitions")
    if any(report.get("repetitions") != 1 for report in reports):
        raise RuntimeError(f"{suite} aggregate requires single-repetition source reports")
    fingerprints = reports[0].get("condition_fingerprints")
    if any(report.get("condition_fingerprints") != fingerprints for report in reports[1:]):
        raise RuntimeError(f"{suite} fingerprints changed between independent repetitions")
    runs = [
        {**run, "repetition": repetition}
        for repetition, report in enumerate(reports, start=1)
        for run in report["runs"]
    ]
    gating_counts = {
        status: sum(run.get("gating", True) and run.get("status") == status for run in runs)
        for status in ("pass", "fail", "needs-review")
    }
    passed = sum(outcome.passed for outcome in outcomes)
    failed = sum(outcome.failed for outcome in outcomes)
    needs_review = sum(outcome.needs_review for outcome in outcomes)
    aggregate = {
        "version": 2,
        "suite": suite,
        "condition_fingerprints": fingerprints,
        "model": reports[0].get("model"),
        "reasoning": reports[0].get("reasoning"),
        "codex_version": reports[0].get("codex_version"),
        "promptfoo_version": reports[0].get("promptfoo_version"),
        "seed": reports[0].get("seed"),
        "repetitions": len(outcomes),
        "independent_runs": [
            {"repetition": repetition, "report": _display_path(outcome.report_path)}
            for repetition, outcome in enumerate(outcomes, start=1)
        ],
        "duration_seconds": round(duration_seconds, 3),
        "privacy": {"shared": False, "remote_redteam_generation": False, "raw_responses_saved": False},
        "summary": {
            "provider_responses": sum(outcome.provider_responses for outcome in outcomes),
            "passed": passed,
            "failed": failed,
            "needs_review": needs_review,
            "gating_passed": gating_counts["pass"],
            "gating_failed": gating_counts["fail"],
            "gating_needs_review": gating_counts["needs-review"],
            "status": _outcomes_status(outcomes),
        },
        "runs": runs,
        "limitations": reports[0]["limitations"],
    }
    output = _write_report(aggregate, suite, "-aggregate")
    result = _outcome(aggregate, output)
    print(
        f"[baseline] {suite} independent repetitions: "
        f"{passed}/{result.provider_responses} passed, result={_display_path(output)}"
    )
    return result


def run_promptfoo_suite(
    suite: str,
    config: Path,
    *,
    codex_home: Path | None = None,
    current_root: Path = ROOT,
    proposed_root: Path | None = None,
    repeat: int = 1,
) -> SuiteOutcome:
    codex_home = codex_home or PREPARE.preflight_codex_home()
    shards = _suite_shards(suite)
    if not shards:
        return run_promptfoo(
            suite, config, codex_home=codex_home, current_root=current_root,
            proposed_root=proposed_root, repeat=repeat,
        )
    outcomes: list[SuiteOutcome] = []
    started = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=FULL_MAX_WORKERS) as executor:
        futures = [
            executor.submit(
                run_promptfoo,
                suite,
                config,
                codex_home=codex_home,
                current_root=current_root,
                proposed_root=proposed_root,
                repeat=repeat,
                timeout=3600,
                shard=shard,
            )
            for shard in shards
        ]
        for future in futures:
            outcomes.append(future.result())
    return _aggregate_shards(suite, outcomes, time.monotonic() - started)


def _require_passing_outcomes(outcomes: list[SuiteOutcome]) -> None:
    failed = [outcome for outcome in outcomes if outcome.status != "pass"]
    if not failed:
        return
    summary = "; ".join(
        f"{outcome.suite}: {outcome.passed}/{outcome.provider_responses} passed "
        f"({outcome.failed} failed, {outcome.needs_review} needs-review), report={_display_path(outcome.report_path)}"
        for outcome in failed
    )
    raise RuntimeError(f"evaluation assertions did not pass: {summary}")


def _write_full_summary(outcomes: list[SuiteOutcome], duration_seconds: float) -> Path:
    status = _outcomes_status(outcomes)
    report = {
        "version": 2,
        "suite": "full",
        "duration_seconds": round(duration_seconds, 3),
        "privacy": {"shared": False, "remote_redteam_generation": False, "raw_responses_saved": False},
        "execution_controls": FULL_EXECUTION_CONTROLS,
        "summary": {
            "provider_responses": sum(outcome.provider_responses for outcome in outcomes),
            "passed": sum(outcome.passed for outcome in outcomes),
            "failed": sum(outcome.failed for outcome in outcomes),
            "needs_review": sum(outcome.needs_review for outcome in outcomes),
            "status": status,
        },
        "suites": [
            {
                "suite": outcome.suite,
                "status": outcome.status,
                "provider_responses": outcome.provider_responses,
                "passed": outcome.passed,
                "failed": outcome.failed,
                "needs_review": outcome.needs_review,
                "report": _display_path(outcome.report_path),
            }
            for outcome in outcomes
        ],
    }
    output = _write_report(report, "full", "-aggregate")
    print(f"[baseline] full aggregate: status={status}, {duration_seconds:.3f}s, result={_display_path(output)}")
    return output


def _run_skills() -> None:
    codex_home = PREPARE.preflight_codex_home()
    outcomes = [
        run_promptfoo_suite("routing", PROMPTFOO_ROOT / "routing-config.yaml", codex_home=codex_home),
        run_promptfoo_suite("behavior", PROMPTFOO_ROOT / "promptfooconfig.yaml", codex_home=codex_home),
    ]
    _require_passing_outcomes(outcomes)


def _run_compare() -> None:
    raw = os.environ.get("BASELINE_EVAL_PROPOSED_ROOT")
    if not raw:
        raise RuntimeError("BASELINE_EVAL_PROPOSED_ROOT is required for eval:compare")
    started = time.monotonic()
    codex_home = PREPARE.preflight_codex_home()
    outcomes = [
        run_promptfoo(
            "compare",
            PROMPTFOO_ROOT / "compare-config.yaml",
            proposed_root=Path(raw),
            repeat=1,
            codex_home=codex_home,
        )
        for _ in range(3)
    ]
    outcome = _aggregate_repetitions("compare", outcomes, time.monotonic() - started)
    _require_passing_outcomes([outcome])


def _redteam(command_name: str) -> None:
    if command_name == "review":
        path = PROMPTFOO_ROOT / "generated" / "redteam.yaml"
        if not path.is_file():
            raise RuntimeError("no generated probes found; run eval:redteam:generate explicitly first")
        lines = path.read_text(encoding="utf-8").splitlines()
        print(f"[baseline] generated probe file: {path.relative_to(ROOT)} ({len(lines)} sanitized lines)")
        for line in lines[:40]:
            print(_redact(line[:240]))
        return

    codex_home = PREPARE.preflight_codex_home()
    env = PREPARE.evaluation_environment(codex_home)
    env["PROMPTFOO_DISABLE_REDTEAM_REMOTE_GENERATION"] = "true"
    env["PROMPTFOO_DISABLE_SHARE"] = "true"
    state_root = Path(tempfile.mkdtemp(prefix="baseline-promptfoo-redteam-"))
    env["PROMPTFOO_CONFIG_DIR"] = str(state_root / "promptfoo-state")
    (state_root / "promptfoo-state").mkdir()
    config = PROMPTFOO_ROOT / "redteam-config.yaml"
    try:
        workspace_root = state_root / "workspaces"
        PREPARE.prepare_redteam(workspace_root, ROOT)
        env["BASELINE_EVAL_WORKSPACE_ROOT"] = str(workspace_root)
        if command_name == "generate":
            output = PROMPTFOO_ROOT / "generated" / "redteam.yaml"
            _run([
                PNPM, "exec", "promptfoo", "redteam", "generate", "-c", str(config), "-o", str(output), "--no-cache",
                "--no-progress-bar", "--strict", "--plugins", "coding-agent:core", "--num-tests", "10",
            ], timeout=1800, env=env, label="Promptfoo red-team probe generation (explicit, local-only)")
            print(f"[baseline] generated probes at {output.relative_to(ROOT)}; review before execution")
        elif command_name == "full":
            _run([
                PNPM, "exec", "promptfoo", "redteam", "run", "-c", str(config), "--no-cache", "--no-progress-bar", "--strict",
            ], timeout=3600, env=env, label="Promptfoo full red-team scan (explicit, expensive)")
    finally:
        shutil.rmtree(state_root, ignore_errors=True)


def run_full_evaluation() -> None:
    started = time.monotonic()
    before = _git_status()
    codex_home = PREPARE.preflight_codex_home()
    _official_validators()
    _python_and_shell_checks()
    _promptfoo_validate()
    _validate_fixture_catalog()
    outcomes = [
        run_promptfoo_suite("routing", PROMPTFOO_ROOT / "routing-config.yaml", codex_home=codex_home),
        run_promptfoo_suite("behavior", PROMPTFOO_ROOT / "promptfooconfig.yaml", codex_home=codex_home),
        run_promptfoo_suite("security", PROMPTFOO_ROOT / "security-config.yaml", codex_home=codex_home),
    ]
    _write_full_summary(outcomes, time.monotonic() - started)
    _git_diff_check()
    after = _git_status()
    if after != before:
        raise RuntimeError("evaluation modified the checkout; before/after git status differ")
    _require_passing_outcomes(outcomes)
    print("[baseline] eval:full passed; checkout status unchanged")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", choices=("smoke", "routing", "skills", "security", "compare", "redteam-generate", "redteam-review", "redteam-full", "full"), required=True)
    parser.add_argument("--case-pattern", help="Promptfoo description regex; supported by routing and security")
    args = parser.parse_args(argv)
    try:
        if args.case_pattern and args.suite not in {"routing", "security"}:
            raise RuntimeError("--case-pattern is supported only with --suite routing or security")
        if args.suite == "smoke":
            _require_passing_outcomes([run_promptfoo("smoke", PROMPTFOO_ROOT / "smoke-config.yaml")])
        elif args.suite == "routing":
            _require_passing_outcomes([
                run_promptfoo(
                    "routing",
                    PROMPTFOO_ROOT / "routing-config.yaml",
                    case_pattern=args.case_pattern,
                )
            ])
        elif args.suite == "skills":
            _run_skills()
        elif args.suite == "security":
            _require_passing_outcomes([
                run_promptfoo(
                    "security",
                    PROMPTFOO_ROOT / "security-config.yaml",
                    case_pattern=args.case_pattern,
                )
            ])
        elif args.suite == "compare":
            _run_compare()
        elif args.suite == "redteam-generate":
            _redteam("generate")
        elif args.suite == "redteam-review":
            _redteam("review")
        elif args.suite == "redteam-full":
            _redteam("full")
        else:
            run_full_evaluation()
        return 0
    except RuntimeError as exc:
        print(f"[baseline] {_redact(str(exc))}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
