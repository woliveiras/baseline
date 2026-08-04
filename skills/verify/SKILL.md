---
name: verify
description: Verify a software change through isolated spec, test, and code review plus fresh execution evidence. Use at review or completion boundaries for behavior changes; do not treat passing tests, coverage, or confidence as proof of spec fidelity.
---

# Verify

Apply [the three-phase review contract](./references/review-contract.md) and preserve context separation.

1. Classify blast radius and risk as `trivial`, `small`, `medium`, or `large/high-risk`, never by line count.
2. Run spec review with objective, full spec, criteria, domain, invariants, and reproduction only. Produce the behavior/oracle matrix without diff or new implementation.
3. Run test review with the approved spec, matrix, and tests. Exclude the new implementation. Check mapping, assertions, edges, failure paths, and provenance.
4. Run code review with spec, matrix, tests, diff, and fresh evidence. Report `Spec`, `Standards`, and `Risk` independently.
5. Execute the focused tests and nearest relevant suite; inspect exact outputs and timestamps. Check docs, migrations, error paths, compatibility, and cleanup.
6. Repair in-scope findings only when authorized, then rerun fresh evidence and review. Record unavailable checks as residual risk.

Trivial and small changes may use one isolated reviewer for all three passes. Medium changes require explicit context separation. Large/high-risk changes should use independent reviewers per phase when available. Lack of multiple agents does not waive separation: rebuild each pass from its allowed artifacts.

Return findings ordered by severity with tight locations and evidence. Say `no findings` explicitly when applicable, then list residual risks and commands actually executed.
