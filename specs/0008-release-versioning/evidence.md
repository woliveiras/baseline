# SPEC-0008 evidence

## Fail-first evidence

On 2026-08-08, before release implementation, this focused command ran the new
release oracles:

```bash
uv run python -m unittest discover -s tests -p 'test_toolkit.py' -k release -v
```

Result: 3 tests ran and all 3 errored for the expected missing release surfaces:
`.github/workflows/ci.yml`, `CHANGELOG.md`, and
`.release-please-manifest.json`. No production release artifact existed yet.

## Local implementation evidence

- Focused release tests: 3/3 passed.
- Reconciled project-vocabulary test: 1/1 passed.
- Reconciled remote-marketplace documentation test: 1/1 passed.
- Full deterministic unit suite: 95/95 passed.
- `uv run python evals/run.py --dry-run`: passed with all 48 seeded run
  configurations and no provider/model execution.
- `pnpm install --frozen-lockfile --ignore-scripts`: passed with the committed
  lockfile unchanged.
- All three new GitHub YAML files parsed successfully with PyYAML 6.0.2.
- `actionlint` 1.7.7 reported no workflow findings.
- Release Please 17.6.0's pinned official JSON Schema accepted
  `release-please-config.json` with no validation errors.
- Official plugin validator from OpenAI Codex `rust-v0.146.0` passed.
- Official skill validator from the same pinned Codex commit passed for exactly
  17 skill directories. The initial simulation exposed and then removed the
  accidental `catalog.md` glob input.
- Shell syntax checks and `git diff --check` passed.
- A concurrent, unrelated `AGENTS.md` edit appeared during validation. It was
  not modified by this task and is excluded from the task-owned candidate.

## Required completion evidence

The final local suite repeated 95/95 unit tests, the 48-case evaluation dry-run,
YAML parsing, `actionlint`, shell syntax, and `git diff --check` successfully.
Pending the final-candidate repeat of protected pull-request CI, protected
`main` merge, tag/GitHub Release inspection, and tag-pinned clean-room Codex
installation.

## Protected pull-request evidence

- Draft PR [#1](https://github.com/woliveiras/tuxedo/pull/1) ran `Validate` on
  candidate `cf90cd8`; GitHub Actions run `31266278812`, job `93124824801`,
  passed in 26 seconds.
- The GitHub Actions repository policy keeps default workflow permissions at
  `read` and now permits Actions to create Release Please pull requests.
- The `main` branch-protection API reports strict required context `Validate`
  from GitHub Actions app `15368`, pull-request enforcement with zero mandatory
  approvals, administrator enforcement, linear history, required conversation
  resolution, and disabled force pushes/deletion.
- This evidence commit intentionally changes the candidate SHA, so `Validate`
  must pass again before merge.

## Release automation regression

The protected bootstrap merged as `4370b1ebecb31f58619e8f877fccbea9769c92a7`.
Main CI run `31266579295` passed, but the first Release Please run
`31266579282` exposed two independent defects before publication:

1. With no prior tag or `bootstrap-sha`, Release Please included historical
   `feat` commits and opened PR [#2](https://github.com/woliveiras/tuxedo/pull/2)
   for `0.2.0` instead of waiting for the `v0.1.0` bootstrap.
2. The exact generated candidate updated synchronized versions to `0.2.0`, but
   three tests froze current versions at `0.1.0`. The read-only validation job
   failed and the no-checkout status job reported `Validate: failure` on head
   `e2a9e8380aadbadeb28176270ec525bf829a1dfc`, so protection blocked merge.

Ranked hypotheses and outcomes:

- unbounded pre-bootstrap commit history caused the premature minor proposal:
  confirmed by Release Please's documented bootstrap behavior and PR #2;
- hardcoded current-version assertions rejected legitimate release candidates:
  confirmed by the three exact CI assertion failures;
- the generated-PR status bridge failed to protect `main`: disproved because it
  attached the failure to the resolved head and branch protection blocked PR #2.

PR #2 was closed without merge. The regression fix adds the protected bootstrap
merge as top-level `bootstrap-sha`, makes current-version oracles dynamic, adds
generic README version updates, moves checkout/setup-node to pinned v5 commits,
and disables the unused UV cache that generated a warning.

The corrected release-focused regression suite passed 3/3. The reconciled
identity, manifest inventory, and remote-install documentation tests each
passed. `actionlint` 1.7.7, YAML parsing, `git diff --check`, and the official
Release Please 17.6.0 JSON Schema also passed. A clean task-owned PR must repeat
the full suite because concurrent SPEC-0009 work is intentionally preserved in
the local worktree and excluded from this correction.
