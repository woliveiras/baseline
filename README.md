# Tuxedo

Tuxedo is an installable, spec-driven software engineering toolkit distributed as a Codex plugin and portable Agent Skills. It keeps intent, behavioral oracles, implementation, evidence, and review connected throughout a change.

## From Geremmyas to Tuxedo

Tuxedo is a successor to Geremmyas, a previous project that explored spec-driven development with coding agents.

Geremmyas began as an attempt to reinforce spec-driven development while working with coding agents. It combined specifications, tests, reviews, workflow guidance, and executable guardrails to reduce drift between intended and implemented behavior.

Tuxedo carries that purpose forward as a portable, evidence-driven engineering toolkit. It treats specifications as active engineering artifacts: they guide implementation, provide the source for test oracles, and remain part of verification and review.

The project is named after Geremmyas, my tuxedo cat and the namesake of the toolkit that preceded it.

## Included capabilities

The v0.1 plugin distributes `refine`, `brainstorming`, `spec`, `tdd`, `bugfix`, `verify`, `docs`, `git-commit`, `ci-workflow`, `shape-domain`, `design-deep-modules`, `improve-architecture`, `decision-framework`, `premortem`, `session-bridge`, `technical-research`, and `security-review`.

`brainstorming`, `session-bridge`, and architecture audit workflows are explicit tools for deep work. Routine changes should load only the smallest relevant workflow.

## Fidelity model

```text
spec
  -> behavior and oracle matrix
  -> tests
  -> implementation
  -> evidence
  -> isolated spec / test / code review
```

Specs remain active artifacts. They may be corrected when evidence exposes ambiguity or contradiction, but code, tests, and documentation must then be reconciled explicitly. Passing tests are evidence, not proof that the intended behavior was captured.

## Executable reinforcement

Tuxedo separates command authority from workflow integrity:

- `templates/codex/tuxedo.rules` uses native Codex Rules for explicitly listed, standard direct command prefixes. The template forbids a few literal broad-deletion forms and requests human approval for listed direct forms of push, destructive Git cleanup, release, publication, deployment, and infrastructure mutations.
- plugin hooks reinforce Tuxedo's spec-driven workflow at direct commits and turn completion. An opt-in version 2 receipt binds the current spec, behavior matrix, every file in configured test and implementation scopes, fail-first and passing evidence, the documentation decision, and the three review phases through SHA-256 hashes.

Rules and hooks do not inspect transcripts, collect prompts, send network requests, or decide semantic quality. Exact prefix rules do not cover executable paths, wrappers, or global options inserted before a subcommand. Receipt hashes make stale or incomplete relationships detectable; they cannot prove wall-clock TDD order, oracle quality, or actual reviewer independence. See `docs/architecture/enforcement.md` for the exact boundary and setup.

## Installation and development

The repository itself is the plugin. Validate it with the current `plugin-creator` validator before adding it to a local marketplace. Installation, publication, release, and global changes are intentionally not automated by this repository. Codex Rules are project opt-in: copy the template to `.codex/rules/tuxedo.rules` in a trusted project and restart Codex.

Local deterministic checks:

```bash
uv run python -m unittest discover -s tests -v
uv run python evals/run.py --dry-run
```

The legacy deterministic runner is Codex-first and maintainer-only. It compares baseline, minimal core, focal skill, broad configuration, and distinct current-versus-proposed roots with seeded ordering and repeated trials. Executable fixture tasks use deterministic hidden oracles. Architectural and intent-sensitive tasks remain `needs-review` until the secondary rubric is applied; response keywords never establish a pass. `evals/run.py` never executes model calls unless a maintainer passes `--execute`; the separate Promptfoo commands below intentionally do.

## Maintainer-only Promptfoo evaluations

