---
status: accepted
date: 2026-08-09
decision-makers:
  - William Oliveira
supersedes: the product-workflow assumptions in ADR 0002; its no-runtime and command-authority decisions remain active
---

# Adopt the proportional baseline and move SDD ownership

## Context and problem statement

Tuxedo originally distributed `spec` and required a persistent specification, behavior/oracle matrix, formal oracle provenance, evidence file, and separate specification/test/code review artifacts for material changes. That made an optional methodology part of the universal cost of every Tuxedo task and coupled baseline TDD, bug repair, documentation, and review to SDD artifacts.

The reusable SDD method is valuable, but it has a different ownership boundary from universal engineering practices. Storehouse already provides independent, selectively installable Agent Skills by project, while Tuxedo is the global horizontal baseline.

## Decision drivers

- Keep Tuxedo useful for any software repository without requiring one requirements methodology.
- Classify work by risk, boundaries, and reversibility rather than text size.
- Preserve fail-first behavior, proportional review, durable knowledge, security, worktree ownership, and explicit authority.
- Let SDD users install its complete artifact chain selectively and independently.
- Avoid runtime dependencies, synchronization, duplicated TDD/review implementations, or repository imports.

## Decision outcome

Tuxedo becomes a portable baseline for disciplined, proportional software engineering. Its baseline flow is:

`input -> measurer -> optional refine/decision docs -> fail-first check -> implementation -> durable docs -> proportional review -> explicitly authorized Git operation`

`measurer` replaces `spec` in the distributed Tuxedo inventory. It returns an ephemeral JSON classification and creates no files. TDD and bugfix begin directly from sufficient governing input; review uses the complete diff and fresh results without requiring SDD files.

Storehouse owns the optional `spec` skill and declarative `sdd` collection. That skill carries metadata-first discovery, stable acceptance criteria, behavior/oracle matrices, formal provenance, reconciliation, evidence, and phased SDD review. It can hand approved artifacts to installed TDD and review capabilities without depending on or copying them.

## Consequences

- Good: the Tuxedo base cost is smaller and proportional to risk.
- Good: SDD remains complete, standalone, discoverable, and selectively installable.
- Good: the two repositories have one-way artifact-level composition and no runtime coupling.
- Bad: provider results from another catalog do not validate the new catalog; a fresh authorized run is required.
- Neutral: Tuxedo still distributes 17 skills because `measurer` replaces `spec`; the number is derived from the actual trees, not guaranteed by the decision.
- Neutral: superseded SDD bundles, reviews, and evaluation logs live only in Git history after current knowledge is preserved here, in the baseline contract, tests, glossary, catalog, and Storehouse skill.

## Confirmation

Deterministic repository tests prove the product identity, distributed inventory, `measurer` JSON contract, ambiguity routing, baseline TDD/bugfix/review behavior, documentation timing, `ENG-NOTE`, optional Storehouse SDD distribution, absence of copied TDD/bugfix/verify skills, link integrity, and no installed runtime or cross-repository dependency. Provider/model evaluation requires separate future authority.
