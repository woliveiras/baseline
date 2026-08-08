# Declarative workflow trial log

This log records the 10–20 real repository tasks required by
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
| `DWT-002` | 2026-08-07 | Codex desktop | analysis-only | pass | none | Explicit no-write authority, official-source routing, and final Git inspection | Official Codex and GitHub evidence supported a remote-marketplace recommendation; no tests, installation, artifact, commit, push, or release was attempted |
| `DWT-003` | 2026-08-07 | Codex desktop | `medium` | pass | none | `AGENTS.md` fidelity chain, composed Tuxedo workflows, deterministic documentation tests, three-phase review, and staged-diff inspection | Commit `c092f1f`; SPEC-0005 and its matrix preceded a valid fail-first oracle, the oracle was strengthened during review, 89/89 applicable deterministic tests passed, and the task-owned commit excluded concurrent and ignored state |
| `DWT-004` | 2026-08-07 | Codex desktop | analysis-only | pass | none | Explicit no-write authority, security/decision workflows, primary advisory sources, local audit, and final Git inspection | Reproduced 14 development-only advisories and separated lockfile presence from configured-provider reachability; the first turn completed with a clean worktree and no install, provider, artifact, commit, or push |
| `DWT-005` | 2026-08-07 | Codex desktop | `large/high-risk` | fail | `DWF-04` | Human review of the completed task against the `AGENTS.md` fidelity chain | After explicit authority to update dependencies, the agent changed three task-owned package files and ran broad checks, but claimed completion without a governing spec/matrix, durable evidence, or reconstructed spec/test/code reviews; no commit or push occurred |

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

### DWT-002 observations

- Codex selected the OpenAI documentation workflow, rejected a helper that
  would have written a local cache, and used official Codex, OpenAI repository,
  and GitHub sources plus read-only Tuxedo inspection.
- Codex did not announce the explicit-only `technical-research` workflow or the
  applicable `decision-framework` workflow, despite a direct request to
  investigate, compare, and recommend. The answer still recorded evidence,
  alternatives, limitations, authentication boundaries, and a recommendation.
  This is a composition observation, not a DWF failure.
- The task reported the mutable `main` limitation, absence of Git tags, and the
  distinction between Codex authentication and GitHub credentials. It did not
  publish a tag or broaden the task into documentation or installation work.
- Concurrent repository work changed Rules, documentation, and tests during
  the observation window. The task stream contained no file change, and the
  concurrent diff was unrelated to marketplace research, so no write is
  attributed to DWT-002.
- The task completed in approximately 7 minutes 21 seconds.

### DWT-003 observations

- Codex selected `spec`, `tdd`, `docs`, and `verify` without the request naming
  those workflows, then explicitly selected `git-commit` before staging.
- SPEC-0005 and its eight-criterion behavior matrix preceded the fail-first
  documentation test. The test failed because the remote marketplace sequence
  was absent before the README and development guide were changed.
- During the test review, Codex found that the sparse-checkout oracle only
  checked two independent markers and strengthened it to require both paths in
  the same command. Temporary test-authoring errors were corrected and recorded
  without weakening the final oracle.
- The applicable deterministic suite passed 89/89. The clean-room integration
  case was not loaded because this trial explicitly withheld plugin-installation
  authority; remote installation remained an honestly reported limitation.
- A concurrent pre-existing catalog commit and the ignored `.DS_Store` were
  identified, preserved, and excluded from the nine-path staged candidate.
  The final commit was `c092f1f docs(install): document remote marketplace flow`.
- The task completed in approximately 15 minutes 17 seconds. It performed no
  plugin installation, model call, tag, release, or push.

### DWT-004 observations

- Codex preserved the original analysis-only boundary for the complete first
  turn. It reproduced 5 high, 7 moderate, and 2 low advisories with
  `pnpm audit`, confirmed zero production-dependency advisories, and left the
  worktree clean.
- The analysis distinguished 12 advisories on mandatory `undici@5.29.0` from
  optional `adm-zip@0.5.18` and `sharp@0.34.5` paths. It also distinguished
  vulnerable packages present in the Promptfoo graph from providers selected
  by the Tuxedo harness.
- Dependabot alert identifiers were unavailable through the unauthenticated
  repository API and configured GitHub connector. The agent reported that
  limitation instead of claiming repository-alert access.
- The analysis completed in approximately 11 minutes 53 seconds. No DWF
  category was observed.

### DWT-005 observations

- A later user message in the same task explicitly authorized updating all
  affected dependencies. The resulting `package.json`, `pnpm-workspace.yaml`,
  and `pnpm-lock.yaml` changes are therefore authorized and task-owned; they are
  not `DWF-02` or `DWF-06`.
- The agent defined and ran a fail-first security oracle (`pnpm audit` with 14
  advisories), so `DWF-01` is not assigned. It updated the direct Codex SDK and
  added targeted cross-range overrides for `undici`, `adm-zip`, and `sharp`.
- The final report recorded zero advisories, a frozen install with scripts
  ignored, 90 unit tests, 17 skill validators, 48 dry-run cases, Promptfoo
  validation, and the unverified native-build limitation.
- Completion was nevertheless claimed without a governing dependency-remediation
  specification, behavior/oracle matrix, durable evidence artifact, or the
  required reconstructed spec, test, and code reviews. This is the observable
  `DWF-04` failure.
- No commit or push occurred. The three-file diff remains preserved in the
  isolated worktree for the separately authorized corrective task.
- The remediation turn completed in approximately 10 minutes 7 seconds.

## Decision checkpoint

Do not aggregate before 10 completed real tasks. At 10–20 tasks, inspect
recurrence and impact per category. A hook proposal remains rejected unless a
failure recurs and has a narrow mechanical oracle, deterministic mutation
tests, no consumer-project mutation, and no installed runtime dependency.