Promptfoo and the Codex SDK are development-only dependencies. They are not
part of the plugin or installed skills. The provider runs in fresh disposable
workspaces with `network_access_enabled: false`, no Promptfoo sharing, and a
dedicated Codex home outside the checkout. The runner never copies personal
Codex authentication or content and never uses the personal `~/.codex` home.

Use Node `>=22.22.0`, UV for Python, and PNPM for Node. Install Node
dependencies with `pnpm install --frozen-lockfile`, then follow
[the harness guide](docs/guides/using-the-eval-harness.md):

```bash
pnpm run eval:login
pnpm run eval:auth:status
pnpm run eval:smoke
pnpm run eval:skills
pnpm run eval:security
pnpm run eval:full
```

`eval:login` authenticates a dedicated Codex home once; `eval:auth:status`
verifies it. The harness runs the provider in fresh disposable workspaces and
isolates the dedicated Codex home, authentication, `config.toml` parsing, and
Promptfoo state as described in
[the isolation model](docs/architecture/eval-isolation.md). Full step-by-step
usage, including the optional `TUXEDO_VALIDATOR_PYTHON` interpreter for the
official validators, is in
[the harness guide](docs/guides/using-the-eval-harness.md).

`eval:full` is the explicit maintainer evaluation stack. It executes the
official validators, deterministic suites, 34 routing cases, 40 behavior
trials, and 12 security probes, and may make up to 86 provider calls. It is not
a pre-push hook, is not invoked by installation, and a passing result does not
itself authorize a push. Existing sanitized reports under
`evals/promptfoo/results/` are preserved, so the stack is repeatable. Routing is
split into two shards and behavior into four, with at most two active at once,
which changes elapsed time but not the 86-call coverage.
`eval:redteam:generate`, `eval:redteam:review`, and `eval:redteam:full` are
separate explicit maintainer actions.

The suites test different properties of the skills:

- `eval:skills` runs positive and negative routing cases for every distributed
  skill. A positive case asks for a named workflow and checks structured
  provider metadata for an observed skill-file read; a negative case checks
  that an unrelated skill was not observed. This is evidence of routing and
  invocation, not proof that every instruction in a skill was obeyed.
- Behavior trials give the agent a legitimate task in a fresh workspace across
  baseline/core/focal/broad/current conditions. Hidden deterministic oracles
  verify required file changes, protected paths, no-op rejection, regression
  behavior, and completed turns; a response saying “done” is insufficient.
- Security probes pair a distinct adversarial fixture stimulus with the same
  legitimate `src/app.py` oracle. Assertions inspect workspace snapshots,
  protected hashes, outside sentinels, canary exposure, and structured command
  or file events when the provider exposes them. They do not certify universal
  security or silent reads when trajectory evidence is unavailable.

`eval:smoke` is the small provider sanity check. `eval:full` is the broadest
local empirical stack, but its result remains scoped to the recorded Codex
account, CLI, provider, tasks, fixtures, and dependency versions. Measured run
outcomes and open items are recorded in
[the run log](docs/evidence/eval-runs.md). See
[the evaluation architecture](docs/architecture/evaluations.md) and
[ADR 0001](docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md)
for failure semantics, security limits, and authority boundaries.

## Provenance and influences

Tuxedo selectively adapts content from Geremmyas, which is MIT-licensed and owned by the same author. It preserves that project's spec-driven purpose without carrying over its CLI or distribution architecture.

The workflows were informed by established engineering practice, compared for coverage with community engineering skills including Matt Pocock's, and reviewed against recent empirical studies. No third-party skill text or procedure is copied. Rules are labeled as empirical results, engineering heuristics, product decisions, or community inspiration; citations do not imply that every rule is scientifically proven.

Recognized design references include John Ousterhout's *A Philosophy of Software Design* and Andrew Hunt and David Thomas's *The Pragmatic Programmer*. Their ideas are translated into operational checks such as interface comparison, information hiding, locality, reversibility, and evidence before broad change.

Research details and limitations are recorded in `docs/research/evidence-map.md`.
