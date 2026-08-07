# SPEC-0004 evidence

## Fail-first evidence

| Criterion | Verification or probe | Test-tree digest | Command | Expected failure | Observed failure | Oracle provenance |
| --- | --- | --- | --- | --- | --- | --- |
| CP-001–CP-003, CP-007 | Package boundary and documentation tests | `6eb4ec66815edccde4b8032b89eb13ccf7aedae7` | `uv run python -m unittest -v tests.test_toolkit.ToolkitStructureTests.test_plugin_package_boundary_and_canonical_skill_tree tests.test_toolkit.ToolkitStructureTests.test_codex_plugin_clean_room_install_discover_remove_and_reinstall` | Existing marketplace points to repository root; dedicated package and compatibility link are absent | Two failures: expected `./plugins/tuxedo`, observed `./`; the CLI lifecycle stopped before copying | spec-derived, independent |
| CP-004–CP-006 | Initial real Codex clean-room diagnostic | pre-test diagnostic | isolated `codex plugin marketplace add`, `plugin list`, and `plugin add` with a 30-second observation bound | Root-source installation copies maintainer content and cannot complete promptly | Codex CLI 0.144.4 created two interrupted partial caches of 780 MB and 807 MB containing `node_modules/`, `evals/`, and `specs/`; a 260 KB control package installed successfully | external, diagnostic-probe |

## Passing evidence

| Criterion | Test-tree digest | Command | Result | Timestamp or run identifier |
| --- | --- | --- | --- | --- |
| CP-001–CP-007 | `1d498959674f3683e17dd1c1a65da30f42082229` | `uv run python -m unittest discover -s tests -v` | 81/81 pass, including real install, 17-skill App Server discovery, remove, and reinstall | 2026-08-07 / Codex CLI 0.144.4 |
| CP-001–CP-003 | `1d498959674f3683e17dd1c1a65da30f42082229` | official plugin validator plus all official skill validators through isolated UV/PyYAML | plugin pass; 17/17 skills pass | 2026-08-07 |
| CP-001–CP-007 | `1d498959674f3683e17dd1c1a65da30f42082229` | `pnpm run promptfoo:validate`; `uv run python evals/run.py --dry-run`; shell syntax; `git diff --check` | valid; 48 runs with fingerprint `0f99551effe2b515832bc5ff3667cb8e0ed25b85bdd6b8cfa250a2f2032b3e9b`; zero shell files; pass | 2026-08-07 |

## Documentation decision

- Decision: `required`
- Rationale: The install command remains simple, but users and maintainers need an explicit distinction between the repository, the package root, and the standalone skill path.
- Updated artifacts: `README.md`, `docs/development.md`, `docs/README.md`, and `AGENTS.md`.

## Residual limitations

- Installation and discovery do not establish that a model follows a skill correctly; real-task trials remain separate evidence.
- Codex desktop UI and non-Codex clients are outside this clean-room run.
- The root compatibility symlink is supported for the maintainer's macOS and Linux scope; the installed plugin contains no symlinks.

## Primary source

- OpenAI Codex plugin package and repo-marketplace layout: https://developers.openai.com/plugins/build/plugins
