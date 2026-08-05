# Tuxedo documentation

This index separates three kinds of documentation so each one can be read for a
single purpose:

- **Guides** answer "how do I use this?" in the present imperative.
- **Architecture** answers "how does this work?" as timeless reference.
- **Decisions** answer "why was this chosen?" as dated ADRs.
- **Evidence** answers "what was measured, and when?" as an append-only log.

## Guides

- [Using the evaluation harness](guides/using-the-eval-harness.md) — prerequisites,
  authentication, suites, reading results, and cleanup.

## Architecture

- [Enforcement boundaries](architecture/enforcement.md) — Codex Rules and
  workflow hooks, and the limits of what the mechanical gates establish.
- [Evaluation architecture](architecture/evaluations.md) — responsibility
  boundaries, oracle matrix, failure semantics, and suites.
- [Evaluation isolation and authentication](architecture/eval-isolation.md) —
  dedicated Codex home, authentication, `config.toml` parsing, and Promptfoo
  state isolation.

## Decisions

- [ADR index](decisions/README.md)
- [ADR 0001: Promptfoo as evaluation orchestrator](decisions/0001-use-promptfoo-as-evaluation-orchestrator.md)

## Evidence

- [Evaluation run evidence](evidence/eval-runs.md) — dated results and open
  items from maintainer runs.

## Research

- [Engineering evidence map](research/evidence-map.md) — empirical results,
  heuristics, product decisions, and their limits.

## Maintainer-internal notes

- [`internal/`](internal/skill-creator-limitations.md) — maintenance observation
  logs that are not product documentation.
