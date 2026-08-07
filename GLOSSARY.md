# Tuxedo glossary

This glossary defines specialized terms used by Tuxedo's engineering contract and skills. Read a term according to this file unless a governing task or domain specification gives it a more specific meaning.

| Term | Operational meaning |
| --- | --- |
| Acceptance criterion | The obligation to satisfy |
| Invariant | The rule that must remain true |
| Oracle | The expected observable result |
| Verification or test | The mechanism that evaluates the oracle |
| Evidence | The record of what actually happened |
| Provenance | The origin and implementation exposure of each oracle |

## Identifier and evidence prefixes

Tuxedo prefixes stable identifiers with the artifact family that owns them.
The numeric suffix identifies one criterion, trial, finding, or work package
inside that family. Prefixes are scoped by their governing artifact, not
globally unique across every fixture and subsystem in the repository.

| Prefix | Expansion | Repository use |
| --- | --- | --- |
| `AC` | Acceptance Criterion | Generic example prefix for a uniquely identified obligation. A concrete specification may use a more specific family prefix instead. |
| `SPEC` | Specification | Governing specification directories and documents, such as `SPEC-0005`. |
| `GL` | Glossary | Acceptance criteria owned by `SPEC-0002`, the repository glossary contract. |
| `DW` | Declarative Workflow | Acceptance criteria owned by `SPEC-0001`, the declarative workflow decision. |
| `DWF` | Declarative Workflow Failure | Observable failure categories used by the real-task workflow experiment. |
| `DWT` | Declarative Workflow Trial | Individual real maintainer tasks observed during that experiment. |
| `SC` | Skill Catalog | Acceptance criteria owned by `SPEC-0003`, the skill catalog and composition contract. |
| `CP` | Clean-room Plugin package | Acceptance criteria owned by `SPEC-0004`, covering package boundaries, installation, discovery, and lifecycle. |
| `RM` | Remote Marketplace | Acceptance criteria owned by `SPEC-0005`, covering remote marketplace installation and Git transport. |
| `EV` | Evaluation | Umbrella prefix for evaluation-harness criteria represented in deterministic test names and evidence. |
| `EV-AGG` | Evaluation Aggregate | Exact aggregation and complete-suite verdict behavior. |
| `EV-ISO` | Evaluation Isolation | Isolation of workspaces, state, homes, and provider execution. |
| `EV-PRV` | Evaluation Privacy | Sanitization and prevention of durable secret or sensitive-output exposure. |
| `EV-RPT` | Evaluation Report | Persistence, validity, and failure semantics of evaluation reports. |
| `EV-SHD` | Evaluation Shard | Sharding, checkpoint survival, and full case coverage across shards. |
| `TUX-AUD` | Tuxedo Audit | Findings in the indexed internal repository audit. |
| `WP` | Work Package | Remediation groups defined by the internal audit. |

Read the complete identifier in context. For example, `RM-001` through
`RM-009` are Remote Marketplace criteria in `SPEC-0005`; `RM-01` in
command-Rules fixtures labels a test case for the shell command `rm` and does
not belong to that specification. The different digit widths help readers, but
the governing file remains authoritative.

## Documentation abbreviations

| Abbreviation | Expansion | Repository use |
| --- | --- | --- |
| `ADR` | Architecture Decision Record | A durable record of an architectural decision, its context, alternatives, and consequences. |
| `MADR` | Markdown Architectural Decision Records | The Markdown template and structure used for Tuxedo ADRs. |
| `RFC` | Request for Comments | A reviewable proposal for a material technical or process change before it becomes a settled decision. |
| `C4` | Context, Containers, Components, and Code | The architecture-model levels used by Tuxedo documentation templates; only the levels proportionate to the system are required. |
| `TDD` | Test-Driven Development | The fail-first implementation workflow: define the behavioral oracle, observe the relevant verification fail, implement, and refactor while preserving behavior. |
| `API` | Application Programming Interface | A programmatic contract exposed by a library, service, or tool. |
| `CI` | Continuous Integration | Automated repository checks run for proposed or integrated changes. |
| `CLI` | Command-Line Interface | A tool operated through terminal commands, such as Codex CLI. |
| `MCP` | Model Context Protocol | A protocol through which agent clients can use external tools and context providers. |
| `SDK` | Software Development Kit | A library and supporting contract used to integrate with a platform, such as the Codex SDK provider used by evaluations. |
| `SSH` | Secure Shell | The authenticated Git transport currently verified for fetching the private Tuxedo marketplace. |
| `HTTPS` | Hypertext Transfer Protocol Secure | The transport used by the `owner/repo` marketplace shorthand; private repositories require separately configured GitHub access. |

