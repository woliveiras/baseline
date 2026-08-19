---
name: verify
description: Review a software change proportionally against its governing input, expected behavior, tests, complete diff, relevant risks, fresh results, unrelated changes, and limitations. Use at review or completion boundaries; do not also invoke for a request limited to security risks, which security-review owns.
---

# Verify

Use the review depth selected by `measurer`; load [review depth](./references/review-depth.md) when the classification or required validation is uncertain.
For `expanded` or `independent` review, or when behavioral correctness and engineering risk may diverge, load [review lenses](./references/review-lenses.md).

1. Read the governing input and state the expected behavior and explicit exclusions.
2. Inspect tests and the fail-first observation where available. Check assertion strength, boundary and failure cases, and whether a plausible wrong implementation could pass.
3. Inspect the complete diff and worktree state. Check correctness, readability, architecture, compatibility, security, privacy, data loss, concurrency, rollback, documentation, `ENG-NOTE` reasons, and unrelated changes as relevant.
4. Run focused checks and the nearest relevant suite when authorized. Respect task-specific execution constraints; do not work around them by installing tools or accessing outside the authorized workspace. Treat unavailable or stale checks as limitations, not passing evidence.
5. Repair in-scope findings only when authorized, rerun fresh checks, and review the resulting complete diff.

Do not create review files or a persistent evidence artifact by default. Return findings ordered by severity with tight locations, followed by fresh commands/results, residual risk, and limitations. Say `no findings` explicitly when applicable.
