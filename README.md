# Tuxedo

Tuxedo is an installable, spec-driven software engineering toolkit for coding agents. It is distributed as a Codex plugin and portable Agent Skills, and it keeps intent, behavioral oracles, implementation, evidence, and review connected throughout a change.

If you want to *use* Tuxedo with your agent, this page is enough to get started. If you want to *work on* Tuxedo itself, go to the [documentation hub](docs/README.md). I'll really appreciate your help, feedback, and contributions.

## Why Tuxedo

Coding agents drift: the code they produce can quietly diverge from what you actually asked for, and passing tests do not prove that the intended behavior was captured. Tuxedo treats the specification as an active artifact and threads a fidelity chain through every change:

```text
spec
  -> behavior and oracle matrix
  -> tests
  -> implementation
  -> evidence
  -> isolated spec / test / code review
```

A spec can be corrected when evidence exposes ambiguity or contradiction, but the tests, code, and docs must then be reconciled explicitly. Nothing silently redefines intent.

## What's inside

Tuxedo v0.1 distributes workflow skills that your agent loads on demand:

| Category | Skills |
| --- | --- |
| Change workflow | `refine`, `spec`, `tdd`, `bugfix`, `verify`, `git-commit`, `ci-workflow`, `docs` |
| Design and architecture | `shape-domain`, `design-deep-modules`, `improve-architecture`, `decision-framework` |
| Deep work (explicitly invoked) | `brainstorming`, `premortem`, `session-bridge`, `technical-research` |
| Safety | `security-review` |

Routine changes load only the smallest relevant workflow. `brainstorming`, `git-commit`, `improve-architecture`, `premortem`, `session-bridge`, and `technical-research` are explicit-only; the other workflows may be selected automatically when their descriptions match. The [catalog contract](plugins/tuxedo/skills/catalog.md) defines ownership, precedence, stop conditions, and composition without adding a runtime state machine.

## Install for Codex

Cloning the repository does not install Tuxedo. Choose either the plugin route for the complete bundle or the standalone route for direct Agent Skills. Neither route installs a Tuxedo runtime, Python, UV, or Node dependency in the consumer project.

### Option A: install the plugin

This repository includes a local marketplace entry that points to the dedicated package at `plugins/tuxedo/`. That package contains only the plugin manifest and the distributed skills; maintainer tests, evaluations, specifications, documentation, and `node_modules/` are outside it. No package-build or copy script is required.

From a trusted clone:

```bash
git clone https://github.com/woliveiras/tuxedo.git
cd tuxedo
codex plugin marketplace add "$(pwd)"
codex plugin add tuxedo@tuxedo-local
```

Start a new Codex session after installation. You can also open `/plugins` in Codex CLI, select the `tuxedo-local` marketplace, and install `tuxedo`. In Codex desktop, restart the app, open **Plugins**, choose **Tuxedo local**, install **Tuxedo**, and start a new task. The installed plugin exposes all distributed skills; you do not have to name the plugin in normal prompts.

#### Update

Pull the trusted clone, then refresh the installed cache:

```bash
codex plugin remove tuxedo@tuxedo-local
codex plugin add tuxedo@tuxedo-local
```

Start a new session afterward. The same remove/install cycle is available through `/plugins` or the desktop Plugins screen.

#### Remove

Uninstall Tuxedo, then remove the marketplace:

```bash
codex plugin remove tuxedo@tuxedo-local
codex plugin marketplace remove tuxedo-local
```

### Option B: install standalone skills

Codex discovers user skills under `$HOME/.agents/skills` and repository skills under `.agents/skills`. It follows symlinked skill directories. The canonical Tuxedo skill tree is `plugins/tuxedo/skills/`. For a personal installation from an existing trusted clone:

```bash
mkdir -p "$HOME/.agents/skills"
for skill_dir in "/absolute/path/to/tuxedo/plugins/tuxedo/skills"/*/; do
  ln -s "$skill_dir" "$HOME/.agents/skills/$(basename "$skill_dir")"
done
```

