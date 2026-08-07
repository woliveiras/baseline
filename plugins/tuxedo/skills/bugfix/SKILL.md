---
name: bugfix
description: Diagnose and repair a software defect with a fail-first reproduction, ranked hypotheses, a regression oracle, and fresh evidence. Use for incorrect existing behavior or intermittent failures; do not use for new features disguised as bugs.
---

# Bugfix

1. Read the governing spec, bug report, domain invariants, recent changes, and current tests. Identify the expected behavior and its criterion or external source.
2. Reproduce the symptom before production edits. Prefer the fastest deterministic seam that still observes the correct failure.
   Task-specific execution constraints remain authoritative: if they prohibit a normal diagnostic or check, do not work around the restriction by installing tools, relocating caches, or accessing outside the authorized workspace. Use permitted evidence and report the limitation.
3. If ordinary reproduction is difficult, slow, or intermittent, load [feedback loops](./references/feedback-loops.md); otherwise do not load it.
4. Rank hypotheses and gather discriminating evidence. A diagnostic probe may localize the cause but is not automatically the regression oracle.
5. Add or identify a regression test with provenance. Run it fail-first, confirm the failure represents the reported behavior rather than harness damage, and record the test-tree state, command, and observed failure before the production fix.
6. Apply the smallest causal fix. Do not broaden behavior or weaken the spec to fit the current implementation.
7. Re-run the regression, original reproduction, nearest suite, and applicable static checks. Remove temporary instrumentation.
8. Record actual cause, criterion, test provenance, commands, outcomes, and residual evidence. Reconcile the spec if the report exposed ambiguity or an invalid premise.

Keep working inside the authorized scope. Stop only for a material objective contradiction, a withheld authority boundary, or an evidence blocker that cannot be reduced safely.
