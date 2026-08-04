#!/usr/bin/env python3
"""Local Codex-first evaluation runner. Dry-run is the safe default."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("baseline", "core", "focal", "broad")


def load_tasks():
    return [json.loads(path.read_text()) for path in sorted((ROOT / "evals" / "tasks").glob("*.json"))]


def materialize(case: dict, destination: Path) -> None:
    for relative, content in case.items():
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def configure(variant: str, task: dict, workspace: Path) -> None:
    if variant != "baseline":
        shutil.copy2(ROOT / "AGENTS.md", workspace / "AGENTS.md")
    if variant in {"focal", "broad"}:
        skill_root = workspace / ".agents" / "skills"
        skill_root.mkdir(parents=True)
        names = [task["focal_skill"]] if variant == "focal" else sorted(path.name for path in (ROOT / "skills").iterdir() if path.is_dir())
        for name in names:
            shutil.copytree(ROOT / "skills" / name, skill_root / name)


def score(text: str, task: dict) -> dict:
    lowered = text.lower()
    required = {term: bool(re.search(re.escape(term.lower()), lowered)) for term in task["required"]}
    forbidden = {term: bool(re.search(re.escape(term.lower()), lowered)) for term in task["forbidden"]}
    return {"pass": all(required.values()) and not any(forbidden.values()), "required": required, "forbidden": forbidden}


def execute(task: dict, variant: str, catalog: dict, codex: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="tuxedo-eval-") as tmp:
        workspace = Path(tmp)
        materialize(catalog[task["fixture"]], workspace)
        configure(variant, task, workspace)
        command = [codex, "exec", "--json", "--sandbox", "workspace-write", "--skip-git-repo-check", "-C", str(workspace), task["prompt"]]
        started = time.time()
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        combined = completed.stdout + "\n" + completed.stderr
        return {"task": task["id"], "variant": variant, "command": command, "exit_code": completed.returncode, "seconds": round(time.time() - started, 3), "score": score(combined, task), "raw": combined}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="list the evaluation matrix without model calls")
    parser.add_argument("--execute", action="store_true", help="run Codex calls; may consume quota")
    parser.add_argument("--variant", choices=VARIANTS, action="append")
    parser.add_argument("--task", action="append")
    parser.add_argument("--codex", default=shutil.which("codex") or "codex")
    args = parser.parse_args()
    tasks = load_tasks()
    if args.task:
        tasks = [task for task in tasks if task["id"] in set(args.task)]
    variants = args.variant or list(VARIANTS)
    matrix = [{"task": task["id"], "variant": variant, "focal_skill": task["focal_skill"]} for task in tasks for variant in variants]
    if not args.execute:
        print(json.dumps({"mode": "dry-run", "runs": matrix}, indent=2))
        return 0
    catalog = json.loads((ROOT / "evals" / "fixtures" / "catalog.json").read_text())
    results = []
    for task in tasks:
        for variant in variants:
            result = execute(task, variant, catalog, args.codex)
            results.append(result)
            print(json.dumps({key: value for key, value in result.items() if key != "raw"}))
    stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    output = ROOT / "evals" / "results" / f"run-{stamp}.json"
    output.write_text(json.dumps({"runs": results}, indent=2))
    print(output)
    return 0 if all(result["exit_code"] == 0 for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
