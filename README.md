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
python3 -m unittest discover -s tests -v
python3 evals/run.py --dry-run
```

The evaluation harness is Codex-first and maintainer-only. It compares baseline, minimal core, focal skill, broad configuration, and distinct current-versus-proposed roots with seeded ordering and repeated trials. Executable fixture tasks use deterministic hidden oracles. Architectural and intent-sensitive tasks remain `needs-review` until the secondary rubric is applied; response keywords never establish a pass. The runner never executes model calls unless a maintainer passes `--execute`.

## Maintainer-only Promptfoo evaluations

Promptfoo and the Codex SDK are development-only dependencies. They are not
part of the plugin or installed skills. The provider runs in fresh disposable
workspaces with `network_access_enabled: false`, no Promptfoo sharing, and a
dedicated authenticated `TUXEDO_EVAL_CODEX_HOME` outside the checkout. The
runner never copies personal Codex authentication or content.

Install with Node `>=22.22.0` and run `npm ci`. Then use:

```bash
npm run eval:smoke
npm run eval:skills
npm run eval:security
npm run verify:push
```

`verify:push` executes the official validators, deterministic suites, 34
routing cases, 40 behavior trials, and 12 security probes. It is expected to
make 86 provider calls and records the measured duration and sanitized evidence
in ignored `evals/promptfoo/results/*.json`. Existing reports are preserved, so
the gate is repeatable. `eval:redteam:generate`, `eval:redteam:review`, and
`eval:redteam:full` are explicit maintainer actions; full red teaming is not a
pre-push check. See [the evaluation architecture](docs/architecture/evaluations.md)
and [ADR 0001](docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md)
for failure semantics, security limits, and authority boundaries.

## Provenance and influences

Tuxedo selectively adapts content from Geremmyas, which is MIT-licensed and owned by the same author. It preserves that project's spec-driven purpose without carrying over its CLI or distribution architecture.

The workflows were informed by established engineering practice, compared for coverage with community engineering skills including Matt Pocock's, and reviewed against recent empirical studies. No third-party skill text or procedure is copied. Rules are labeled as empirical results, engineering heuristics, product decisions, or community inspiration; citations do not imply that every rule is scientifically proven.

Recognized design references include John Ousterhout's *A Philosophy of Software Design* and Andrew Hunt and David Thomas's *The Pragmatic Programmer*. Their ideas are translated into operational checks such as interface comparison, information hiding, locality, reversibility, and evidence before broad change.

Research details and limitations are recorded in `docs/research/evidence-map.md`.
