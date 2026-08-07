# SPEC-0002 test review

Context reconstructed from SPEC-0002, its behavior matrix, and the fail-first output. The new glossary text was excluded as a justification.

## Findings

The oracle must prove both discoverability and the minimum semantic distinctions that prevent a circular definition. Checking only for a `GLOSSARY.md` file or isolated keywords would allow empty, irrelevant, or inverted definitions to pass. The focused test therefore validates the canonical glossary and synthetic adversarial variants for every GL-003/GL-004 boundary: exact headings, obligation, invariant, oracle, verification, evidence, matrix mapping and fields, per-oracle provenance, valid fail-first chronology, governing-input authority, task ownership, and distinct review contexts.

The validation remains a deterministic contract check rather than a substitute for language review. Required semantic phrases can prevent named regressions, but they cannot prove that every reader will interpret the complete prose identically, so an isolated semantic review remains part of the evidence.

## Decision

Approved. The test failed before implementation because `GLOSSARY.md` was absent and passed after the canonical definitions and links were added.

## Identifier-prefix amendment

### Spec

The focused oracle covers every GL-006 namespace family named by the current
specification and every GL-007 documentation abbreviation. It also requires the
scope rule and both sides of the contextual `RM` example.

### Standards

Table rows are matched exactly so an expansion cannot silently drift. Prose is
checked after whitespace normalization so normal Markdown wrapping is not
mistaken for a semantic failure. The initial absent-heading failure is valid
fail-first evidence; the later line-wrap failure is recorded as test authoring,
not product behavior.

### Risk

The test intentionally does not infer a namespace from every uppercase token in
the repository. Such a scan would mix stable contracts with commands,
protocols, and disposable fixtures and would create false obligations.
