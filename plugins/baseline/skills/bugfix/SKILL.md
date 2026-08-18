---
name: bugfix
description: Diagnose and repair an existing software defect through bug report, reproduction, fail-first regression test, causal fix, and focused review. Use for incorrect or intermittent existing behavior; do not use for new features disguised as bugs.
---

# Bugfix

Follow `bug report -> reproduction -> fail-first regression test -> causal fix -> focused review`.

1. Read the bug report, governing input, domain invariants, recent changes, and current tests. Identify the expected behavior without treating current code as authority.
2. Reproduce the symptom before production edits at the fastest deterministic seam that still observes the defect. Respect task-specific execution constraints; do not work around them by installing tools or accessing outside the authorized workspace.
3. Load [feedback loops](./references/feedback-loops.md) only when ordinary reproduction is slow, difficult, or intermittent.
4. When ordinary reproduction or the first hypothesis remains insufficient, load [diagnostic escalation](./references/diagnostic-escalation.md).
5. Rank hypotheses, gather discriminating evidence, and add the smallest regression test. Confirm it fails for the reported behavior before the fix.
6. Apply the smallest causal repair, then rerun the regression, original reproduction, nearest suite, and applicable static checks. Remove temporary instrumentation.
7. Review the complete diff, causal fit, unrelated changes, fresh results, and residual risk.

For `S/M` bugs, create no specification, behavior/oracle matrix, evidence file, or review files. The regression test is the primary durable artifact; keep commands and limitations in the final response. Add `ENG-NOTE[bug][optional-id]` in the nearest test only when the historical reason is not evident.

For `L/XL` defects or material incidents, follow the documentation selected by `measurer`; a postmortem threshold depends on user impact, data loss, security impact, manual recovery, unavailability, or consequential detection failure, never line count.
