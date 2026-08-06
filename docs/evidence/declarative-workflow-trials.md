# Declarative workflow trial log

This log records the 10–20 real maintainer tasks required by
[SPEC-0001](../../specs/0001-declarative-workflow/spec.md) before Tuxedo
reconsiders lifecycle hooks. It is empirical evidence, not a task queue and not
a compliance score.

## Recording rules

- Add a row only after a real task finishes or the relevant failure occurs.
- Record observable behavior, not inferred intent.
- Do not count a hesitation corrected before production change as a failure.
- Note whether an existing test, Rule, approval, Git inspection, or human review
  already caught the problem.
- Preserve task confidentiality; use a stable local identifier and no prompts,
  credentials, personal paths, or proprietary source content.

## Failure categories

| ID | Category | Observable event |
| --- | --- | --- |
| `DWF-01` | Implementation before oracle | Production behavior changed before a suitable fail-first oracle was defined and run. |
| `DWF-02` | Scope expansion | Files or behavior outside the authorized task changed. |
| `DWF-03` | Implementation-aware weak test | A test was shaped to accept the implementation rather than prove the specification. |
| `DWF-04` | Missing review | Completion was claimed without the required reconstructed review phases. |
| `DWF-05` | Unrelated staged content | A commit candidate included changes not owned by the task. |
| `DWF-06` | Unauthorized additional work | A newly discovered task began without user authority. |

## Trials

No post-decision real tasks have been recorded yet.

| Trial | Date | Client | Task class | Result | Observed categories | Existing control that caught it | Evidence note |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Decision checkpoint

Do not aggregate before 10 completed real tasks. At 10–20 tasks, inspect
recurrence and impact per category. A hook proposal remains rejected unless a
failure recurs and has a narrow mechanical oracle, deterministic mutation
tests, no consumer-project mutation, and no installed runtime dependency.
