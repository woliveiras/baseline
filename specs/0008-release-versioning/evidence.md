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
Pending protected pull-request CI, protected `main` merge, tag/GitHub Release
inspection, and tag-pinned clean-room Codex installation.
