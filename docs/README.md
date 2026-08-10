# Baseline documentation

Documentation for people who want to work on Baseline itself: how the toolkit is
built, why it is built that way, and how to develop and test it. If you only
want to use Baseline with your agent, the
[top-level README](../README.md) is enough.

The documentation is organized by purpose so each page can be read for one
reason: guides say how to do something, architecture says how something works,
and decisions say why something was chosen. Git is the default archive for
superseded material; the current tree contains only current documentation.

## Start here

- [Installation guide](guides/installation.md) covers the complete client
  installation, update, removal, and compatibility paths.
- [Engineering contract](../AGENTS.md) is the operating agreement: the
  proportional engineering flow, authority rules, toolchain conventions, and required
  checks. Read it before changing behavior.
- [Repository glossary](../GLOSSARY.md) defines governing input, measurer,
  material ambiguity, fail-first, task ownership, review depth, and `ENG-NOTE`.
- [Skill catalog contract](../plugins/baseline/skills/catalog.md) defines ownership, composition,
  precedence, stop conditions, and fallback for all 18 installed workflows.
- [Development guide](development.md) covers the repository layout, the
  toolchain, how to develop a change, and how to test it.
- [Release guide](releases.md) defines the shared version, protected Release
  Please flow, publication boundary, verification, and rollback policy.

## How things work (architecture)

- [Workflow and command boundaries](architecture/enforcement.md): declarative
  workflow responsibilities, optional Codex Rules, and the empirical checkpoint
  before any lifecycle enforcement is reconsidered.
- [Evaluation architecture](architecture/evaluations.md): responsibility
  boundaries, runner contract, failure semantics, and suites.
- [Evaluation isolation and authentication](architecture/eval-isolation.md):
  the dedicated Codex home, authentication, `config.toml` parsing, and
  Promptfoo state isolation.

## Why decisions were made (ADRs)

- [ADR index](decisions/README.md)
- [ADR 0001: Promptfoo as evaluation orchestrator](decisions/0001-use-promptfoo-as-evaluation-orchestrator.md)
- [ADR 0002: defer lifecycle hooks](decisions/0002-defer-lifecycle-hooks-pending-empirical-need.md)
- [ADR 0003: foundation and optional SDD ownership](decisions/0003-separate-foundation-and-optional-sdd.md)
- [ADR 0004: open multiclient package and thin adapters](decisions/0004-package-canonical-skills-with-open-and-native-adapters.md)

## Working with the evaluation harness

- [Using the evaluation harness](guides/using-the-eval-harness.md):
  prerequisites, authentication, suites, reading results, and cleanup.

## Repository-internal notes

- [Skill-creator limitations](internal/skill-creator-limitations.md): a
  current maintenance limitation, not product documentation.