Replace the example path with the absolute path to your clone and restart Codex. For one repository only, use that repository's `.agents/skills` instead of `$HOME/.agents/skills`. Update by pulling the source clone; remove by deleting only the Tuxedo symlinks you created. Do not symlink the whole `skills/` directory as one skill.

### Discovery and invocation

- **Implicit invocation:** Codex may select an installed skill when the request matches its frontmatter description and `agents/openai.yaml` permits it. Ask for the outcome normally; no plugin name is required.
- **Explicit invocation:** use `$skill-name` in Codex CLI/IDE or choose the skill from the UI. Explicit-only Tuxedo workflows require this or an equally direct request.
- If many skills are installed, Codex may shorten or omit entries from its initial skill list because of the context budget. Use explicit invocation when you need a particular workflow deterministically.
- Clean-room Codex CLI evidence covers plugin installation, discovery of all distributed skills, removal, and reinstallation without credentials or model calls. It proves packaging and discovery, not that a model follows a skill correctly.
- The plugin is supported by Codex CLI and Codex desktop. Codex IDE supports standalone skills but not plugin installation. Tuxedo follows the portable Agent Skills format, but installation, discovery, routing, and composition in other clients remain unverified until client-specific clean-room tests are recorded.

### Optional command rules

Copy [`templates/codex/tuxedo.rules`](templates/codex/tuxedo.rules) to `.codex/rules/tuxedo.rules` in a trusted project and restart Codex. The rules ask for human approval before push, destructive Git cleanup, release, publication, deploy, selected direct remote database and project mutations, infrastructure changes, and selected direct device mutations, and forbid a few literal broad-deletion forms.

Once installed, work normally: start from the authorized task, define the oracle and run the appropriate verification fail-first, stay inside scope, review intent/tests/code separately, and inspect the staged candidate before a local commit. Each skill documents its own workflow in `SKILL.md`.

## Responsibility boundaries

Tuxedo separates command authority from workflow guidance:

- **Codex Rules** handle command-level safety through native, explicitly listed command prefixes.
- **`AGENTS.md` and skills** define the strict spec-first, oracle-first, scoped, reviewed workflow.
- **Tests and CI** provide executable evidence for product behavior.

Tuxedo does not install lifecycle hooks or require external dependencies in consumer projects. The workflow requirements are declarative rather than mechanically enforced. The maintainer is validating them across real tasks before deciding whether any narrow gate is necessary. See [the workflow boundary](docs/architecture/enforcement.md) for responsibilities and the observation protocol.

## Documentation

- **Use it:** this page, plus each skill's own `SKILL.md`.
- **Learn the vocabulary:** the [repository glossary](GLOSSARY.md) defines oracle, evidence, provenance, fail-first, and the three review phases.
- **Work on it:** the [documentation hub](docs/README.md) links the development guide, architecture, decisions (ADRs), research evidence, and the maintainer evaluation harness.

## History: from Geremmyas to Tuxedo

Tuxedo is the successor to [Geremmyas](https://github.com/woliveiras/geremmyas), an earlier project that explored spec-driven development with coding agents by combining specifications, tests, reviews, workflow guidance, and executable guardrails. Tuxedo carries that purpose forward as a portable, evidence-driven toolkit and drops the CLI and distribution machinery. It selectively adapts content from Geremmyas (MIT-licensed, same author).

The project is named after Geremmyas, my tuxedo cat and the namesake of the toolkit that preceded it.

## Provenance and influences

The workflows were informed by established engineering practice, compared for coverage with community engineering skills (including [Superpowers](https://github.com/obra/superpowers), [Spec Kit](https://github.com/github/spec-kit) and [Matt Pocock's](https://github.com/mattpocock/skills)), and reviewed against recent empirical studies. No third-party skill text or procedure is copied. Recognized design references include John Ousterhout's *A Philosophy of Software Design* and Andrew Hunt and David Thomas's *The Pragmatic Programmer*, translated into operational checks such as interface comparison, information hiding, locality, reversibility, and evidence before broad change.

Rules are labeled as empirical results, engineering heuristics, product decisions, or community inspiration; a citation does not imply that a rule is scientifically proven. Details and limitations live in [the evidence map](docs/research/evidence-map.md).

## License

Tuxedo is released under the [MIT License](LICENSE).
