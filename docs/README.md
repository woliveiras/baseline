# Tuxedo documentation

Documentation for people who want to work on Tuxedo itself: how the toolkit is
built, why it is built that way, how to develop and test it, and where the
evidence lives. If you only want to use Tuxedo with your agent, the
[top-level README](../README.md) is enough.

The documentation is organized by purpose so each page can be read for one
reason: guides say how to do something, architecture says how something works,
decisions say why something was chosen, and evidence records what was measured.

## Start here

- [Engineering contract](../AGENTS.md) is the operating agreement: the fidelity
  chain, proportionality tiers, authority and evidence rules, toolchain
  conventions, and the required checks. Read it before changing behavior.
- [Development guide](development.md) covers the repository layout, the
  toolchain, how to develop a change, and how to test it.

## How things work (architecture)

- [Workflow and command boundaries](architecture/enforcement.md): declarative
  workflow responsibilities, optional Codex Rules, and the empirical checkpoint
  before any lifecycle enforcement is reconsidered.
- [Evaluation architecture](architecture/evaluations.md): responsibility
  boundaries, oracle matrix, failure semantics, and suites.
- [Evaluation isolation and authentication](architecture/eval-isolation.md):
  the dedicated Codex home, authentication, `config.toml` parsing, and
  Promptfoo state isolation.

## Why decisions were made (ADRs)

- [ADR index](decisions/README.md)
- [ADR 0001: Promptfoo as evaluation orchestrator](decisions/0001-use-promptfoo-as-evaluation-orchestrator.md)

## Working with the evaluation harness

- [Using the evaluation harness](guides/using-the-eval-harness.md):
  prerequisites, authentication, suites, reading results, and cleanup.
- [Evaluation run evidence](evidence/eval-runs.md): dated results and open items
  from maintainer runs.
- [Declarative workflow trial log](evidence/declarative-workflow-trials.md):
  real-task observations used to decide whether any lifecycle gate is needed.

## Research and evidence

- [Engineering evidence map](research/evidence-map.md): empirical results,
  heuristics, product decisions, and their limits.

## Maintainer-internal notes

- [Skill-creator limitations](internal/skill-creator-limitations.md): a
  maintenance observation log, not product documentation.
