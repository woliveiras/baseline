from __future__ import annotations

import json
import os
import subprocess
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_TOKEN = "tuxe" + "do"


def tracked_legacy_matches() -> list[str]:
    tracked = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    matches: list[str] = []
    for raw in tracked:
        if not raw:
            continue
        relative = raw.decode()
        path = ROOT / relative
        if not path.exists() and not path.is_symlink():
            continue
        candidate = relative.lower()
        if path.is_symlink():
            candidate += "\n" + os.readlink(path).lower()
        elif path.is_file():
            candidate += "\n" + path.read_text(encoding="utf-8", errors="ignore").lower()
        if LEGACY_TOKEN in candidate:
            matches.append(relative)
    return matches


class ProductIdentityTests(unittest.TestCase):
    def test_current_tree_has_only_the_baseline_identity(self):
        self.assertEqual([], tracked_legacy_matches())

    def test_plugin_marketplace_and_compatibility_path_are_baseline(self):
        marketplace = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        plugin = json.loads(
            (ROOT / "plugins/baseline/.codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual("baseline", marketplace["name"])
        self.assertEqual("Baseline", marketplace["interface"]["displayName"])
        self.assertEqual("baseline", marketplace["plugins"][0]["name"])
        self.assertEqual(
            {"source": "local", "path": "./plugins/baseline"},
            marketplace["plugins"][0]["source"],
        )
        self.assertEqual("baseline", plugin["name"])
        self.assertEqual("Baseline", plugin["interface"]["displayName"])
        self.assertEqual("plugins/baseline/skills", os.readlink(ROOT / "skills"))
        self.assertFalse((ROOT / "plugins" / LEGACY_TOKEN).exists())

    def test_development_packages_and_release_paths_are_baseline(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        lock = tomllib.loads((ROOT / "uv.lock").read_text(encoding="utf-8"))
        release = json.loads((ROOT / "release-please-config.json").read_text(encoding="utf-8"))
        self.assertEqual("baseline", package["name"])
        self.assertEqual("baseline", project["project"]["name"])
        self.assertIn("baseline", {item["name"] for item in lock["package"]})
        root_release = release["packages"]["."]
        self.assertEqual("baseline", root_release["package-name"])
        self.assertIn(
            "plugins/baseline/.codex-plugin/plugin.json",
            {item["path"] for item in root_release["extra-files"]},
        )
        self.assertTrue((ROOT / "templates/codex/baseline.rules").is_file())

    def test_evaluation_identity_and_control_condition_are_unambiguous(self):
        eval_sources = "\n".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in (
                "evals/run.py",
                "evals/promptfoo/assertions/workspace.py",
                "evals/promptfoo/scripts/prepare-workspaces.py",
                "evals/promptfoo/scripts/run-evaluations.py",
            )
        )
        config = (ROOT / "evals/promptfoo/promptfooconfig.yaml").read_text(encoding="utf-8")
        self.assertIn("BASELINE_EVAL_", eval_sources)
        self.assertNotIn(LEGACY_TOKEN.upper(), eval_sources)
        self.assertIn('"control"', eval_sources)
        self.assertNotRegex(
            eval_sources,
            r'(?:VARIANTS|CONDITIONS)\s*=\s*\("' + "base" + r'line"',
        )
        self.assertIn("label: control", config)
        self.assertNotIn("label: " + "base" + "line", config)

    def test_readme_describes_the_product_and_storehouse_relationship(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("# Baseline", readme)
        self.assertIn("Baseline is the portable minimum for disciplined software engineering.", readme)
        self.assertIn("## From Geremmyas to Baseline", readme)
        self.assertIn("woliveiras/baseline", readme)
        self.assertIn("baseline@baseline", readme)
        self.assertIn("Storehouse", readme)


if __name__ == "__main__":
    unittest.main()
