from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "hooks" / "scripts" / "guard.py"
RULES = ROOT / "templates" / "codex" / "tuxedo.rules"
EXPECTED_SKILLS = {
    "refine", "brainstorming", "spec", "tdd", "bugfix", "verify", "docs",
    "git-commit", "ci-workflow", "shape-domain", "design-deep-modules",
    "improve-architecture", "decision-framework", "premortem", "session-bridge",
    "technical-research", "security-review",
}

sys.path.insert(0, str(ROOT / "evals"))
from run import apply_process_checks, parse_events  # noqa: E402
from verifiers import snapshot, verify  # noqa: E402


def digest_object(value: dict) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def digest_map(value: dict[str, str]) -> str:
    return digest_object(value)


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.exists(), f"{path}: {target}")

    def test_maintainer_content_is_not_referenced_as_installed_content(self):
        manifest = (ROOT / ".codex-plugin" / "plugin.json").read_text()
        for name in ("docs/", "tests/", "evals/"):
            self.assertNotIn(name, manifest)
        corpus = "\n".join(path.read_text(errors="ignore") for path in (ROOT / "skills").rglob("*") if path.is_file())
        for forbidden in ("geremmyas ", "go:embed", "geremmyas.yml", "internal/cli", "catalog/packs"):
            self.assertNotIn(forbidden, corpus.lower())

    def test_canonical_templates_are_kept_in_sync(self):
        pairs = [
            ("templates/spec/spec.md", "skills/spec/assets/spec-template.md"),
            ("templates/spec/behavior-matrix.md", "skills/spec/assets/behavior-matrix-template.md"),
            ("templates/spec/evidence.md", "skills/verify/assets/evidence-template.md"),
            ("templates/review/spec.json", "skills/verify/assets/spec-review.json"),
            ("templates/review/tests.json", "skills/verify/assets/test-review.json"),
            ("templates/review/code.json", "skills/verify/assets/code-review.json"),
            ("skills/spec/references/scope-tiers.md", "skills/verify/references/scope-tiers.md"),
        ]
        for left, right in pairs:
            self.assertEqual((ROOT / left).read_bytes(), (ROOT / right).read_bytes(), f"{left} != {right}")
        self.assertNotIn("## Behavior and oracle matrix", (ROOT / "templates/spec/spec.md").read_text())
        self.assertFalse((ROOT / "templates/policy/authority.json").exists())

    def test_eval_dry_run_is_seeded_and_covers_all_comparisons(self):
        command = ["python3", str(ROOT / "evals" / "run.py"), "--dry-run", "--seed", "17"]
        first = subprocess.run(command, text=True, capture_output=True, check=False)
        second = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        runs = payload["runs"]
        self.assertEqual(48, len(runs))
        self.assertEqual({"baseline", "core", "focal", "broad", "current", "proposed"}, {run["variant"] for run in runs})
        self.assertTrue(all("verifier" in run and "repetition" in run for run in runs))
        self.assertRegex(payload["current_fingerprint"], r"^[0-9a-f]{64}$")

    def test_eval_rejects_same_current_and_proposed_root(self):
        result = subprocess.run(
            [
                "python3", str(ROOT / "evals" / "run.py"), "--execute",
                "--variant", "proposed", "--task", "clear-local-change",
                "--proposed-root", str(ROOT),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("must differ", result.stderr)

    def test_eval_rejects_distinct_paths_with_identical_toolkit_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            candidate = Path(tmp) / "candidate"
            candidate.mkdir()
            shutil.copy2(ROOT / "AGENTS.md", candidate / "AGENTS.md")
            shutil.copytree(ROOT / "skills", candidate / "skills")
            result = subprocess.run(
                [
                    "python3", str(ROOT / "evals" / "run.py"), "--execute",
                    "--variant", "proposed", "--task", "clear-local-change",
                    "--proposed-root", str(candidate),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(0, result.returncode)
            self.assertIn("different AGENTS.md or skill content", result.stderr)

    def test_eval_rejects_a_noop_process_as_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "result.json"
            result = subprocess.run(
                [
                    "python3", str(ROOT / "evals" / "run.py"), "--execute",
                    "--variant", "baseline", "--task", "no-change-correct",
                    "--codex", "/usr/bin/true", "--timeout", "5",
                    "--output", str(output),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            payload = json.loads(output.read_text())
            self.assertEqual({"pass": 0, "needs-review": 0, "fail": 1}, payload["summary"])
            checks = {item["id"]: item for item in payload["runs"][0]["verification"]["checks"]}
            self.assertTrue(checks["codex-process"]["pass"])
            self.assertFalse(checks["final-response"]["pass"])
            self.assertFalse(checks["codex-turn-completed"]["pass"])


class CodexRulesTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("codex"), "Codex CLI is required to validate native rules")
    def test_rules_load_and_classify_direct_commands(self):
        cases = [
            (["rm", "-rf", "/"], "forbidden"),
            (["rm", "-r", "-f", "/"], "forbidden"),
            (["git", "push", "origin", "main"], "prompt"),
            (["gh", "release", "view", "v1.0.0"], None),
            (["terraform", "destroy"], "prompt"),
            (["rg", "push", "README.md"], None),
            (["git", "-C", ".", "push"], None),
        ]
        for command, expected in cases:
            result = subprocess.run(
                ["codex", "execpolicy", "check", "--rules", str(RULES), "--", *command],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(expected, json.loads(result.stdout).get("decision"), command)


class HookTests(unittest.TestCase):
    def run_guard(self, mode: str, payload: str, cwd: Path):
        payload = payload.replace("FIXTURE_CWD", str(cwd))
        return subprocess.run(["python3", str(GUARD), mode], input=payload, text=True, capture_output=True, check=False)

    def fixture(self, name: str) -> str:
        return (ROOT / "tests" / "fixtures" / "hooks" / name).read_text()

    def payload(self, cwd: Path, command: str) -> str:
        return json.dumps({
            "cwd": str(cwd),
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": command},
        })

    def policy(self, required_trees: list[str] | None = None) -> dict:
        return {
            "version": 1,
            "require_receipts_on": ["commit", "stop"],
            "receipt_path": ".tuxedo/receipts.json",
            "required_trees": required_trees if required_trees is not None else ["tests", "implementation"],
            "tree_scopes": {
                "tests": {"include": ["tests/**/*"], "exclude": []},
                "implementation": {"include": ["src/**/*"], "exclude": []},
            },
            "allow_tree_overlap": False,
        }

    def write_receipt(self, cwd: Path, *, documentation: str = "required") -> dict:
        control = cwd / ".tuxedo"
        control.mkdir(exist_ok=True)
        files = {
            "spec.md": "# Spec\n",
            "matrix.md": "# Matrix\n",
            "evidence.md": "# Evidence\n",
            "tests/test_example.py": "def test_example():\n    assert True\n",
            "src/example.py": "VALUE = 1\n",
        }
        if documentation == "required":
            files["README.md"] = "# Example\n"
        for relative, content in files.items():
            path = cwd / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)

        tests = {"tests/test_example.py": hash_file(cwd / "tests/test_example.py")}
        implementation = {"src/example.py": hash_file(cwd / "src/example.py")}
        test_evidence = {
            "fail_first": {
                "test_tree": digest_map(tests),
                "command": "python3 -m unittest tests/test_example.py",
                "observed_failure": "expected VALUE behavior was absent",
            },
            "passing": {
                "test_tree": digest_map(tests),
                "command": "python3 -m unittest tests/test_example.py",
                "observed_result": "focused test passed",
            },
        }
        artifacts = {name: hash_file(cwd / name) for name in ("spec.md", "matrix.md", "evidence.md")}

        reviews_dir = cwd / "reviews"
        reviews_dir.mkdir(exist_ok=True)
        spec_review = {
            "version": 1,
            "phase": "spec",
            "status": "approved",
            "context": {"tests_exposed": False, "implementation_exposed": False},
            "input_hashes": {"spec": artifacts["spec.md"]},
            "output_hashes": {"behavior_matrix": artifacts["matrix.md"]},
            "findings": [],
        }
        (reviews_dir / "spec.json").write_text(json.dumps(spec_review))
        artifacts["reviews/spec.json"] = hash_file(reviews_dir / "spec.json")

        test_review = {
            "version": 1,
            "phase": "tests",
            "status": "approved",
            "context": {"tests_exposed": True, "implementation_exposed": False},
            "input_hashes": {
                "spec": artifacts["spec.md"],
                "behavior_matrix": artifacts["matrix.md"],
                "tests": digest_map(tests),
                "spec_review": artifacts["reviews/spec.json"],
                "fail_first": digest_object(test_evidence["fail_first"]),
            },
            "output_hashes": {},
            "findings": [],
        }
        (reviews_dir / "tests.json").write_text(json.dumps(test_review))
        artifacts["reviews/tests.json"] = hash_file(reviews_dir / "tests.json")

        docs = {
            "decision": documentation,
            "rationale": "The public behavior changed." if documentation == "required" else "No user-facing or durable contract changed.",
            "artifacts": ["README.md"] if documentation == "required" else [],
        }
        if documentation == "required":
            artifacts["README.md"] = hash_file(cwd / "README.md")
        docs_value = {
            "decision": docs["decision"],
            "rationale": docs["rationale"],
            "artifact_hashes": {path: artifacts[path] for path in docs["artifacts"]},
        }
        docs_digest = hashlib.sha256(
            json.dumps(docs_value, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

        code_review = {
            "version": 1,
            "phase": "code",
            "status": "approved",
            "context": {"tests_exposed": True, "implementation_exposed": True},
            "input_hashes": {
                "spec": artifacts["spec.md"],
                "behavior_matrix": artifacts["matrix.md"],
                "tests": digest_map(tests),
                "implementation": digest_map(implementation),
                "evidence": artifacts["evidence.md"],
                "test_review": artifacts["reviews/tests.json"],
                "test_evidence": digest_object(test_evidence),
                "documentation": docs_digest,
            },
            "output_hashes": {},
            "findings": [],
        }
        (reviews_dir / "code.json").write_text(json.dumps(code_review))
        artifacts["reviews/code.json"] = hash_file(reviews_dir / "code.json")

        receipt = {
            "version": 2,
            "spec": "spec.md",
            "behavior_matrix": "matrix.md",
            "evidence": "evidence.md",
            "trees": {"tests": tests, "implementation": implementation},
            "test_evidence": test_evidence,
            "documentation": docs,
            "reviews": {
                "spec": "reviews/spec.json",
                "tests": "reviews/tests.json",
                "code": "reviews/code.json",
            },
            "artifact_hashes": artifacts,
        }
        (control / "receipts.json").write_text(json.dumps(receipt))
        return receipt

    def test_valid_invalid_absent_and_malformed_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            ok = self.run_guard("pre-tool", self.fixture("pretool-valid.json"), cwd)
            self.assertEqual(0, ok.returncode, ok.stdout + ok.stderr)
            self.assertEqual("", ok.stdout)
            for name in ("pretool-missing.json", "pretool-malformed.json"):
                result = self.run_guard("pre-tool", self.fixture(name), cwd)
                self.assertEqual(0, result.returncode, name)
                self.assertEqual("deny", json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"])

    def test_command_language_is_not_used_as_a_security_classifier(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            for command in (
                "rg production README.md",
                "git commit-message --help",
                "printf 'DELETE FROM users'",
                "rm -rf /",
                "git push origin main",
            ):
                result = self.run_guard("pre-tool", self.payload(cwd, command), cwd)
                self.assertEqual(0, result.returncode, command)
                self.assertEqual("", result.stdout, command)

    def test_direct_commit_and_stop_validate_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            control = cwd / ".tuxedo"
            control.mkdir()
            (control / "policy.json").write_text(json.dumps(self.policy()))
            denied = self.run_guard("pre-tool", self.payload(cwd, 'git commit -m "feat: example"'), cwd)
            self.assertEqual("deny", json.loads(denied.stdout)["hookSpecificOutput"]["permissionDecision"])

            self.write_receipt(cwd)
            allowed = self.run_guard("pre-tool", self.payload(cwd, 'git commit -m "feat: example"'), cwd)
            self.assertEqual("", allowed.stdout)
            stop_payload = json.dumps({"cwd": str(cwd), "hook_event_name": "Stop"})
            stopped = self.run_guard("stop", stop_payload, cwd)
            self.assertEqual("", stopped.stdout)

    def test_receipts_detect_stale_trees_reviews_and_documentation(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            control = cwd / ".tuxedo"
            control.mkdir()
            policy = self.policy()
            policy["require_receipts_on"] = ["stop"]
            (control / "policy.json").write_text(json.dumps(policy))
            payload = json.dumps({"cwd": str(cwd), "hook_event_name": "Stop"})

            self.write_receipt(cwd)
            (cwd / "tests/test_example.py").write_text("def test_example():\n    assert False\n")
            stale_test = self.run_guard("stop", payload, cwd)
            self.assertIn("Test tree is stale", json.loads(stale_test.stdout)["reason"])

            self.write_receipt(cwd)
            spec_review_path = cwd / "reviews/spec.json"
            spec_review = json.loads(spec_review_path.read_text())
            spec_review["context"]["implementation_exposed"] = True
            spec_review_path.write_text(json.dumps(spec_review))
            receipt = json.loads((control / "receipts.json").read_text())
            receipt["artifact_hashes"]["reviews/spec.json"] = hash_file(spec_review_path)
            (control / "receipts.json").write_text(json.dumps(receipt))
            exposed = self.run_guard("stop", payload, cwd)
            self.assertIn("Spec review must declare", json.loads(exposed.stdout)["reason"])

            self.write_receipt(cwd)
            (cwd / "README.md").write_text("# Changed\n")
            stale_docs = self.run_guard("stop", payload, cwd)
            self.assertIn("Completion artifact hashes is stale", json.loads(stale_docs.stdout)["reason"])

            self.write_receipt(cwd)
            receipt = json.loads((control / "receipts.json").read_text())
            receipt["test_evidence"]["fail_first"]["test_tree"] = "0" * 64
            (control / "receipts.json").write_text(json.dumps(receipt))
            stale_red = self.run_guard("stop", payload, cwd)
            self.assertIn("fail_first record is stale", json.loads(stale_red.stdout)["reason"])

    def test_receipts_cover_exact_configured_tree_scopes(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            control = cwd / ".tuxedo"
            control.mkdir()
            policy = self.policy()
            policy["require_receipts_on"] = ["stop"]
            (control / "policy.json").write_text(json.dumps(policy))
            payload = json.dumps({"cwd": str(cwd), "hook_event_name": "Stop"})

            self.write_receipt(cwd)
            unlisted = cwd / "tests/unlisted.py"
            unlisted.write_text("raise AssertionError('must be covered')\n")
            omitted = self.run_guard("stop", payload, cwd)
            self.assertIn("Test tree omits scoped artifact", json.loads(omitted.stdout)["reason"])

            unlisted.unlink()
            receipt = self.write_receipt(cwd)
            receipt["trees"]["tests"]["spec.md"] = hash_file(cwd / "spec.md")
            (control / "receipts.json").write_text(json.dumps(receipt))
            outside = self.run_guard("stop", payload, cwd)
            self.assertIn("Test tree contains artifact outside its scope", json.loads(outside.stdout)["reason"])

    def test_not_required_documentation_is_explicit_and_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            control = cwd / ".tuxedo"
            control.mkdir()
            policy = self.policy()
            policy["require_receipts_on"] = ["stop"]
            (control / "policy.json").write_text(json.dumps(policy))
            self.write_receipt(cwd, documentation="not-required")
            result = self.run_guard(
                "stop",
                json.dumps({"cwd": str(cwd), "hook_event_name": "Stop"}),
                cwd,
            )
            self.assertEqual("", result.stdout, result.stdout)


class EvaluationVerifierTests(unittest.TestCase):
    def catalog(self) -> dict:
        return json.loads((ROOT / "evals" / "fixtures" / "catalog.json").read_text())

    def task(self, name: str) -> dict:
        return json.loads((ROOT / "evals" / "tasks" / f"{name}.json").read_text())

    def materialize(self, workspace: Path, fixture: str) -> None:
        for relative, content in self.catalog()[fixture].items():
            path = workspace / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)

    def test_behavior_verifiers_use_hidden_oracles_not_response_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.materialize(workspace, "clear-local-change")
            before = snapshot(workspace)
            (workspace / "app.py").write_text("def double(value):\n    return value * 2\n")
            result = verify(self.task("clear-local-change"), workspace, before)
            self.assertEqual("pass", result["status"])

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.materialize(workspace, "clear-local-change")
            before = snapshot(workspace)
            (workspace / "README.md").write_text("AC-001 test pass\n")
            result = verify(self.task("clear-local-change"), workspace, before)
            self.assertEqual("fail", result["status"])

    def test_bug_verifier_requires_behavior_and_regression_assertion(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.materialize(workspace, "bug-with-regression")
            before = snapshot(workspace)
            (workspace / "clamp.py").write_text(
                "def clamp(value, low, high):\n"
                "    return max(low, min(value, high))\n"
            )
            (workspace / "test_clamp.py").write_text(
                "from clamp import clamp\n\n"
                "def test_upper_bound():\n"
                "    assert clamp(9, 1, 5) == 5\n"
            )
            result = verify(self.task("bug-with-regression"), workspace, before)
            self.assertEqual("pass", result["status"])

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.materialize(workspace, "bug-with-regression")
            before = snapshot(workspace)
            (workspace / "clamp.py").write_text(
                "def clamp(value, low, high):\n"
                "    return max(low, min(value, high))\n"
            )
            (workspace / "test_clamp.py").write_text(
                "from clamp import clamp\n\n"
                "def test_upper_bound():\n"
                "    if False:\n"
                "        assert clamp(9, 1, 5) == 5\n"
            )
            result = verify(self.task("bug-with-regression"), workspace, before)
            self.assertEqual("fail", result["status"])
            self.assertFalse(next(check for check in result["checks"] if check["id"] == "regression-assertion")["pass"])

    def test_process_checks_require_answer_and_completed_codex_turn(self):
        verification = {"status": "pass", "checks": []}
        count, usage, completed_turn = parse_events("")
        self.assertEqual((0, {}, False), (count, usage, completed_turn))
        apply_process_checks(
            verification,
            exit_code=0,
            timed_out=False,
            answer="",
            completed_turn=completed_turn,
        )
        self.assertEqual("fail", verification["status"])

        verification = {"status": "pass", "checks": []}
        count, usage, completed_turn = parse_events(
            '{"type":"turn.completed","usage":{"input_tokens":12,"output_tokens":3}}\n'
        )
        self.assertEqual(1, count)
        self.assertEqual({"input_tokens": 12, "output_tokens": 3}, usage)
        apply_process_checks(
            verification,
            exit_code=0,
            timed_out=False,
            answer="Done.",
            completed_turn=completed_turn,
        )
        self.assertEqual("pass", verification["status"])

    def test_semantic_tasks_never_auto_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.materialize(workspace, "real-ambiguity")
            before = snapshot(workspace)
            result = verify(self.task("real-ambiguity"), workspace, before)
            self.assertEqual("needs-review", result["status"])

    def test_no_change_task_checks_behavior_and_unchanged_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp)
            self.materialize(workspace, "no-change-correct")
            before = snapshot(workspace)
            result = verify(self.task("no-change-correct"), workspace, before)
            self.assertEqual("pass", result["status"])


if __name__ == "__main__":
    unittest.main()
