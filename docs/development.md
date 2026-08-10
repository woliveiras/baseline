# Developing Baseline

This guide covers the repository layout, the toolchain, and how to develop and
test changes. The authoritative rules are in the
[engineering contract](../AGENTS.md); this guide is the practical companion.

## The product is the repository

Baseline is not a program with a build step. The repository contains the complete
product contract and repository evidence; its directly consumable multiclient
package is committed under `plugins/baseline/`. There is intentionally no CLI,
daemon, package manager, sync layer, telemetry, client generator, generated
distribution directory, or runtime dependency, and none should be added.

## Repository layout

- `plugins/baseline/` is the complete consumer package. Its open `plugin.json`,
  Codex and Claude manifest directories, and private Pi `package.json` are thin
  declarative adapters around the same 17 distributed workflow skills. It
  contains nothing from the development-only toolchain.
- `.agents/plugins/marketplace.json` and `.github/plugin/marketplace.json` are
  the Codex and Copilot repository catalogs. Both point to
  `plugins/baseline/`; neither contains or generates skill behavior.
- `skills/` is a repository compatibility symlink to
  `plugins/baseline/skills/`. It keeps existing repository and evaluation paths
  stable without creating a second skill tree or a package-generation step.
- Each distributed skill is a `SKILL.md` with optional `references/`, `assets/`,
  and `agents/` beside it.
- `templates/` holds the opt-in Codex Rules template.
- `docs/` holds project documentation.
- `evals/` holds the development-only evaluation harness (the deterministic
  runner plus the Promptfoo orchestration). It is not installed with the plugin.
- `tests/` holds the deterministic tests for the mechanical invariants.

`docs/`, `tests/`, and `evals/` are repository-only and are not part
of the installed plugin surface.

## Toolchain

- Python uses the non-package UV project in `pyproject.toml`. Run
  `uv sync --locked` after checkout and execute scripts and tests with
  `uv run --locked python ...`. `uv.lock` is the only dependency resolution
  source; do not introduce a manual virtualenv or pip workflow.
- Node.js uses PNPM. Install with `pnpm install --frozen-lockfile` and run
  package commands with `pnpm run` or `pnpm exec`. Do not use npm or maintain a
  `package-lock.json`.

These are development toolchain conventions. Installed Baseline skills do not run
UV, Python, PNPM, or Node.js in consumer projects.

The Python development group contains only PyYAML, used by the official
Codex plugin and skill validators to parse frontmatter. PyYAML is MIT-licensed,
version-pinned, lockfile-resolved, and absent from `plugins/baseline/`; it is not a
consumer runtime dependency.

## How to develop

- Read the complete governing input and every applicable skill before changing behavior.
- Classify with `measurer`; refine only material ambiguity and add durable
  decision documentation only when timing and reversibility justify it.
- Keep each `SKILL.md` concise and imperative. Put optional depth one level down
  in `references/`.
- Keep portable workflow logic client-neutral. Codex invocation policy belongs
  in `agents/openai.yaml`.
- Keep `plugins/baseline/skills/` as the only skill tree. Agent Plugins and
  native client descriptors may identify or select it, but must not copy,
  generate, patch, or wrap its behavior.
- Keep package descriptors data-only. Adding hooks, package scripts,
  dependencies, commands, agents, MCP servers, or client-specific behavior is
  a separate architecture and security decision.
- Add a deterministic test for every mechanical invariant you introduce.
- Classify work by the highest applicable proportionality tier (see the
  contract), never by line count.

## Local development installation

The consumer installation routes are documented in the [top-level README](../README.md).
Codex can fetch an immutable `vX.Y.Z` marketplace ref; Copilot registers the
repository's native marketplace and installs the same `baseline@baseline`
selector. `main` remains a mutable development channel rather than an immutable
release source.

For people developing the repository itself, keep the local marketplace
flow so changes can be inspected directly from the checkout:

```bash
git clone https://github.com/woliveiras/baseline.git
cd baseline
codex plugin marketplace add "$(pwd)"
codex plugin add baseline@baseline

copilot plugin marketplace add "$(pwd)"
copilot plugin install baseline@baseline
```

This local clone is a development convenience, not a prerequisite for users.
GitHub access for a private marketplace is configured through Git/SSH on the
machine and remains separate from Codex account authentication. Do not put
credentials in URLs or repository files.

## How to test

Local deterministic checks are fast and make no model calls:

```bash
uv run --locked python -m unittest discover -s tests -v
uv run --locked python evals/run.py --dry-run
```

`evals/run.py` never calls a model unless a user explicitly passes `--execute`. The
legacy runner compares control, minimal core, focal skill, broad configuration,
and distinct current-versus-proposed roots with seeded ordering and hidden
deterministic oracles. Architectural and intent-sensitive tasks stay
`needs-review` until the secondary rubric is applied; response keywords never
establish a pass.

Before completing a material change, run the checks listed in the
[engineering contract](../AGENTS.md): the official plugin validator, the
official skill validator for every skill, the unit tests, the eval dry-run,
shell syntax checks, `git diff --check`, and `git status --short`.

Multiclient package changes also validate `plugins/baseline/plugin.json`
against the exact Agent Plugins schema declared by its `$schema` field and run
the native validators already available without login or model calls. The
deterministic suite enforces the closed open-manifest fields, one canonical
skill tree, exact Pi allowlist, declarative adapter boundary, package contents,
identity, catalog source paths, and version parity. Where the CLI is available,
the Copilot clean-room exercises marketplace add/browse/remove and plugin
install/list/update/uninstall/reinstall. Client clean rooms use disposable
`HOME`, XDG, and client configuration directories; an unavailable client or a
lifecycle that requires a published Git source is recorded as an evidence gap,
never a pass.

Version increments, protected CI, Release Please, and the explicit publication
boundary are documented in the [release guide](releases.md). The root Node
package remains private and is never published to npm.

The empirical provider evaluations (Promptfoo plus Codex) are development-only
and require explicit user authority. They are described in
[the harness guide](guides/using-the-eval-harness.md) and
[the evaluation architecture](architecture/evaluations.md), and are never
implied by installation or a Git push.

## Committing

Commit coherent, task-owned slices locally with Conventional Commits
(`type(scope): subject`). Never infer authority for push, force-push, amend,
rebase, tag, release, publication, or deploy. See the
[`git-commit` skill](../plugins/baseline/skills/git-commit/SKILL.md) for the safe procedure.
