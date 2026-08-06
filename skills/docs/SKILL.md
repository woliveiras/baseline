---
name: docs
description: Maintain the smallest durable project documentation surface and reconcile it with active specs and shipped behavior. Use for project docs, domain vocabulary, accepted architecture decisions, or proposals; do not use to author feature specs or unrelated prose.
---

# Docs

Route the request without loading every reference.

| Need | Load |
| --- | --- |
| API, architecture, setup, configuration, onboarding | [project documentation](./references/project-docs.md) |
| Vocabulary, conflicting terms, bounded contexts | Use `shape-domain`; update the project's chosen glossary/context artifact |
| Accepted hard-to-reverse decision | [decision record](./references/decision-record.md) |
| Unresolved material proposal | [proposal](./references/proposal.md) |
| Incident learning and corrective actions | [postmortem guidance](./references/postmortem.md) |

1. Read the full governing spec, implemented behavior, existing docs, and repository convention.
2. Select one mode by default and update the smallest relevant surface.
3. Preserve criterion IDs and link durable claims to the spec or current code. If docs, tests, code, and spec disagree, expose and reconcile the conflict rather than documenting the implementation as truth.
4. Create a decision record only for an accepted, surprising, hard-to-reverse trade-off. Keep unresolved choices in a proposal or spec.
5. Validate filenames, indexes, local links, commands, examples, and version-sensitive claims.

Report the mode, inspected evidence, updated claims, and checks. Match the repository's voice and avoid unsupported significance claims.

When the repository has no stronger template, copy the matching asset rather than recreating its structure:

- [MADR decision record](./assets/adr-madr-template.md)
- [C4 project architecture](./assets/project-c4-template.md)
- [RFC proposal](./assets/rfc-template.md)
- [blameless postmortem](./assets/postmortem-template.md)
