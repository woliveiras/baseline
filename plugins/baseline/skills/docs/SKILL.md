---
name: docs
description: Maintain the smallest durable software documentation surface for shipped behavior, architecture, decisions, operations, incidents, and non-obvious code reasons. Use when knowledge must outlive the current task; do not create documentation for routine reversible work or narrate self-explanatory code.
---

# Docs

Route to one smallest durable surface by default.

| Need and timing | Load |
| --- | --- |
| Open material decision before implementation | [RFC guidance](./references/proposal.md) |
| Accepted hard-to-reverse decision | [ADR guidance](./references/decision-record.md) |
| Stable boundaries or shipped API/operations | [project documentation](./references/project-docs.md) |
| Incident learning after threshold | [postmortem guidance](./references/postmortem.md) |
| Non-obvious local reason in code or test | [code comments](./references/code-comments.md) |
| Vocabulary or bounded contexts | Use `shape-domain` and the project's chosen vocabulary surface |

Read the governing input, implemented behavior, existing docs, and repository convention. Do not create an RFC after implementation has made the choice effectively irreversible; record the accepted decision as an ADR when its threshold is met. Do not create an ADR for routine reversible work. Use C4 or the repository's architecture notation only when boundaries and responsibilities have stabilized. Synchronize API and operations documentation with shipped behavior.

Use Git as the default historical archive. Remove a document from the current tree when it no longer guides a current decision, operation, contract, risk, or behavior and Git can reconstruct it completely. Do not create `archive/` directories for superseded snapshots, reviews, evidence logs, or completed task bundles.

Validate filenames, indexes, local links, commands, examples, and version-sensitive claims. Report the selected mode, updated claims, checks, and limitations.

When no stronger template exists, use the matching bundled asset:

- [MADR decision record](./assets/adr-madr-template.md)
- [C4 project architecture](./assets/project-c4-template.md)
- [RFC proposal](./assets/rfc-template.md)
- [blameless postmortem](./assets/postmortem-template.md)
