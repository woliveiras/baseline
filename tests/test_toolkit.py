from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "hooks" / "scripts" / "guard.py"
EXPECTED_SKILLS = {
    "refine", "brainstorming", "spec", "tdd", "bugfix", "verify", "docs",
    "git-commit", "ci-workflow", "shape-domain", "design-deep-modules",
    "improve-architecture", "decision-framework", "premortem", "session-bridge",
    "technical-research", "security-review",
}


class ToolkitStructureTests(unittest.TestCase):
    def test_manifest_and_distributed_inventory(self):
        manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text())
        self.assertEqual("tuxedo", manifest["name"])
        self.assertEqual("0.1.0", manifest["version"])
        self.assertNotIn("hooks", manifest, "default hooks/hooks.json discovery avoids stale manifest schemas")
        actual = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
        self.assertEqual(EXPECTED_SKILLS, actual)

    def test_skill_frontmatter_and_ui_policy(self):
        for name in EXPECTED_SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text()
            match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            self.assertIsNotNone(match, name)
            keys = {line.split(":", 1)[0] for line in match.group(1).splitlines() if ":" in line}
            self.assertEqual({"name", "description"}, keys, name)
            self.assertIn(f"name: {name}", match.group(1))
            ui = (ROOT / "skills" / name / "agents" / "openai.yaml").read_text()
            self.assertIn(f"$%s" % name, ui)
        for name in {"brainstorming", "session-bridge", "improve-architecture"}:
            ui = (ROOT / "skills" / name / "agents" / "openai.yaml").read_text()
            self.assertIn("allow_implicit_invocation: false", ui)

    def test_links_resolve_and_no_placeholders(self):
        markdown = list((ROOT / "skills").rglob("*.md"))
        for path in markdown:
            text = path.read_text()
            self.assertNotRegex(text, r"\[TODO|TODO:", str(path))
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                self.assertTrue((path.parent / target.split("#", 1)[0]).resolve().exists(), f"{path}: {target}")

    def test_maintainer_content_is_not_referenced_as_installed_content(self):
        manifest = (ROOT / ".codex-plugin" / "plugin.json").read_text()
        for name in ("docs/", "tests/", "evals/"):
            self.assertNotIn(name, manifest)
        corpus = "\n".join(path.read_text(errors="ignore") for path in (ROOT / "skills").rglob("*") if path.is_file())
        for forbidden in ("geremmyas ", "go:embed", "geremmyas.yml", "internal/cli", "catalog/packs"):
            self.assertNotIn(forbidden, corpus.lower())

    def test_eval_dry_run_covers_all_comparisons(self):
        result = subprocess.run(["python3", str(ROOT / "evals" / "run.py"), "--dry-run"], text=True, capture_output=True, check=False)
        self.assertEqual(0, result.returncode, result.stderr)
        runs = json.loads(result.stdout)["runs"]
        self.assertEqual(48, len(runs))
        self.assertEqual({"baseline", "core", "focal", "broad", "current", "proposed"}, {run["variant"] for run in runs})


class HookTests(unittest.TestCase):
    def run_guard(self, mode: str, payload: str, cwd: Path):
        payload = payload.replace("FIXTURE_CWD", str(cwd))
        return subprocess.run(["python3", str(GUARD), mode], input=payload, text=True, capture_output=True, check=False)

    def fixture(self, name: str) -> str:
        return (ROOT / "tests" / "fixtures" / "hooks" / name).read_text()

    def test_valid_invalid_absent_and_malformed_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            ok = self.run_guard("pre-tool", self.fixture("pretool-valid.json"), cwd)
            self.assertEqual(0, ok.returncode, ok.stdout + ok.stderr)
            blocked = self.run_guard("pre-tool", self.fixture("pretool-dangerous.json"), cwd)
            self.assertEqual(0, blocked.returncode)
            self.assertEqual("deny", json.loads(blocked.stdout)["hookSpecificOutput"]["permissionDecision"])
            for name in ("pretool-missing.json", "pretool-malformed.json"):
                result = self.run_guard("pre-tool", self.fixture(name), cwd)
                self.assertEqual(0, result.returncode, name)
                self.assertEqual("deny", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"])

    def test_exact_authority_grant(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / ".tuxedo").mkdir()
            command = "git push origin feature"
            payload = json.dumps({"cwd": str(cwd), "hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": command}})
            denied = self.run_guard("pre-tool", payload, cwd)
            self.assertEqual(0, denied.returncode)
            self.assertEqual("deny", json.loads(denied.stdout)["hookSpecificOutput"]["permissionDecision"])
            grant = {"version": 1, "grants": [{"operation": "push", "command_sha256": hashlib.sha256(command.encode()).hexdigest()}]}
            (cwd / ".tuxedo" / "authority.json").write_text(json.dumps(grant))
            allowed = self.run_guard("pre-tool", payload, cwd)
            self.assertEqual(0, allowed.returncode, allowed.stdout + allowed.stderr)

    def test_receipts_valid_stale_missing_and_malformed(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            control = cwd / ".tuxedo"
            control.mkdir()
            paths = ["spec.md", "matrix.md", "evidence.md"]
            for name in paths:
                (cwd / name).write_text(name)
            policy = {"version": 1, "require_receipts_on": ["stop"], "receipt_path": ".tuxedo/receipts.json"}
            (control / "policy.json").write_text(json.dumps(policy))
            payload = json.dumps({"cwd": str(cwd), "hook_event_name": "Stop"})
            missing = self.run_guard("stop", payload, cwd)
            self.assertEqual(0, missing.returncode)
            self.assertEqual("block", json.loads(missing.stdout)["decision"])
            (control / "receipts.json").write_text("{")
            malformed = self.run_guard("stop", payload, cwd)
            self.assertEqual(0, malformed.returncode)
            self.assertEqual("block", json.loads(malformed.stdout)["decision"])
            hashes = {name: hashlib.sha256((cwd / name).read_bytes()).hexdigest() for name in paths}
            receipt = {"version": 1, "spec": paths[0], "behavior_matrix": paths[1], "evidence": paths[2], "artifact_hashes": hashes}
            (control / "receipts.json").write_text(json.dumps(receipt))
            valid = self.run_guard("stop", payload, cwd)
            self.assertEqual(0, valid.returncode, valid.stdout + valid.stderr)
            (cwd / paths[2]).write_text("changed")
            stale = self.run_guard("stop", payload, cwd)
            self.assertEqual(0, stale.returncode)
            self.assertIn("stale", stale.stdout)


if __name__ == "__main__":
    unittest.main()
