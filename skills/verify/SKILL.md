---
name: verify
description: Verify a software change through isolated spec, test, and code review plus fresh execution evidence. Use at review or completion boundaries for behavior changes; do not treat passing tests, coverage, or confidence as proof of spec fidelity.
---

# Verify

Apply [the three-phase review contract](./references/review-contract.md) and preserve context separation.

1. Classify with [the scope tiers](./references/scope-tiers.md), never by line count.
2. Run spec review with objective, full spec, criteria, domain, invariants, and reproduction only. Produce the behavior/oracle matrix without tests, diff, or new implementation. When receipts are used, start from [the spec-review asset](./assets/spec-review.json).
3. Run test review with the approved spec, matrix, fail-first record, and tests. Exclude the new implementation. Check mapping, assertions, edges, failure paths, provenance, and the recorded failure. Use [the test-review asset](./assets/test-review.json) when receipts are used.
4. Run code review with spec, matrix, tests, diff, structured test evidence, documentation decision, and fresh evidence. Report `Spec`, `Standards`, and `Risk` independently. Use [the code-review asset](./assets/code-review.json) when receipts are used.
5. Execute the focused tests and nearest relevant suite; inspect exact outputs and timestamps. Capture fail-first and passing evidence with [the evidence template](./assets/evidence-template.md) when the project lacks a stronger format.
6. Decide whether documentation is required. Update and hash the named artifacts, or record a concrete `not-required` rationale.
7. Repair in-scope findings only when authorized, then rerun fresh evidence and review. Mark review receipts `approved` only after actionable findings are reconciled. Record unavailable checks as residual risk.

Trivial and small changes may use one isolated reviewer for all three passes. Medium changes require explicit context separation. Large/high-risk changes should use independent reviewers per phase when available. Lack of multiple agents does not waive separation: rebuild each pass from its allowed artifacts. Hash receipts demonstrate current artifact relationships and declared exposure only; they do not prove semantic quality or actual reviewer independence.

Return findings ordered by severity with tight locations and evidence. Say `no findings` explicitly when applicable, then list residual risks and commands actually executed.
