from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "baseline" / "skills"


class BaselineBoundaryTests(unittest.TestCase):
    def test_product_identity_is_not_spec_driven(self) -> None:
        for relative in ("AGENTS.md", "README.md", "plugins/baseline/.codex-plugin/plugin.json"):
            text = (ROOT / relative).read_text(encoding="utf-8").lower()
            self.assertNotIn("spec-driven", text, relative)
            self.assertNotIn("specification-driven development toolkit", text, relative)
        self.assertIn(
            "portable minimum for disciplined, proportional software engineering",
            (ROOT / "plugins/baseline/.codex-plugin/plugin.json").read_text(encoding="utf-8").lower(),
        )

    def test_distributed_inventory_replaces_spec_with_measurer(self) -> None:
        inventory = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertIn("measurer", inventory)
        self.assertNotIn("spec", inventory)

    def test_measurer_contract_is_ephemeral_implicit_and_risk_based(self) -> None:
        skill = (SKILLS / "measurer" / "SKILL.md").read_text(encoding="utf-8")
        metadata = (SKILLS / "measurer" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        reference = (SKILLS / "measurer" / "references" / "classification.md").read_text(encoding="utf-8")
        self.assertRegex(skill, r"(?m)^name: measurer$")
        self.assertIn("exactly one valid JSON object", skill)
        self.assertIn("conversation", skill.lower())
        self.assertRegex(skill.lower(), r"do not (?:create|write|save).*(?:file|artifact)")
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("highest applicable risk", reference.lower())
        self.assertIn("never", reference.lower())
        self.assertIn("line", reference.lower())
        self.assertRegex(reference, r"(?is)one.line.*XL|XL.*one.line")
        self.assertRegex(reference, r"(?is)hundreds.*M|M.*hundreds")

    def test_measurer_examples_use_only_the_json_contract(self) -> None:
        reference = (SKILLS / "measurer" / "references" / "classification.md").read_text(encoding="utf-8")
        examples = re.findall(r"```json\s*(\{.*?\})\s*```", reference, re.DOTALL)
        self.assertGreaterEqual(len(examples), 2)
        allowed = {"size", "drivers", "refine", "documentation", "review"}
        for raw in examples:
            payload = json.loads(raw)
            self.assertEqual(allowed, set(payload))
            self.assertIn(payload["size"], {"S", "M", "L", "XL"})
            self.assertIn(payload["review"], {"inline", "focused", "expanded", "independent"})
            self.assertEqual({"required"} | ({"reason"} if payload["refine"]["required"] else set()), set(payload["refine"]))
            for item in payload["documentation"]:
                self.assertEqual({"type", "timing"}, set(item))
                self.assertIn(item["type"], {"rfc", "adr", "c4", "api", "operations", "postmortem"})
                self.assertIn(item["timing"], {"before-implementation", "during-implementation", "after-incident"})

    def test_refine_routes_only_material_ambiguity(self) -> None:
        text = (SKILLS / "refine" / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("material ambiguity", text)
        self.assertRegex(text, r"l/xl.*without.*refine|large.*without.*refine")
        self.assertRegex(text, r"s/m.*require.*refine|small.*require.*refine")
        self.assertIn("conversation", text)
        self.assertNotIn("creates a specification", text)

    def test_tdd_starts_from_input_without_sdd_artifacts(self) -> None:
        text = "\n".join(path.read_text(encoding="utf-8") for path in (SKILLS / "tdd").rglob("*.md")).lower()
        for forbidden in ("behavior/oracle matrix", "oracle provenance", "evidence artifact", "full spec"):
            self.assertNotIn(forbidden, text)
        self.assertIn("expected behavior", text)
        self.assertIn("fail-first", text)
        self.assertIn("smallest", text)
        self.assertIn("never change an assertion", text)

    def test_bugfix_keeps_small_repairs_lightweight(self) -> None:
        text = (SKILLS / "bugfix" / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("bug report", text)
        self.assertIn("regression test", text)
        self.assertIn("s/m", text)
        self.assertIn("final response", text)
        for forbidden in ("requires a specification", "requires a behavior/oracle matrix", "requires an evidence file", "requires review files"):
            self.assertNotIn(forbidden, text)

    def test_verify_is_proportional_and_does_not_require_sdd_review_files(self) -> None:
        text = "\n".join(path.read_text(encoding="utf-8") for path in (SKILLS / "verify").rglob("*.md")).lower()
        for forbidden in ("three-phase", "three review files", "requires an evidence artifact", "canonical matrix"):
            self.assertNotIn(forbidden, text)
        for required in ("governing input", "complete diff", "unrelated", "residual risk", "inline", "focused", "expanded", "independent"):
            self.assertIn(required, text)

    def test_documentation_timing_and_eng_note_convention_are_durable(self) -> None:
        docs = "\n".join(path.read_text(encoding="utf-8") for path in (SKILLS / "docs").rglob("*.md"))
        for token in ("RFC", "ADR", "C4", "API", "operations", "postmortem"):
            self.assertIn(token, docs)
        self.assertRegex(docs, r"(?is)RFC.*before")
        self.assertRegex(docs, r"(?is)ADR.*hard-to-reverse")
        self.assertRegex(docs, r"(?is)postmortem.*after")
        for token in ("ENG-NOTE[", "bug", "invariant", "compat", "security", "decision", "rg 'ENG-NOTE\\['", "optional ID"):
            self.assertIn(token, docs)
        self.assertIn("why", docs.lower())
        self.assertNotRegex(docs, r"ENG-NOTE\[[^]]+\].*(?:increment|assign|returns the value)")

    def test_sdd_templates_and_references_are_not_distributed(self) -> None:
        for relative in (
            "templates/spec",
            "plugins/baseline/skills/spec",
            "plugins/baseline/skills/tdd/references/provenance.md",
            "plugins/baseline/skills/verify/references/review-contract.md",
            "plugins/baseline/skills/verify/assets/evidence-template.md",
        ):
            self.assertFalse((ROOT / relative).exists(), relative)

    def test_deterministic_routing_uses_measurer_and_not_spec(self) -> None:
        routing = json.loads((ROOT / "evals/promptfoo/tests/routing.yaml").read_text(encoding="utf-8"))
        routed = set()
        for item in routing:
            routed.update(item.get("skills", []))
            for key in ("skill", "expected_skill", "avoid_skill"):
                if item.get(key):
                    routed.add(item[key])
        self.assertIn("measurer", routed)
        self.assertNotIn("spec", routed)
        self.assertTrue(any(item.get("id") == "large-defined-no-refine" and item.get("avoid_skill") == "refine" for item in routing))
        self.assertTrue(any(item.get("id") == "small-ambiguous-refine" and "refine" in item.get("skills", []) for item in routing))

    def test_reconstructible_history_is_not_in_the_current_tree(self) -> None:
        for relative in (
            "docs/evidence",
            "docs/internal/audit",
            "docs/research/evidence-map.md",
            "docs/tmp/v0.1-map.md",
        ):
            self.assertFalse((ROOT / relative).exists(), relative)
        contract = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        docs_skill = (ROOT / "plugins/baseline/skills/docs/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Git is the default archive", contract)
        self.assertIn("Git as the default historical archive", docs_skill)

    def test_distribution_has_no_runtime_or_storehouse_dependency(self) -> None:
        plugin_files = [path for path in (ROOT / "plugins" / "baseline").rglob("*") if path.is_file()]
        self.assertFalse(any(path.name in {"package.json", "pyproject.toml", "requirements.txt"} for path in plugin_files))
        text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in plugin_files)
        self.assertNotIn("/Developer/woliveiras/agent-skills", text)
        self.assertNotIn("woliveiras/storehouse", text)


if __name__ == "__main__":
    unittest.main()
