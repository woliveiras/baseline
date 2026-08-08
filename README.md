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

### Option A: install from the GitHub marketplace

For another machine, install Tuxedo without keeping a local Tuxedo checkout. Codex fetches the GitHub marketplace snapshot, reads its committed `.agents/plugins/marketplace.json`, and then installs the package at `plugins/tuxedo/`.

This repository is public. Install the stable release from its immutable tag:

```bash
codex plugin marketplace add woliveiras/tuxedo --ref v0.1.0
codex plugin add tuxedo@tuxedo
```

The `woliveiras/tuxedo` shorthand uses HTTPS. The marketplace and plugin are both named `tuxedo`; `tuxedo@tuxedo` is `plugin@marketplace`, not `name@version`. The installed manifest reports version `0.1.0` separately. Start a new Codex session after installation. You can also open `/plugins` in Codex CLI, select the **Tuxedo** marketplace, and install **Tuxedo**. In Codex desktop, restart the app, open **Plugins**, choose **Tuxedo**, install **Tuxedo**, and start a new task. The installed plugin exposes all distributed skills; you do not have to name the plugin in normal prompts.

#### Optional sparse checkout

To fetch only the two paths needed to resolve and install the plugin, repeat `--sparse` for the marketplace manifest and the package. This HTTPS form has the same access requirement described above:

```bash
codex plugin marketplace add woliveiras/tuxedo --ref v0.1.0 \
  --sparse .agents/plugins/marketplace.json \
  --sparse plugins/tuxedo
codex plugin add tuxedo@tuxedo
```

For a private fork, use the same sparse paths with an SSH source after configuring GitHub access on the machine:

```bash
codex plugin marketplace add git@github.com:OWNER/tuxedo.git --ref v0.1.0 \
  --sparse .agents/plugins/marketplace.json \
  --sparse plugins/tuxedo
codex plugin add tuxedo@tuxedo
```

Do not omit either sparse path: the manifest selects the plugin and `plugins/tuxedo/` contains the manifest and distributed skills.

#### Private forks and credentials

For a private fork, use an SSH Git URL after configuring the machine's GitHub SSH access:

```bash
codex plugin marketplace add git@github.com:OWNER/tuxedo.git --ref v0.1.0
codex plugin add tuxedo@tuxedo
```

Codex account authentication and GitHub repository authentication are separate. The former is used by Codex itself; the latter is used by Git to fetch a private marketplace. A public repository does not require a GitHub credential for this fetch. No credential, token, private key, or credential-bearing URL belongs in commands committed to documentation or in the repository. Configure SSH keys, an agent, or an approved Git credential helper on the machine instead.

#### Update

Tags are immutable, so upgrading replaces the configured marketplace ref and then reinstalls the plugin. For example, after `v0.2.0` exists:

```bash
codex plugin remove tuxedo@tuxedo
codex plugin marketplace remove tuxedo
codex plugin marketplace add woliveiras/tuxedo --ref v0.2.0
codex plugin add tuxedo@tuxedo
```

Start a new session afterward. The same lifecycle is available through `/plugins` or the desktop Plugins screen. `v0.1.0` is immutable; a later version always uses a new tag.

#### Reinstall and Remove

To reinstall only Tuxedo:

```bash
codex plugin remove tuxedo@tuxedo
codex plugin add tuxedo@tuxedo
```

To remove Tuxedo completely, uninstall the plugin before removing its marketplace:

```bash
codex plugin remove tuxedo@tuxedo
codex plugin marketplace remove tuxedo
```

The supported remote route is marketplace-first. Do not use `codex plugin add <URL>`; `codex plugin add` receives the `plugin@marketplace` selector after the marketplace has been configured. For unreleased testing only, `--ref main` remains a mutable development channel; review its source before use and do not treat it as a reproducible release.

### Option B: clone locally for development

This repository includes a local marketplace entry that points to the dedicated package at `plugins/tuxedo/`. That package contains only the plugin manifest and the distributed skills; repository-only tests, evaluations, specifications, documentation, and `node_modules/` are outside it. No package-build or copy script is required. Preserve this flow for developing Tuxedo itself:

