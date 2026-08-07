# SPEC-0002 spec review

Context reconstructed from the user's question, the current engineering contract, and Tuxedo's existing fidelity-chain vocabulary. Tests and the proposed glossary were excluded as justifications.

## Findings

The current contract explains when to create an oracle but assumes the reader already knows what an oracle is. The phrase “behavior/oracle matrix” compounds that ambiguity. A canonical root glossary is proportionate because the terms govern both installed workflows and repository maintenance, while a link near the first use keeps `AGENTS.md` concise.

The glossary must define operational distinctions, not merely provide circular synonyms. In particular, it must distinguish the expected observation (oracle), the mechanism that evaluates it (test or inspection), and the record produced by execution (evidence).

Because `AGENTS.md` is a public repository contract, the change is `medium` under Tuxedo's proportionality table even though it is easy to reverse. The acceptance criteria therefore require an explicit matrix, a spec-derived oracle, reconstructed review contexts, and complete evidence.

## Decision

Approved for fail-first test design with GL-001 through GL-005 unchanged.

## Identifier-prefix amendment

### Spec

The request identifies a real contract ambiguity: `DWT`, `DWF`, `RM`, and the
other prefixes are meaningful only when their artifact family is known. A
canonical mapping belongs in the existing glossary rather than being repeated
across evidence files. GL-006 covers internal namespaces and contextual
ownership; GL-007 covers the small set of documentation abbreviations that
Tuxedo expects readers to understand operationally.

### Standards

The amendment excludes an exhaustive catalog of every command, product, or
fixture-only label. This keeps the glossary focused on repository contracts.

### Risk

Prefix strings are not globally unique. The specification must state that the
governing artifact is authoritative and explicitly explain the existing `RM`
collision instead of implying a repository-wide namespace registry.
