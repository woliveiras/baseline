---
name: tdd
description: Implement approved behavior through fail-first tests and traceable oracles. Use when a material testable change has stable criteria and a behavior-oracle matrix; do not use to invent requirements from existing implementation or to maximize test count.
---

# TDD

Preserve the chain from criterion to oracle to test to implementation.

1. Read the full spec and matrix. Select one criterion-sized slice and confirm its oracle provenance using [provenance](./references/provenance.md).
2. Write the smallest test at the most economical public seam: unit, integration, contract, or end-to-end. Prefer observable behavior over collaborator order or private structure.
3. Run it before production changes. Confirm it fails for the expected behavioral reason; infrastructure errors and unrelated failures are not red evidence.
4. Implement the smallest coherent behavior that satisfies the criterion without weakening the oracle.
5. Run the focused test, nearby suite, and relevant static checks. Add boundary cases where the matrix requires them, not to inflate counts.
6. Refactor only while behavior remains green. Re-run fresh evidence after refactoring.
7. Update the matrix with the test and evidence. If the spec, test, and code disagree, stop the slice and reconcile intent explicitly.

For medium and larger testable changes, require at least one `spec-derived`, `independent`, or `external` oracle. Treat tests written after viewing the new implementation as `implementation-aware` unless their oracle clearly comes from an independent source.

Never change an assertion merely to match current code. Do not claim semantic completeness from coverage or a passing suite.
