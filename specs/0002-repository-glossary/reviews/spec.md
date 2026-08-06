# SPEC-0002 spec review

Context reconstructed from the user's question, the current engineering contract, and Tuxedo's existing fidelity-chain vocabulary. Tests and the proposed glossary were excluded as justifications.

## Findings

The current contract explains when to create an oracle but assumes the reader already knows what an oracle is. The phrase “behavior/oracle matrix” compounds that ambiguity. A canonical root glossary is proportionate because the terms govern both installed workflows and repository maintenance, while a link near the first use keeps `AGENTS.md` concise.

The glossary must define operational distinctions, not merely provide circular synonyms. In particular, it must distinguish the expected observation (oracle), the mechanism that evaluates it (test or inspection), and the record produced by execution (evidence).

Because `AGENTS.md` is a public repository contract, the change is `medium` under Tuxedo's proportionality table even though it is easy to reverse. The acceptance criteria therefore require an explicit matrix, a spec-derived oracle, reconstructed review contexts, and complete evidence.

## Decision

Approved for fail-first test design with GL-001 through GL-005 unchanged.