```bash
git clone https://github.com/woliveiras/tuxedo.git
cd tuxedo
codex plugin marketplace add "$(pwd)"
codex plugin add tuxedo@tuxedo
```

This local-clone route is for people working on the checkout. It is not required for the remote installation above.

### Option C: install standalone skills

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
- Local clean-room Codex CLI evidence covers plugin installation, discovery of all distributed skills, removal, and reinstallation without Codex authentication or model calls. A separate remote clean-room run verified the same lifecycle over SSH using machine-managed GitHub access. These checks prove packaging and discovery, not that a model follows a skill correctly.
- The plugin is supported by Codex CLI and Codex desktop. Codex IDE supports standalone skills but not plugin installation. Tuxedo follows the portable Agent Skills format, but installation, discovery, routing, and composition in other clients remain unverified until client-specific clean-room tests are recorded.

### Optional command rules

Copy [`templates/codex/tuxedo.rules`](templates/codex/tuxedo.rules) to `.codex/rules/tuxedo.rules` in a trusted project and restart Codex. The rules ask for human approval before push, destructive Git cleanup, release, publication, deploy, selected direct remote database and project mutations, infrastructure changes, and selected direct device mutations, and forbid a few literal broad-deletion forms.

Once installed, work normally: start from the authorized task, define the oracle and run the appropriate verification fail-first, stay inside scope, review intent/tests/code separately, and inspect the staged candidate before a local commit. Each skill documents its own workflow in `SKILL.md`.

## Responsibility boundaries

Tuxedo separates command authority from workflow guidance:

- **Codex Rules** handle command-level safety through native, explicitly listed command prefixes.
- **`AGENTS.md` and skills** define the strict spec-first, oracle-first, scoped, reviewed workflow.
- **Tests and CI** provide executable evidence for product behavior.

Tuxedo does not install lifecycle hooks or require external dependencies in consumer projects. The workflow requirements are declarative rather than mechanically enforced. They are being validated across real repository tasks before any narrow gate is considered. See [the workflow boundary](docs/architecture/enforcement.md) for responsibilities and the observation protocol.

## Documentation

- **Use it:** this page, plus each skill's own `SKILL.md`.
- **Learn the vocabulary:** the [repository glossary](GLOSSARY.md) defines oracle, evidence, provenance, fail-first, and the three review phases.
- **Work on it:** the [documentation hub](docs/README.md) links the development guide, architecture, decisions (ADRs), research evidence, and the development-only evaluation harness.
- **Release it:** the [release guide](docs/releases.md) defines the single product version, protected automation, verification, and rollback.

## History: from Geremmyas to Tuxedo

Tuxedo is the successor to [Geremmyas](https://github.com/woliveiras/geremmyas), an earlier project that explored spec-driven development with coding agents by combining specifications, tests, reviews, workflow guidance, and executable guardrails. Tuxedo carries that purpose forward as a portable, evidence-driven toolkit and drops the CLI and distribution machinery. It selectively adapts content from Geremmyas (MIT-licensed, same author).

The project is named after Geremmyas, my tuxedo cat and the namesake of the toolkit that preceded it.

## Provenance and influences

The workflows were informed by established engineering practice, compared for coverage with community engineering skills (including [Superpowers](https://github.com/obra/superpowers), [Spec Kit](https://github.com/github/spec-kit) and [Matt Pocock's](https://github.com/mattpocock/skills)), and reviewed against recent empirical studies. No third-party skill text or procedure is copied. Recognized design references include John Ousterhout's *A Philosophy of Software Design* and Andrew Hunt and David Thomas's *The Pragmatic Programmer*, translated into operational checks such as interface comparison, information hiding, locality, reversibility, and evidence before broad change.

Rules are labeled as empirical results, engineering heuristics, product decisions, or community inspiration; a citation does not imply that a rule is scientifically proven. Details and limitations live in [the evidence map](docs/research/evidence-map.md).

## License

Tuxedo is released under the [MIT License](LICENSE).
