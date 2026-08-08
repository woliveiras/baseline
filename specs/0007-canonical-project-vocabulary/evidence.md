# SPEC-0007 evidence

Date: 2026-08-08

## Documentation decision

- Decision: `required`
- Rationale: The task changes project identity and the operational meaning of
  boundary and authority terms across public and repository documentation.
- Intended active surfaces: `package.json`, `AGENTS.md`, `GLOSSARY.md`,
  `README.md`, current development/evaluation documentation, evaluation labels
  and source comments, active specifications, and deterministic tests.
- Preserved surfaces: completed evidence/review records and the frozen internal
  repository audit.

## Fail-first evidence

| Criterion | Verification | Test-tree digest | Expected failure | Observed failure | Provenance |
| --- | --- | --- | --- | --- | --- |
| TV-001–TV-006 | `uv run python -m unittest -v tests.test_toolkit.ToolkitStructureTests.test_canonical_project_vocabulary_and_package_identity` | `1c6d6f30ebf6b82a401dae7d4cf2e2b5c0348d59` | The pre-migration package identity or active terminology fails the canonical vocabulary contract | Failed at the first identity oracle: expected `tuxedo`, observed the role-branded evaluation package name | spec-derived |

## Passing evidence

| Criterion | Verification | Result |
| --- | --- | --- |
| TV-001–TV-006 | `uv run python -m unittest -v tests.test_toolkit.ToolkitStructureTests.test_canonical_project_vocabulary_and_package_identity` | pass: 1 test |
| TV-001–TV-006 | `uv run python -m unittest discover -s tests -v` | pass: 92 tests |
| TV-006 | Official Codex plugin validator | pass: `plugins/tuxedo` |
| TV-006 | Official Codex skill validator for each distributed skill | pass: 17 skills |
| TV-006 | `uv run python evals/run.py --dry-run` | pass: 48 seeded comparison runs; no provider/model call |
| TV-003/TV-006 | `pnpm run promptfoo:validate` | pass: configuration valid |
| TV-001 | `pnpm install --frozen-lockfile --ignore-scripts` | pass: lockfile current; no dependency or lockfile change |
| TV-003 | `bash -n` for every tracked `*.sh` file | pass |
| TV-003/TV-005 | Repository-wide `rg -i maintainer` audit and Git diff inspection | pass: active uses are limited to the role definition, SPEC-0007 rationale, and the deterministic retired-term oracle; older uses are completed evidence/reviews or the frozen audit |
| TV-005 | SHA-256 comparison of the old and renamed SPEC-0006 evidence and three review files | pass: all four pairs are byte-identical |
| TV-006 | `codex plugin remove tuxedo@tuxedo`, `codex plugin add tuxedo@tuxedo`, `codex plugin list` | pass: `tuxedo@tuxedo` 0.1.0 installed and enabled from `plugins/tuxedo` |
| TV-006 | Recursive installed/source comparison and plugin-manifest SHA-256 | pass: no diff; both manifests `b7330fdd2e0e3ca00e442cf503720f5d0e77df9d6e20901cc81cb8cd83c09156` |

The passing test-tree SHA-256 is
`957636880924dd7e9cd46e7738eb0196ac21c42ce69f7658255dae3aa15b5fd3`.

## Residual limitations

- Historical evidence, completed reviews, and the frozen repository audit still
  contain their original `maintainer` wording by design. Rewriting those files
  would falsify the recorded context and violate TV-005.
- `maintainer` remains a valid role term. The change removes its use as project
  identity, generic boundary, dependency class, or source of task authority;
  it does not ban the word globally.
- Provider/model evaluations were not run because the user authorized local
  implementation and installation, not quota-consuming evaluation calls.
