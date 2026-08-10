# Baseline

Baseline is the portable minimum for disciplined software engineering. It is distributed as portable Agent Skills inside one open Agent Plugin package, with thin declarative adapters for clients that require their own package contract.

If you want to *use* Baseline with your agent, this page is enough to get started. If you want to *work on* Baseline itself, go to the [documentation hub](docs/README.md). I'll really appreciate your help, feedback, and contributions.

## Why Baseline

Coding agents drift, overcomplicate routine work, and may cross authority boundaries. Baseline keeps the engineering foundation small while making risk, ambiguity, verification, durable knowledge, review, and Git authority explicit:

```text
input
  -> measurer
  -> refine or decision documentation only when needed
  -> fail-first tests
  -> implementation
  -> durable documentation when applicable
  -> proportional review
  -> explicitly authorized Git operation
```

The input can be a request, issue, bug report, external contract, accepted architecture decision, or explicitly approved behavior. Baseline does not require a persistent specification, behavior/oracle matrix, formal provenance, evidence file, or review file. Teams that choose Specification-Driven Development can install the independent `sdd` collection from [Storehouse](https://github.com/woliveiras/storehouse); Baseline does not depend on it.

## What's inside

Baseline distributes workflow skills that your agent loads on demand:

| Category | Skills |
| --- | --- |
| Change workflow | `measurer`, `refine`, `tdd`, `bugfix`, `verify`, `git-commit`, `ci-workflow`, `docs` |
| Design and architecture | `shape-domain`, `design-deep-modules`, `improve-architecture`, `decision-framework` |
| Deep work (explicitly invoked) | `brainstorming`, `premortem`, `session-bridge`, `technical-research` |
| Safety | `security-review` |

`measurer` is intentionally concise and implicitly classifies work by the highest applicable risk, never line count. `refine` follows only when material ambiguity remains. Baseline classifies `brainstorming`, `git-commit`, `improve-architecture`, `premortem`, `session-bridge`, and `technical-research` as explicit-only; the other workflows may be selected automatically when their descriptions match. Codex preserves this policy through `agents/openai.yaml`. Other clients do not share one portable invocation-policy contract, so their limitation is documented below instead of being hidden behind custom metadata. The [catalog contract](plugins/baseline/skills/catalog.md) defines ownership, precedence, stop conditions, and composition without adding a runtime state machine.

## Package architecture

The complete consumer package is [`plugins/baseline/`](plugins/baseline/). It has one canonical `skills/` tree and no copied or generated client variants:

- `plugin.json` implements the open [Agent Plugins 1.0.0](https://agent-plugins.org/) package manifest used by compatible clients such as Cursor and GitHub Copilot;
- `.codex-plugin/plugin.json` preserves the existing Codex package and marketplace lifecycle;
- `.claude-plugin/plugin.json` is the minimal Claude Code package adapter;
- `package.json` is a private, dependency-free Pi package descriptor whose exact allowlist selects the 17 canonical `SKILL.md` files;
- `skills/` contains all behavior, references, assets, scripts, and Codex invocation metadata.

The repository-level `.github/plugin/marketplace.json` adds the native Copilot marketplace lifecycle while pointing to that same package. The adapters and marketplaces add identity, selection, and lifecycle metadata only. They contain no hooks, dependencies, scripts, runtime, copied skills, or client-specific behavior. The root [`skills`](skills) compatibility symlink points to the same canonical tree. Release Please updates every product manifest and marketplace version from one product version.

## Install

### Codex

Cloning the repository does not install Baseline. Choose either the plugin route for the complete bundle or the standalone route for direct Agent Skills. Neither route installs a Baseline runtime, Python, UV, or Node dependency in the consumer project.

### Option A: install from the GitHub marketplace

For another machine, install Baseline without keeping a local Baseline checkout. Codex fetches the GitHub marketplace snapshot, reads its committed `.agents/plugins/marketplace.json`, and then installs the package at `plugins/baseline/`.

This repository is public. Install the stable release from its immutable tag:

```bash
# x-release-please-start-version
codex plugin marketplace add woliveiras/baseline --ref v0.2.0
codex plugin add baseline@baseline
# x-release-please-end
```

<!-- x-release-please-start-version -->
The `woliveiras/baseline` shorthand uses HTTPS. The marketplace and plugin are both named `baseline`; `baseline@baseline` is `plugin@marketplace`, not `name@version`. The installed manifest reports version `0.2.0` separately. Start a new Codex session after installation. You can also open `/plugins` in Codex CLI, select the **Baseline** marketplace, and install **Baseline**. In Codex desktop, restart the app, open **Plugins**, choose **Baseline**, install **Baseline**, and start a new task. The installed plugin exposes all distributed skills; you do not have to name the plugin in normal prompts.
<!-- x-release-please-end -->

#### Optional sparse checkout

To fetch only the two paths needed to resolve and install the plugin, repeat `--sparse` for the marketplace manifest and the package. This HTTPS form has the same access requirement described above:

```bash
# x-release-please-start-version
codex plugin marketplace add woliveiras/baseline --ref v0.2.0 \
  --sparse .agents/plugins/marketplace.json \
  --sparse plugins/baseline
codex plugin add baseline@baseline
# x-release-please-end
```

For a private fork, use the same sparse paths with an SSH source after configuring GitHub access on the machine:

```bash
# x-release-please-start-version
codex plugin marketplace add git@github.com:OWNER/baseline.git --ref v0.2.0 \
  --sparse .agents/plugins/marketplace.json \
  --sparse plugins/baseline
codex plugin add baseline@baseline
# x-release-please-end
```

Do not omit either sparse path: the manifest selects the plugin and `plugins/baseline/` contains the manifest and distributed skills.

#### Private forks and credentials

For a private fork, use an SSH Git URL after configuring the machine's GitHub SSH access:

```bash
# x-release-please-start-version
codex plugin marketplace add git@github.com:OWNER/baseline.git --ref v0.2.0
codex plugin add baseline@baseline
# x-release-please-end
```

Codex account authentication and GitHub repository authentication are separate. The former is used by Codex itself; the latter is used by Git to fetch a private marketplace. A public repository does not require a GitHub credential for this fetch. No credential, token, private key, or credential-bearing URL belongs in commands committed to documentation or in the repository. Configure SSH keys, an agent, or an approved Git credential helper on the machine instead.

#### Update

Tags are immutable, so upgrading replaces the configured marketplace ref and then reinstalls the plugin. For example, after `v0.2.0` exists:

```bash
codex plugin remove baseline@baseline
codex plugin marketplace remove baseline
codex plugin marketplace add woliveiras/baseline --ref v0.2.0
codex plugin add baseline@baseline
```

<!-- x-release-please-start-version -->
Start a new session afterward. The same lifecycle is available through `/plugins` or the desktop Plugins screen. `v0.2.0` is immutable; a later version always uses a new tag.
<!-- x-release-please-end -->

#### Reinstall and Remove

To reinstall only Baseline:

```bash
codex plugin remove baseline@baseline
codex plugin add baseline@baseline
```

To remove Baseline completely, uninstall the plugin before removing its marketplace:

```bash
codex plugin remove baseline@baseline
codex plugin marketplace remove baseline
```

The supported remote route is marketplace-first. Do not use `codex plugin add <URL>`; `codex plugin add` receives the `plugin@marketplace` selector after the marketplace has been configured. For unreleased testing only, `--ref main` remains a mutable development channel; review its source before use and do not treat it as a reproducible release.

### Option B: clone locally for development

This repository includes a local marketplace entry that points to the dedicated package at `plugins/baseline/`. That package contains only the plugin manifest and the distributed skills; repository-only tests, evaluations, documentation, and `node_modules/` are outside it. No package-build or copy script is required. Preserve this flow for developing Baseline itself:

```bash
git clone https://github.com/woliveiras/baseline.git
cd baseline
codex plugin marketplace add "$(pwd)"
codex plugin add baseline@baseline
```

This local-clone route is for people working on the checkout. It is not required for the remote installation above.

### Option C: install standalone skills

Codex discovers user skills under `$HOME/.agents/skills` and repository skills under `.agents/skills`. It follows symlinked skill directories. The canonical Baseline skill tree is `plugins/baseline/skills/`. For a personal installation from an existing trusted clone:

```bash
mkdir -p "$HOME/.agents/skills"
for skill_dir in "/absolute/path/to/baseline/plugins/baseline/skills"/*/; do
  ln -s "$skill_dir" "$HOME/.agents/skills/$(basename "$skill_dir")"
done
```

Replace the example path with the absolute path to your clone and restart Codex. For one repository only, use that repository's `.agents/skills` instead of `$HOME/.agents/skills`. Update by pulling the source clone; remove by deleting only the Baseline symlinks you created. Do not symlink the whole `skills/` directory as one skill.

### Cursor, GitHub Copilot, and OpenCode

All three clients consume Agent Skills from `.agents/skills`. Use the standalone loop above for a personal user installation, or point the loop at a repository's `.agents/skills` for project scope. This keeps every link attached to one canonical skill directory and requires no Baseline process in the consumer project.

Cursor and GitHub Copilot also implement the open Agent Plugins package contract represented by `plugins/baseline/plugin.json`. That common manifest validates against Agent Plugins 1.0.0, but marketplace installation and update remain client-owned lifecycle features. The current checkout has no Cursor-specific manifest because Baseline ships no Cursor-only hooks, agents, rules, commands, or MCP servers. OpenCode needs no JavaScript or TypeScript plugin for static skills.

#### GitHub Copilot plugin marketplace

Copilot direct repository installation works today but is deprecated by the CLI. Register the repository marketplace and install through `plugin@marketplace` instead:

```bash
copilot plugin marketplace add woliveiras/baseline
copilot plugin install baseline@baseline
copilot skill list
```

Update the catalog before updating the plugin:

```bash
copilot plugin marketplace update baseline
copilot plugin update baseline
```

Reinstall or remove Baseline with:

```bash
copilot plugin uninstall baseline
copilot plugin install baseline@baseline

# Complete removal
copilot plugin uninstall baseline
copilot plugin marketplace remove baseline
```

The marketplace and plugin share the `baseline` identity. The committed catalog points to `./plugins/baseline`, and its catalog and plugin versions are synchronized with the other product manifests. The Copilot marketplace clean-room covers add, browse, install, exact discovery of 17 skills, update, uninstall, marketplace removal, and reinstall without login or model calls. Copilot's current `marketplace add OWNER/REPO` command follows the repository marketplace rather than exposing Codex's explicit immutable `--ref` option; release verification therefore checks main/tag parity and the installed version instead of claiming an untested ref pin.

Cursor remains at static format compatibility until its native loader and lifecycle can be exercised locally. Standalone `.agents/skills` remains the usable no-copy route in the meantime.

OpenCode 1.16.2 was locally verified to discover all 17 skills through a project `.agents/skills` link. Its catalog also contains host-provided skills, so discovery checks compare the Baseline subset rather than requiring an otherwise empty catalog.

### Claude Code

Claude Code requires its native `.claude-plugin/plugin.json`; it does not document the common Agent Plugins manifest as its package contract. Validate and load the trusted checkout directly without copying skills:

```bash
claude plugin validate /absolute/path/to/baseline/plugins/baseline
claude --plugin-dir /absolute/path/to/baseline/plugins/baseline
```

The first command performs no model call. `--plugin-dir` loads the local package for that Claude session; a persistent install/update/remove lifecycle requires a Claude marketplace and remains a separate publication concern.

### Pi

Pi can register the package directory directly. For one project:

```bash
cd /path/to/consumer-project
pi install /absolute/path/to/baseline/plugins/baseline -l --approve
pi list --approve
```

Remove and reinstall the same source with:

```bash
pi remove /absolute/path/to/baseline/plugins/baseline -l --approve
pi install /absolute/path/to/baseline/plugins/baseline -l --approve
```

The package stays loaded from the Baseline checkout. Its dependency-free `package.json` uses `pi.skills` to select only `skills/*/SKILL.md`, preventing `skills/catalog.md` from being mistaken for an eighteenth skill. The adapter is private and is not an npm publication.

### Cross-client invocation boundary

The canonical `SKILL.md` files deliberately use only the strict Agent Skills frontmatter shared by validators. Baseline does not invent a metadata field and call it portable enforcement. Today, Codex is the only packaged client in this repository whose explicit-only policy is mechanically mapped by an adapter. Cursor, Copilot, OpenCode, Pi, and Claude may advertise or select a workflow differently; invoke the six explicit-only workflows deliberately and do not interpret static discovery as evidence that routing, composition, authority, or model behavior has been validated.

### Discovery and invocation

- **Implicit invocation:** Codex may select an installed skill when the request matches its frontmatter description and `agents/openai.yaml` permits it. Ask for the outcome normally; no plugin name is required.
- **Explicit invocation:** use `$skill-name` in Codex CLI/IDE or choose the skill from the UI. Explicit-only Baseline workflows require this or an equally direct request.
- If many skills are installed, Codex may shorten or omit entries from its initial skill list because of the context budget. Use explicit invocation when you need a particular workflow deterministically.
- Codex clean-room validation covers plugin installation, discovery of all distributed skills, removal, and reinstallation without authentication or model calls. Client-specific evidence and limitations are stated in their installation sections. These checks establish packaging and discovery, not that a model follows a skill correctly.
- Codex CLI and Codex desktop retain their existing plugin route. Codex IDE supports standalone skills but not plugin installation. Recognition of `SKILL.md`, static schema validation, discovery, native lifecycle, invocation policy, and behavioral evaluation are distinct evidence levels; the sections above state which level was actually reached for each other client.

### Optional command rules

Copy [`templates/codex/baseline.rules`](templates/codex/baseline.rules) to `.codex/rules/baseline.rules` in a trusted project and restart Codex. The rules ask for human approval before push, destructive Git cleanup, release, publication, deploy, selected direct remote database and project mutations, infrastructure changes, and selected direct device mutations, and forbid a few literal broad-deletion forms.

Once installed, work normally: start from the authorized input, classify proportionally, refine only material ambiguity, run the smallest suitable verification fail-first, stay inside scope, synchronize durable knowledge when needed, and review the complete diff before any explicitly authorized Git operation. Each skill documents its own workflow in `SKILL.md`.

## Responsibility boundaries

Baseline separates command authority from workflow guidance:

- **Codex Rules** handle command-level safety through native, explicitly listed command prefixes.
- **`AGENTS.md` and skills** define the proportional, fail-first, scoped, reviewed workflow.
- **Tests and CI** provide executable evidence for product behavior.

Baseline does not install lifecycle hooks or require external dependencies in consumer projects. The workflow requirements are declarative rather than mechanically enforced. They are being validated across real repository tasks before any narrow gate is considered. See [the workflow boundary](docs/architecture/enforcement.md) for responsibilities and the observation protocol.

## Documentation

- **Use it:** this page, plus each skill's own `SKILL.md`.
- **Learn the vocabulary:** the [repository glossary](GLOSSARY.md) defines governing input, measurer, material ambiguity, fail-first, proportional review, task ownership, and `ENG-NOTE`.
- **Work on it:** the [documentation hub](docs/README.md) links the development guide, architecture, active decisions (ADRs), and the development-only evaluation harness.
- **Release it:** the [release guide](docs/releases.md) defines the single product version, protected automation, verification, and rollback.

## From Geremmyas to Baseline

Baseline succeeds Geremmyas by extracting the universal engineering minimum that should be available in every software project. Specialized and technology-specific capabilities live in [Storehouse](https://github.com/woliveiras/storehouse) and can be installed only where they are useful.

Baseline provides the foundation. Storehouse provides optional depth. Together they form the complete engineering suite without introducing a runtime dependency, synchronization layer, or permanent skill copies between the projects.

The workflows are informed by established engineering practice and compared for coverage with community engineering skills, including [Superpowers](https://github.com/obra/superpowers), [Spec Kit](https://github.com/github/spec-kit), and [Matt Pocock's skills](https://github.com/mattpocock/skills). No third-party skill text or procedure is copied. Recognized design references include John Ousterhout's *A Philosophy of Software Design* and Andrew Hunt and David Thomas's *The Pragmatic Programmer*.

Only fresh results from the current checkout can support a current evaluation claim.

## License

Baseline is released under the [MIT License](LICENSE).
