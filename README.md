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
dependencies with `pnpm install --frozen-lockfile`, then run:

```bash
pnpm run eval:login
pnpm run eval:auth:status
pnpm run eval:smoke
pnpm run eval:skills
pnpm run eval:security
pnpm run eval:full
```

`eval:login` is the one-time, explicit maintainer action that runs the official
`codex login` flow using the ChatGPT/Codex account. It stores and reuses that
session in `$HOME/.codex-tuxedo-evals` by default. Set
`TUXEDO_EVAL_CODEX_HOME` to an absolute directory outside this checkout to use
another dedicated home. The resolver rejects relative paths, the personal
`CODEX_HOME`, `$HOME/.codex`, and symlinks that resolve to either a personal
home or this checkout. The executable can be overridden with
`TUXEDO_EVAL_CODEX_PATH`.

Run `pnpm run eval:auth:status` to obtain operational evidence from
`codex login status`. It reports the dedicated home and gives the exact login
command when authentication is absent; it does not inspect or print
`auth.json`. The preflight accepts only the Codex CLI status label
`Logged in using ChatGPT`; API-key, agent-identity, ambiguous, and failed
statuses are rejected. A ChatGPT/Codex login is the canonical local
authentication path; neither `OPENAI_API_KEY` nor `CODEX_API_KEY` is required
or accepted as a silent substitute by the evaluation preflight.

The provider configurations intentionally omit a fixed `model`: the Codex CLI
selects a model supported by the authenticated ChatGPT/Codex account. Reports
record this as `codex-cli-default`; a future model pin requires a fresh
compatibility check against the selected authentication method.

The dedicated home may contain Codex operational state such as authentication,
minimal configuration, logs, history, sessions, state databases, and shell
snapshots. Codex-managed `skills/.system`,
`plugins/cache/openai-curated-remote`, and an empty
`plugins/.remote-plugin-install-staging` are also allowed because the CLI may
materialize them during normal operation. Personal or unknown skill/plugin
namespaces, `memories`, `rules`, instruction files, and MCP configuration are
rejected because they can change evaluated behavior. Tuxedo parses
`config.toml` fail-closed: `cli_auth_credentials_store` and Codex project
`trust_level` metadata are allowed; `hooks`, `profiles`, `model`,
`model_provider(s)`, MCP, instruction, policy, unknown settings, and other
project metadata are rejected. This small allowlist recognizes the current
CLI-managed surfaces; a future surface fails closed and the curated plugin
cache is trusted only as Codex-managed operational content. Tuxedo does not
validate the semantics of the allowed auth-store value, so keep the file
minimal; an unrecognized future status label also fails closed. Allowed managed
entries are required to be real directories/files rather than symlinks, so a
personal target cannot hide behind an allowed name. To switch accounts, set a
different `TUXEDO_EVAL_CODEX_HOME` and run `pnpm run eval:login`; to remove a
dedicated session, remove that home manually after confirming it is not needed.
No login secret enters this repository.

The official plugin and skill validators are discovered from the local Codex
installation or environment configuration. If they need PyYAML, keep it out of
the repository: create a temporary validator interpreter with UV and provide
it through `TUXEDO_VALIDATOR_PYTHON`:

```bash
validator_env_path="$(mktemp -d -t tuxedo-validators.XXXXXX)"
uv venv "$validator_env_path"
uv pip install --python "$validator_env_path/bin/python" PyYAML
TUXEDO_VALIDATOR_PYTHON="$validator_env_path/bin/python" pnpm run eval:full
```

The temporary environment is only for the official validators; PyYAML is not a
Tuxedo runtime or maintainer dependency.

`eval:full` is the explicit maintainer evaluation stack. It executes the
official validators, deterministic suites, 34 routing cases, 40 behavior
trials, and 12 security probes. It may make up to 86 provider calls and records
the measured duration and sanitized evidence in ignored
`evals/promptfoo/results/*.json`. It is not a pre-push hook, is not invoked by
installation, and is not a substitute for ordinary deterministic checks.
Existing reports are preserved, so the stack is repeatable. Run it when
empirical agent evidence is needed, then decide independently whether the
change is ready to push. `eval:redteam:generate`, `eval:redteam:review`, and
`eval:redteam:full` are also explicit maintainer actions.

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
account, CLI, provider, tasks, fixtures, and dependency versions. See
[the evaluation architecture](docs/architecture/evaluations.md) and
[ADR 0001](docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md)
for failure semantics, security limits, and authority boundaries.

## Provenance and influences

Tuxedo selectively adapts content from Geremmyas, which is MIT-licensed and owned by the same author. It preserves that project's spec-driven purpose without carrying over its CLI or distribution architecture.

The workflows were informed by established engineering practice, compared for coverage with community engineering skills including Matt Pocock's, and reviewed against recent empirical studies. No third-party skill text or procedure is copied. Rules are labeled as empirical results, engineering heuristics, product decisions, or community inspiration; citations do not imply that every rule is scientifically proven.

Recognized design references include John Ousterhout's *A Philosophy of Software Design* and Andrew Hunt and David Thomas's *The Pragmatic Programmer*. Their ideas are translated into operational checks such as interface comparison, information hiding, locality, reversibility, and evidence before broad change.

Research details and limitations are recorded in `docs/research/evidence-map.md`.
