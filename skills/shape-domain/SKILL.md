---
name: shape-domain
description: Continuously align domain language, invariants, scenarios, bounded contexts, integration translations, specs, tests, and code. Use when vocabulary or ownership boundaries affect behavior or design; do not use for cosmetic wording changes.
---

# Shape Domain

Treat modeling as a continuous activity across refine, spec, implementation, bugfix, and review.

1. Read the objective, full spec, code, tests, APIs, persistence, events, and the project's chosen vocabulary artifact. Respect `GLOSSARY.md`, `CONTEXT.md`, or another documented artifact; require none of them.
2. Collect domain nouns, actions, states, events, actors, constraints, and terms that are vague, contradictory, synonymous, or overloaded.
3. Exercise each material term with a normal scenario, edge/invalid scenario, invariant, and observable behavior.
4. Confront language with behavior and code: names, types, boundaries, validation, storage, events, tests, and user-facing copy. Do not let code silently define a contradictory domain meaning.
5. When multiple models, ownership policies, or vocabularies are materially distinct, load [context mapping](./references/context-mapping.md). A bounded context is not automatically a service, repository, deployment, or team.
6. Identify upstream/downstream relationships per operation, integration contracts, failure behavior, translation ownership, same terms with different meanings, and different terms for the same concept.
7. Update the smallest authorized vocabulary/spec surface when meaning stabilizes. Preserve public identifiers and stored values unless a migration is explicitly specified.
8. Carry stable terms and invariants into criteria, interfaces, test names, events, and final review findings.

Escalate only when competing meanings change product behavior, ownership, compatibility, or a hard-to-reverse boundary.
