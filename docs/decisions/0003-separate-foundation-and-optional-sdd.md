---
status: accepted
date: 2026-08-09
decision-makers:
  - William Oliveira
supersedes: the product-workflow assumptions in ADR 0002; its no-runtime and command-authority decisions remain active
---

# Separate the engineering foundation from optional SDD

## Context and problem statement

Universal engineering practices and Specification-Driven Development have different ownership and installation boundaries. Requiring persistent specifications, behavior/oracle matrices, formal provenance, evidence files, and phased review for every material change would make an optional methodology part of the minimum cost of using Baseline.

Storehouse already distributes standalone, selectively installable specialized Agent Skills. It is the appropriate owner for optional SDD while Baseline remains the universal engineering foundation.

## Decision drivers

- Keep Baseline useful in any software repository without requiring one requirements methodology.
- Classify work by risk, boundaries, and reversibility rather than textual size.
- Preserve fail-first behavior, proportional review, durable knowledge, security, worktree ownership, and explicit authority.
- Let SDD users install its complete artifact chain selectively and independently.
- Avoid runtime dependencies, synchronization, duplicated TDD/review implementations, and repository imports.

## Decision outcome

Baseline provides this engineering flow:

`input -> measurer -> optional refine/decision docs -> fail-first check -> implementation -> durable docs -> proportional review -> explicitly authorized Git operation`

`measurer` returns an ephemeral JSON classification and creates no files. TDD and bugfix begin directly from sufficient governing input; review uses the complete diff and fresh results without requiring SDD artifacts.

Storehouse owns the optional `spec` skill and declarative `sdd` collection. That capability carries metadata-first discovery, stable acceptance criteria, behavior/oracle matrices, formal provenance, reconciliation, evidence, and phased SDD review. It can hand approved artifacts to installed TDD and review capabilities without depending on or copying them.

## Consequences

- Baseline keeps its universal cost small and proportional to risk.
- SDD remains complete, standalone, discoverable, and selectively installable.
- The two repositories compose through user-selected capabilities and artifacts, with no runtime coupling.
- Provider results from another catalog do not validate the current catalog; a fresh authorized run is required.
- The distributed inventory is derived from the current trees rather than fixed by this decision.

## Confirmation

Deterministic repository tests validate the product identity, distributed inventory, `measurer` contract, ambiguity routing, TDD/bugfix/review behavior, documentation timing, `ENG-NOTE`, optional Storehouse SDD distribution, absence of copied TDD/bugfix/verify skills, link integrity, and absence of a consumer runtime or cross-repository dependency. Provider/model evaluation requires separate authority.
