#!/usr/bin/env python3
"""Dedicated Codex CLI authentication boundary for maintainer evaluations.

This module deliberately treats authentication as an operational property of
the Codex CLI. It never reads, copies, prints, or validates the contents of
auth.json and it never falls back to an API key.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_HOME_NAME = ".codex-tuxedo-evals"
EVAL_HOME_ENV = "TUXEDO_EVAL_CODEX_HOME"
PERSONAL_HOME_ENV = "CODEX_HOME"
CODEX_PATH_ENV = "TUXEDO_EVAL_CODEX_PATH"
API_KEY_ENV_NAMES = ("OPENAI_API_KEY", "CODEX_API_KEY")

# These are behavior-bearing content surfaces. Authentication, configuration,
# logs, history, sessions, state databases, and shell snapshots are allowed
# because the Codex CLI can create them during ordinary operation. config.toml
# is fail-closed: only the authentication-storage setting below is allowed.
FORBIDDEN_CONTENT = {
    "skills": "personal skills can change the evaluated instructions",
    "plugins": "personal plugins can change the evaluated tools or instructions",
    "memories": "personal memories can change the evaluated context",
    "rules": "personal rules can change the evaluated policy",
    "instructions": "personal instruction files can change the evaluated context",
    "mcp": "personal MCP configuration can change the evaluated tools",
    "mcp.json": "personal MCP configuration can change the evaluated tools",
    "mcp.toml": "personal MCP configuration can change the evaluated tools",
    "agents.md": "global instructions can change the evaluated context",
}
ALLOWED_CONFIG_KEYS = {"cli_auth_credentials_store"}
BEHAVIOR_CONFIG_KEYS = {
    "approval_policy",
    "developer_instructions",
    "features",
    "hooks",
    "instructions",
    "mcp_servers",
    "model",
    "model_provider",
    "model_providers",
    "network_access_enabled",
    "profiles",
    "rules",
    "sandbox_mode",
    "skills",
    "web_search_enabled",
}


def _display_home(home: Path) -> str:
    """Return only the resolved directory path for user-facing messages."""

    return str(home)


def _resolve_path(raw: str) -> Path:
    try:
        candidate = Path(raw).expanduser()
    except (OSError, RuntimeError, ValueError) as exc:
        raise RuntimeError(f"{EVAL_HOME_ENV} could not be resolved safely") from exc
    if not candidate.is_absolute():
        raise RuntimeError(f"{EVAL_HOME_ENV} must be an absolute path")
    try:
        return candidate.resolve(strict=False)
    except (OSError, RuntimeError, ValueError) as exc:
        raise RuntimeError(f"{EVAL_HOME_ENV} could not be resolved safely") from exc


def _configured_personal_home() -> Path | None:
    raw = os.environ.get(PERSONAL_HOME_ENV)
    if not raw:
        return None
    try:
        candidate = Path(raw).expanduser()
        return candidate.resolve(strict=False)
    except (OSError, RuntimeError, ValueError) as exc:
        raise RuntimeError(f"{PERSONAL_HOME_ENV} could not be resolved safely") from exc


def resolve_dedicated_home() -> Path:
    """Resolve and validate the dedicated home without creating it."""

    if EVAL_HOME_ENV in os.environ:
        raw = os.environ[EVAL_HOME_ENV]
        if not raw.strip():
            raise RuntimeError(f"{EVAL_HOME_ENV} must not be empty")
    else:
        raw = str(Path.home() / DEFAULT_HOME_NAME)

    try:
        lexical = Path(raw).expanduser()
        if not lexical.is_absolute():
            raise RuntimeError(f"{EVAL_HOME_ENV} must be an absolute path")
        lexical = Path(os.path.abspath(lexical))
    except (OSError, RuntimeError, ValueError) as exc:
        if isinstance(exc, RuntimeError):
            raise
        raise RuntimeError(f"{EVAL_HOME_ENV} could not be resolved safely") from exc

    checkout = ROOT.resolve()
    if lexical == checkout or checkout in lexical.parents:
        raise RuntimeError(f"{EVAL_HOME_ENV} must not be inside the Tuxedo checkout")

    resolved = _resolve_path(raw)
    home_root = Path.home().resolve()
    personal_roots = {home_root / ".codex"}
    configured_personal = _configured_personal_home()
    if configured_personal is not None:
        personal_roots.add(configured_personal)

    if resolved == checkout or checkout in resolved.parents:
        raise RuntimeError(f"{EVAL_HOME_ENV} must not be inside the Tuxedo checkout")
    if resolved == Path(resolved.anchor):
        raise RuntimeError(f"{EVAL_HOME_ENV} must identify a dedicated directory, not a filesystem root")
    for personal in personal_roots:
        if resolved == personal or personal in resolved.parents:
            raise RuntimeError(f"{EVAL_HOME_ENV} must not reuse a personal Codex home")
    return resolved


def _validate_content_surfaces(home: Path) -> None:
    if not home.exists():
        return
    if not home.is_dir():
        raise RuntimeError(f"Dedicated Codex evaluation home is not a directory: {_display_home(home)}")
    names = {entry.name.casefold() for entry in home.iterdir()}
    violations = sorted(name for name in names if name in FORBIDDEN_CONTENT)
    if violations:
        reasons = sorted({FORBIDDEN_CONTENT[name] for name in violations})
        raise RuntimeError(
            "Dedicated Codex evaluation home contains behavior-bearing personal content "
            f"({', '.join(violations)}): {'; '.join(reasons)}"
        )
    config = home / "config.toml"
    if config.is_file():
        try:
            parsed = tomllib.loads(config.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            raise RuntimeError("Dedicated Codex evaluation home has an unreadable config.toml") from exc
        configured = sorted(set(parsed) - ALLOWED_CONFIG_KEYS)
        if configured:
            behavior = sorted(set(configured).intersection(BEHAVIOR_CONFIG_KEYS))
            if behavior:
                raise RuntimeError(
                    "Dedicated Codex evaluation home config.toml contains behavior-bearing personal settings: "
                    + ", ".join(behavior)
                )
            raise RuntimeError(
                "Dedicated Codex evaluation home config.toml contains unsupported settings; "
                "only cli_auth_credentials_store is allowed: "
                + ", ".join(configured)
            )


def _codex_command() -> str:
    configured = os.environ.get(CODEX_PATH_ENV)
    command = configured.strip() if configured else "codex"
    if not command:
        command = "codex"
    return shutil.which(command) or command


def evaluation_environment(home: Path) -> dict[str, str]:
    """Build a child environment that cannot use an API-key fallback."""

    environment = os.environ.copy()
    environment[PERSONAL_HOME_ENV] = str(home)
    environment[EVAL_HOME_ENV] = str(home)
    for name in API_KEY_ENV_NAMES:
        environment.pop(name, None)
    return environment


def _run_login_status(home: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [_codex_command(), "login", "status"],
            cwd=ROOT,
            env=evaluation_environment(home),
            text=True,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(
            "Codex CLI is unavailable; set TUXEDO_EVAL_CODEX_PATH to the configured executable"
        ) from exc


def _reported_method(result: subprocess.CompletedProcess[str]) -> str:
    """Classify only the CLI's sanitized method label, never its credentials."""

    text = " ".join(" ".join((result.stdout or "", result.stderr or "")).split()).casefold()
    if "not logged in" in text:
        return "not-authenticated"
    if "logged in using an api key" in text or "logged in using api key" in text:
        return "api-key"
    if "logged in using agent identity" in text:
        return "agent-identity"
    if "logged in using chatgpt" in text:
        return "chatgpt"
    return "unknown"


