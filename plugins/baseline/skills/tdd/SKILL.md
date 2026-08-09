---
name: tdd
description: Implement approved behavior directly from a governing request, issue, contract, decision, or other sufficient input through a fail-first executable check. Use for clear testable behavior; do not use to invent requirements from current implementation or maximize test count.
---

# TDD

Understand the expected behavior from the governing input and write first the test that demonstrates its absence or incorrectness.

1. Select one behavior-sized slice and the most economical public seam: unit, integration, contract, end-to-end, static, or inspection.
2. Write the smallest check that distinguishes the expected result from a plausible wrong result. Prefer observable behavior over collaborator order or private structure.
3. Run it before production changes. Confirm fail-first for the expected behavioral reason; infrastructure and unrelated failures are not valid red signals.
4. Implement the smallest coherent behavior without weakening the check.
5. Run the focused check, nearby suite, and relevant static checks. Refactor only while behavior remains green.
6. Synchronize durable documentation when shipped behavior or a non-obvious constraint changed. Add an `ENG-NOTE` only when the reason cannot be inferred safely.

When a meaningful unit test is unavailable, use the smallest executable verification that observes the real boundary. Never change an assertion merely to accept the current implementation. Report commands, results, and limitations in the final response; do not create a persistent evidence file by default.
