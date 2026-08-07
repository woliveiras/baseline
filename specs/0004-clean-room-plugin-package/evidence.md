# SPEC-0004 evidence

## Fail-first evidence

| Criterion | Verification or probe | Test-tree digest | Command | Expected failure | Observed failure | Oracle provenance |
| --- | --- | --- | --- | --- | --- | --- |
| CP-001–CP-003, CP-007 | Package boundary and documentation tests | `6eb4ec66815edccde4b8032b89eb13ccf7aedae7` | `uv run python -m unittest -v tests.test_toolkit.ToolkitStructureTests.test_plugin_package_boundary_and_canonical_skill_tree tests.test_toolkit.ToolkitStructureTests.test_codex_plugin_clean_room_install_discover_remove_and_reinstall` | Existing marketplace points to repository root; dedicated package and compatibility link are absent | Two failures: expected `./plugins/tuxedo`, observed `./`; the CLI lifecycle stopped before copying | spec-derived, independent |
| CP-004–CP-006 | Initial real Codex clean-room diagnostic | pre-test diagnostic | isolated `codex plugin marketplace add`, `plugin list`, and `plugin add` with a 30-second observation bound | Root-source installation copies maintainer content and cannot complete promptly | Codex CLI 0.144.4 created two interrupted partial caches of 780 MB and 807 MB containing `node_modules/`, `evals/`, and `specs/`; a 260 KB control package installed successfully | external, diagnostic-probe |
| CP-008–CP-009 | Six local-link fixtures covering valid, missing, escaping, valid anchor, missing anchor, and external URL cases | `ffa0889db2bee9ecc2a65e9f1ad453862c496edb` | `uv run python -m unittest -v tests.test_toolkit.MarkdownLinkValidationTests` | Only the escape and missing-anchor cases fail against the existence-only validator | 6 executed: 4 passed; `test_local_link_cannot_escape_package` and `test_missing_heading_anchor` failed because the validator returned no errors | spec-derived, independent |

## Passing evidence

| Criterion | Test-tree digest | Command | Result | Timestamp or run identifier |
| --- | --- | --- | --- | --- |
| CP-001–CP-007 | `1d498959674f3683e17dd1c1a65da30f42082229` | `uv run python -m unittest discover -s tests -v` | 81/81 pass, including real install, 17-skill App Server discovery, remove, and reinstall | 2026-08-07 / Codex CLI 0.144.4 |
| CP-001–CP-003 | `1d498959674f3683e17dd1c1a65da30f42082229` | official plugin validator plus all official skill validators through isolated UV/PyYAML | plugin pass; 17/17 skills pass | 2026-08-07 |
| CP-001–CP-007 | `1d498959674f3683e17dd1c1a65da30f42082229` | `pnpm run promptfoo:validate`; `uv run python evals/run.py --dry-run`; shell syntax; `git diff --check` | valid; 48 runs with fingerprint `0f99551effe2b515832bc5ff3667cb8e0ed25b85bdd6b8cfa250a2f2032b3e9b`; zero shell files; pass | 2026-08-07 |
| CP-003, CP-008–CP-009 | `01d5ff6f5e99bcd776c8f530824079f27e54f87f` | `uv run python -m unittest -v tests.test_toolkit.MarkdownLinkValidationTests tests.test_toolkit.ToolkitStructureTests.test_links_resolve_and_no_placeholders` | 9/9 pass: valid and missing targets, direct and encoded escape, valid and missing anchors, fragment-only and encoded references, external URL with connection seam unused, and installed traversal through `skills/` | 2026-08-07 |
| CP-001–CP-009 | `01d5ff6f5e99bcd776c8f530824079f27e54f87f` | `uv run python -m unittest discover -s tests -v` with the unrelated ignored `plugins/tuxedo/.DS_Store` preserved temporarily outside the package and automatically restored | 89/89 pass; the same command against the unmodified checkout produced 87/89 because both package-boundary tests correctly rejected the ignored file | 2026-08-07 |
| CP-001–CP-003, CP-008–CP-009 | `01d5ff6f5e99bcd776c8f530824079f27e54f87f` | Official plugin validator; official skill validator for every skill through isolated UV with PyYAML 6.0.2 | plugin pass; 17/17 skill validations pass; no repository dependency added | 2026-08-07 |
| CP-001–CP-009 | `01d5ff6f5e99bcd776c8f530824079f27e54f87f` | `uv run python evals/run.py --dry-run`; tracked shell syntax inventory; `git diff --check` | 48 dry-run configurations with fingerprint `0f99551effe2b515832bc5ff3667cb8e0ed25b85bdd6b8cfa250a2f2032b3e9b`; zero tracked shell files; diff check passes | 2026-08-07 |

## Documentation decision

- Decision: `required`
- Rationale: The install command remains simple, but users and maintainers need an explicit distinction between the repository, the package root, and the standalone skill path.
- Updated artifacts: `README.md`, `docs/development.md`, `docs/README.md`, and `AGENTS.md`.

### Link-integrity amendment

- Decision: `required`
- Rationale: The installed-package contract, behavior matrix, fail-first evidence, and separated review records must describe the new deterministic guarantee; user-facing installation steps do not change.
- Updated artifacts: `spec.md`, `behavior-matrix.md`, `evidence.md`, and `reviews/` within SPEC-0004.

## Residual limitations

- Installation and discovery do not establish that a model follows a skill correctly; real-task trials remain separate evidence.
- Codex desktop UI and non-Codex clients are outside this clean-room run.
- The root compatibility symlink is supported for the maintainer's macOS and Linux scope; the installed plugin contains no symlinks.
- External URLs are classified and skipped without network I/O; their availability and remote fragments remain deliberately unverified.
- The ignored, untracked `plugins/tuxedo/.DS_Store` was preserved. It is not part of the commit, but while present it correctly makes the two installed-package boundary tests fail; a clean tracked candidate passes 89/89.

## Primary source

- OpenAI Codex plugin package and repo-marketplace layout: https://developers.openai.com/plugins/build/plugins