def _status_for_home(home: Path) -> tuple[subprocess.CompletedProcess[str] | None, str]:
    if not home.is_dir():
        return None, "missing"
    result = _run_login_status(home)
    if result.returncode != 0:
        return result, "not-authenticated"
    return result, _reported_method(result)


def is_authenticated(home: Path) -> bool:
    """Require the CLI to report the selected ChatGPT/Codex auth method."""

    result, method = _status_for_home(home)
    return result is not None and result.returncode == 0 and method == "chatgpt"


def _authentication_failure_message(home: Path, method: str) -> str:
    if method == "api-key":
        reason = "Codex CLI reported API-key authentication; this evaluation requires ChatGPT/Codex login."
    elif method == "unknown":
        reason = "Codex CLI reported authentication without identifying ChatGPT/Codex; refusing an ambiguous session."
    elif method == "agent-identity":
        reason = "Codex CLI reported agent-identity authentication; this evaluation requires ChatGPT/Codex login."
    else:
        reason = "Dedicated Codex evaluation home is not authenticated."
    return f"{reason}\nRun: pnpm run eval:login\nHome: {_display_home(home)}"


def require_authenticated() -> Path:
    """Validate the dedicated home and require successful CLI status."""

    home = resolve_dedicated_home()
    _validate_content_surfaces(home)
    result, method = _status_for_home(home)
    if result is None or result.returncode != 0 or method != "chatgpt":
        raise RuntimeError(_authentication_failure_message(home, method))
    return home


def login() -> int:
    home = resolve_dedicated_home()
    _validate_content_surfaces(home)
    print(f"Dedicated Codex evaluation home: {_display_home(home)}")
    try:
        home.mkdir(parents=True, exist_ok=True, mode=0o700)
    except OSError as exc:
        raise RuntimeError(f"Could not create the dedicated Codex evaluation home: {_display_home(home)}") from exc
    if not home.is_dir():
        raise RuntimeError(f"Dedicated Codex evaluation home is not a directory: {_display_home(home)}")

    # Do not capture the interactive login flow: the official Codex CLI owns
    # its browser/device interaction. The environment still prevents the
    # personal CODEX_HOME and API-key environment variables from being used by the child.
    try:
        result = subprocess.run(
            [_codex_command(), "login"],
            cwd=ROOT,
            env=evaluation_environment(home),
            check=False,
        )
    except OSError as exc:
        raise RuntimeError(
            "Codex CLI is unavailable; set TUXEDO_EVAL_CODEX_PATH to the configured executable"
        ) from exc
    return result.returncode


def status() -> int:
    home = resolve_dedicated_home()
    _validate_content_surfaces(home)
    result, method = _status_for_home(home)
    if result is None or result.returncode != 0 or method != "chatgpt":
        print(_authentication_failure_message(home, method), file=sys.stderr)
        return 1
    print(
        f"Dedicated Codex evaluation home: {_display_home(home)}\n"
        "Codex CLI authentication is valid via ChatGPT/Codex."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage the dedicated Tuxedo evaluation Codex home")
    parser.add_argument("command", choices=("login", "status"))
    args = parser.parse_args(argv)
    try:
        return login() if args.command == "login" else status()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
