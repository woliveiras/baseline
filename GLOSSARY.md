# Repository glossary

## Governing input

The authoritative current source of expected behavior, scope, constraints, and
authority. It can be a user request, issue, bug report, external contract,
accepted decision, or explicitly approved behavior. Do not rewrite it merely to
make a change or check pass.

## Measurer

The ephemeral classifier that selects `S`, `M`, `L`, or `XL` from the highest
applicable risk, boundary, reversibility, ambiguity, validation, rollout, and
rollback concern. Its JSON result exists only in conversation. Line count is
not a driver.

## Material ambiguity

Uncertainty with at least two plausible answers that would change observable
behavior, scope, compatibility, constraints, or authority. Implementation
details that are reversible and testable are not material ambiguity.

## Fail-first

Running the smallest suitable verification before production behavior changes
and observing the expected behavioral failure. Infrastructure damage,
unrelated failures, and a test that already passes are not valid fail-first
signals.

## Verification

A unit, integration, contract, end-to-end, static, inspection, or other
executable check that compares observed behavior with the expected result from
the governing input. The check does not invent the expected result.

## Fresh result

The current output of a command or inspection actually performed for the
reviewed worktree. Historical reports remain records of their old candidate;
they are not current validation.

## Proportional review

Review depth selected by the highest applicable risk: `inline` for `S`,
`focused` for `M`, `expanded` for `L`, and `independent` when available for
`XL`. Every depth considers the governing input, expected behavior, complete
diff, relevant checks, unrelated changes, and limitations.

## Task-owned change

A file or hunk created or modified to satisfy the authorized current task.
Adjacent cleanup, pre-existing changes, and useful but unrequested work are not
task-owned without explicit scope expansion.

## ENG-NOTE

A grepable comment for a durable non-obvious reason, constraint, risk, or
history: `ENG-NOTE[kind][optional-id]: concise durable explanation`. It never
narrates the code or stores temporary status.

## Authority boundary

An action that cannot be inferred from implementation authority, including
staging, commit, push, release, publication, deploy, production mutation,
destructive operations, and irreversible policy changes.

## Product and repository boundaries

- `tuxedo` and **Tuxedo** are the stable machine and display identities.
- `development-only` describes tooling used to develop or evaluate Tuxedo that
  is never a consumer runtime dependency.
- `repository-only` describes tracked tests, docs, and evals excluded from the
  installed plugin.
- `user-authorized` means the current task controller explicitly granted an
  operation; being a developer or maintainer grants no task authority.
- `maintainer` names a stewardship role only, never a product identity,
  dependency class, or automatic authority source.
