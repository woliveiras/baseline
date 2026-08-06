# Tuxedo

Tuxedo is an installable, spec-driven software engineering toolkit for coding agents. It is distributed as a Codex plugin and portable Agent Skills, and it keeps intent, behavioral oracles, implementation, evidence, and review connected throughout a change.

If you want to *use* Tuxedo with your agent, this page is enough to get started. If you want to *work on* Tuxedo itself, go to the [documentation hub](docs/README.md).

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

Tuxedo v0.1 distributes 17 workflow skills that your agent loads on demand:

- Change workflow: `refine`, `spec`, `tdd`, `bugfix`, `verify`, `git-commit`, `ci-workflow`, `docs`.
- Design and architecture: `shape-domain`, `design-deep-modules`, `improve-architecture`, `decision-framework`.
- Deep work (explicitly invoked): `brainstorming`, `premortem`, `session-bridge`, `technical-research`.
- Safety: `security-review`.

Routine changes load only the smallest relevant workflow. `brainstorming`, `session-bridge`, and the architecture audits are explicit tools for deep work, not defaults.

## Using it with Codex

The repository itself is the plugin. There is intentionally no separate installer, package manager, or sync layer.

1. **Add the skills.** Validate the repository with the current `plugin-creator` validator, then add it to a local Codex marketplace so the skills load in your agent. Publication and release are intentionally not automated here.
2. **Opt in to Codex Rules (optional).** Copy [`templates/codex/tuxedo.rules`](templates/codex/tuxedo.rules) to `.codex/rules/tuxedo.rules` in a trusted project and restart Codex. The rules ask for human approval before push, destructive Git cleanup, release, publication, deploy, and infrastructure mutations, and forbid a few literal broad-deletion forms.
3. **Follow the declarative workflow.** Start from the authorized task, define the appropriate fail-first oracle before production implementation, stay inside scope, review spec/tests/code separately, and inspect the staged candidate before a local commit.

Once the skills are available, work normally: your agent picks the smallest relevant workflow, and the deep-work skills stay explicit. Each skill documents its own steps in its `SKILL.md`.

## Responsibility boundaries

Tuxedo separates command authority from workflow guidance:

- **Codex Rules** handle command-level safety through native, explicitly listed command prefixes.
- **`AGENTS.md` and skills** define the strict spec-first, oracle-first, scoped, reviewed workflow.
- **Tests and CI** provide executable evidence for product behavior.

Tuxedo does not install lifecycle hooks or require UV or Python in consumer projects. The workflow requirements are declarative rather than mechanically enforced. The maintainer is validating them across real tasks before deciding whether any narrow gate is necessary. See [the workflow boundary](docs/architecture/enforcement.md) for responsibilities and the observation protocol.

## Documentation

- **Use it:** this page, plus each skill's own `SKILL.md`.
- **Work on it:** the [documentation hub](docs/README.md) links the development guide, architecture, decisions (ADRs), research evidence, and the maintainer evaluation harness.

## From Geremmyas to Tuxedo

Tuxedo is the successor to Geremmyas, an earlier project that explored spec-driven development with coding agents by combining specifications, tests, reviews, workflow guidance, and executable guardrails. Tuxedo carries that purpose forward as a portable, evidence-driven toolkit and drops the CLI and distribution machinery. It selectively adapts content from Geremmyas (MIT-licensed, same author).

The project is named after Geremmyas, my tuxedo cat and the namesake of the toolkit that preceded it.

## Provenance and influences

The workflows were informed by established engineering practice, compared for coverage with community engineering skills (including Matt Pocock's), and reviewed against recent empirical studies. No third-party skill text or procedure is copied. Recognized design references include John Ousterhout's *A Philosophy of Software Design* and Andrew Hunt and David Thomas's *The Pragmatic Programmer*, translated into operational checks such as interface comparison, information hiding, locality, reversibility, and evidence before broad change.

Rules are labeled as empirical results, engineering heuristics, product decisions, or community inspiration; a citation does not imply that a rule is scientifically proven. Details and limitations live in [the evidence map](docs/research/evidence-map.md).

## License

Tuxedo is released under the [MIT License](LICENSE).
