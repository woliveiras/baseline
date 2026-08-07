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

| Trial | Date | Client | Task class | Result | Observed categories | Existing control that caught it | Evidence note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `DWT-001` | 2026-08-07 | Codex desktop | `medium` | pass | none | `AGENTS.md` declarative flow, composed Tuxedo workflows, deterministic tests, and Git inspection | Commit `47148ab`; spec and matrix preceded implementation, the six-case fail-first run detected both target defects, three-phase review completed, and the task-owned commit excluded local contamination |

### DWT-001 observations

- Codex selected `spec`, `tdd`, and `verify` without the request naming those
  workflows. The task proceeded through spec, matrix, fail-first tests,
  implementation, evidence, and three reconstructed review phases.
- The request explicitly required a local commit. Codex did not announce the
  explicit-only `git-commit` workflow, but it followed the equivalent
  task-owned staging and Conventional Commit requirements already present in
  `AGENTS.md`. This is a composition observation, not a `DWF-05` failure;
  retain it for recurrence analysis rather than treating skill invocation as a
  compliance score.
- An ignored `plugins/tuxedo/.DS_Store` caused the installed-package boundary
  tests to reject the contaminated checkout. Codex preserved it outside the
  package only while validating the tracked candidate, restored it unchanged,
  excluded it from the commit, and reported both the 87/89 contaminated result
  and the 89/89 tracked-candidate result.
- The task completed in approximately 10 minutes 24 seconds. No push or
  additional remediation was attempted.

## Decision checkpoint

Do not aggregate before 10 completed real tasks. At 10–20 tasks, inspect
recurrence and impact per category. A hook proposal remains rejected unless a
failure recurs and has a narrow mechanical oracle, deterministic mutation
tests, no consumer-project mutation, and no installed runtime dependency.