## Acceptance criterion

A uniquely identified, verifiable condition that must be true for a requirement to be satisfied. Tuxedo uses stable IDs such as `AC-001` so specifications, oracles, tests, evidence, and reviews can refer to the same obligation without relying on prose position.

## Behavior/oracle matrix

A table created before implementation that maps each acceptance criterion and relevant scenario to its invariant, observable oracle, provenance, planned verification, and resulting evidence. It exposes missing cases and weak or circular verification before code is written. “Behavior matrix” and “behavior and oracle matrix” refer to the same artifact in this repository.

## Evidence

The durable record of what was actually inspected or executed and what happened: for example, a command, exit status, test count, observed output, diff, or review finding. Evidence supports a claim only within the limits of what the observation measures. A passing command is evidence that a check passed; it is not by itself proof that the check represents the specification correctly.

## Fail-first

Defining an oracle, then executing the verification that evaluates it before the production implementation and observing that verification fail for the expected reason. This demonstrates that the verification can detect the missing or incorrect behavior. A failure caused by broken setup, syntax, or an unrelated defect is not valid fail-first evidence.

## Governing input

The user request, approved specification, task, plan, bug report, standard, or other authoritative artifact that defines intent and scope for the current work. A governing input must not be edited merely to make implementation or tests pass unless the user explicitly authorizes changing it.

## Invariant

A condition that must remain true across the scenario being evaluated, including relevant edge and failure paths. An invariant states the rule; an oracle states what can be observed to decide whether that rule holds.

## Oracle

The expected observable result used to decide whether behavior is correct for a scenario. Derive the oracle from the governing input or an independent authority, not from the new implementation wherever possible. A test is one mechanism that evaluates observed behavior against an oracle; static analysis, contract validation, inspection, and external conformance checks can also do so. The test code, the oracle, and the evidence produced by running the test are related but distinct.

Examples:

- Requirement: a discount is capped at 50. Oracle: `discount(80)` returns `50`. Unit test: call the function and compare the result with `50`.
- Requirement: installed skills contain no Python runtime. Oracle: the installed skill tree contains no `*.py`, `pyproject.toml`, or `uv.lock`. Verification: inspect the tree deterministically.
- Requirement: documentation contains no broken local links. Oracle: every local Markdown target resolves to an existing file or anchor. Verification: run a link checker.

## Provenance

Where an oracle came from and how exposed its author was to the implementation. Record provenance per oracle:

- `spec-derived`: follows an identifiable approved criterion or invariant.
- `independent`: derived without exposure to the new implementation.
- `implementation-aware`: fixed after its author saw the new implementation.
- `external`: comes from a protocol, standard, upstream contract, or verified reference system.
- `diagnostic-probe`: a temporary observation used to reproduce or localize a problem; it does not establish the final contract by itself.

Provenance helps estimate shared-error risk. It does not guarantee that an oracle is correct.

## Task-owned change

A file or hunk created or modified to satisfy the authorized current task. Pre-existing edits, adjacent cleanup, and newly discovered work are not task-owned unless the user explicitly adds them to scope. A task-owned commit contains only task-owned changes.

## Three-phase review

Three deliberately reconstructed reviews that reduce circular reasoning:

1. **Spec review:** evaluate intent, criteria, ambiguity, contradictions, scope, and risk without using tests or implementation as justification.
2. **Test review:** evaluate whether the matrix and oracles can distinguish correct from plausible wrong behavior without using the new implementation as justification.
3. **Code review:** evaluate the complete implementation and diff against the governing input, matrix, tests, and fresh evidence.

These phases may be performed by one reviewer for proportionate work, but their information boundaries and findings must remain distinct. Passing tests do not replace any phase.

## Verification

The mechanism used to evaluate an oracle and produce evidence. Depending on the behavior, the smallest suitable verification may be a unit, integration, contract, or end-to-end test, static analysis, deterministic inspection, or an external conformance check. Choose the mechanism after defining what must be observed; do not let the mechanism or implementation invent the expected result.
