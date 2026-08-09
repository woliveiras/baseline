# Developing Tuxedo

This guide covers the repository layout, the toolchain, and how to develop and
test changes. The authoritative rules are in the
[engineering contract](../AGENTS.md); this guide is the practical companion.

## The product is the repository

Tuxedo is not a program with a build step. The repository contains the complete
product contract and repository evidence; its directly installable plugin
package is committed under `plugins/tuxedo/`. There is intentionally no CLI,
daemon, package manager, sync layer, telemetry, client generator, generated
distribution directory, or runtime dependency, and none should be added.

## Repository layout

- `plugins/tuxedo/` is the complete installed plugin package. It contains the
  manifest and the 17 distributed workflow skills, and nothing from the
  development-only toolchain.
- `skills/` is a repository compatibility symlink to
  `plugins/tuxedo/skills/`. It keeps existing repository and evaluation paths
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

- Python uses UV. Run scripts and tests with `uv run python ...`. Do not
  introduce a virtualenv or pip workflow.
- Node.js uses PNPM. Install with `pnpm install --frozen-lockfile` and run
  package commands with `pnpm run` or `pnpm exec`. Do not use npm or maintain a
  `package-lock.json`.

These are development toolchain conventions. Installed Tuxedo skills do not run
UV, Python, PNPM, or Node.js in consumer projects.

## How to develop

- Read the complete governing input and every applicable skill before changing behavior.
- Classify with `measurer`; refine only material ambiguity and add durable
  decision documentation only when timing and reversibility justify it.
- Keep each `SKILL.md` concise and imperative. Put optional depth one level down
  in `references/`.
- Keep portable workflow logic client-neutral. Codex invocation policy belongs
  in `agents/openai.yaml`.
- Add a deterministic test for every mechanical invariant you introduce.
- Classify work by the highest applicable proportionality tier (see the
  contract), never by line count.

## Local development installation

The supported consumer installation is documented in the [top-level README](../README.md):
Codex can fetch `woliveiras/tuxedo` as a GitHub marketplace and install
`tuxedo@tuxedo` without a Tuxedo checkout on the consumer machine. The
stable remote ref is the latest published `vX.Y.Z` tag. The initial release is
`v0.1.0`; `main` is a mutable development channel rather than a reproducible
consumer installation.

For people developing the repository itself, keep the local marketplace
flow so changes can be inspected directly from the checkout:

```bash
git clone https://github.com/woliveiras/tuxedo.git
cd tuxedo
codex plugin marketplace add "$(pwd)"
codex plugin add tuxedo@tuxedo
```

This local clone is a development convenience, not a prerequisite for users.
GitHub access for a private marketplace is configured through Git/SSH on the
machine and remains separate from Codex account authentication. Do not put
credentials in URLs or repository files.

## How to test

Local deterministic checks are fast and make no model calls:

```bash
uv run python -m unittest discover -s tests -v
uv run python evals/run.py --dry-run
```

`evals/run.py` never calls a model unless a user explicitly passes `--execute`. The
legacy runner compares baseline, minimal core, focal skill, broad configuration,
and distinct current-versus-proposed roots with seeded ordering and hidden
deterministic oracles. Architectural and intent-sensitive tasks stay
`needs-review` until the secondary rubric is applied; response keywords never
establish a pass.

Before completing a material change, run the checks listed in the
[engineering contract](../AGENTS.md): the official plugin validator, the
official skill validator for every skill, the unit tests, the eval dry-run,
shell syntax checks, `git diff --check`, and `git status --short`.

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
[`git-commit` skill](../plugins/tuxedo/skills/git-commit/SKILL.md) for the safe procedure.
