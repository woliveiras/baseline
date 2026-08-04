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
  -> spec / test / code review
```

Specs remain active artifacts. They may be corrected when evidence exposes ambiguity or contradiction, but code, tests, and documentation must then be reconciled explicitly. Passing tests are evidence, not proof that the intended behavior was captured.

## Hooks

The plugin bundles opt-in Codex lifecycle hooks that block a narrow set of mechanically identifiable dangerous commands, require exact-command authority receipts for protected operations, and validate artifact hashes when a project opts into completion receipts. Codex requires users to review and trust plugin hooks. Hooks do not inspect transcripts, collect prompts, send network requests, or decide semantic quality. See `docs/architecture/enforcement.md` for the exact boundary.

## Installation and development

The repository itself is the plugin. Validate it with the current `plugin-creator` validator before adding it to a local marketplace. Installation, publication, release, and global changes are intentionally not automated by this repository.

Local deterministic checks:

```bash
python3 -m unittest discover -s tests -v
python3 evals/run.py --dry-run
```

The evaluation harness is Codex-first and maintainer-only. It compares baseline, minimal core, focal skill, broad configuration, and current-versus-proposed variants. It never runs in CI and does not execute model calls unless a maintainer opts in.

## Provenance and influences

Tuxedo selectively adapts content from Geremmyas, which is MIT-licensed and owned by the same author. It preserves that project's spec-driven purpose without carrying over its CLI or distribution architecture.

The workflows were informed by established engineering practice, compared for coverage with community engineering skills including Matt Pocock's, and reviewed against recent empirical studies. No third-party skill text or procedure is copied. Rules are labeled as empirical results, engineering heuristics, product decisions, or community inspiration; citations do not imply that every rule is scientifically proven.

Recognized design references include John Ousterhout's *A Philosophy of Software Design* and Andrew Hunt and David Thomas's *The Pragmatic Programmer*. Their ideas are translated into operational checks such as interface comparison, information hiding, locality, reversibility, and evidence before broad change.

Research details and limitations are recorded in `docs/research/evidence-map.md`.
