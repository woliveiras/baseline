# SPEC-0005 evidence

## Oracle provenance

| Criteria | Provenance | Independence boundary |
| --- | --- | --- |
| RM-001–RM-002, RM-004–RM-008 | `spec-derived` | The user request and approved specification define the exact command sequence, lifecycle, limitations, credential boundary, and maintainer path before the documentation test was run. |
| RM-003 | `external` and `spec-derived` | The SSH URL and repeated `--sparse`/`--ref` options were cross-checked against the installed Codex CLI help; the private-repository security boundary comes from the approved specification. |

## Fail-first evidence

| Criterion | Verification or probe | Test-tree digest | Command | Expected failure | Observed failure | Oracle provenance |
| --- | --- | --- | --- | --- | --- | --- |
| RM-001–RM-008 | Remote marketplace documentation contract | `0f1ac59db8f4bdca3e7fe1a1b527d73fd1ec2ccf` | `uv run python -m unittest -v tests.test_toolkit.ToolkitStructureTests.test_readme_documents_remote_marketplace_installation_contract` | The README has no canonical remote command sequence or the required lifecycle and limitation markers | Failed before documentation implementation at the first assertion: the exact `codex plugin marketplace add woliveiras/tuxedo --ref main` plus `codex plugin add tuxedo@tuxedo-local` sequence was absent | spec-derived |

The later focused failures were test-authoring corrections for Markdown
capitalization (`main` rendered as `` `main` `` and the lower-case heading
phrase) and a temporary malformed sparse-command test literal. They were not
product failures. The final focused run passed after the test expectations and
literal were reconciled with the written contract.

## Passing evidence

| Criterion | Test-tree digest | Command | Result | Timestamp or run identifier |
| --- | --- | --- | --- | --- |
| RM-001–RM-008 | `0f1ac59db8f4bdca3e7fe1a1b527d73fd1ec2ccf` | `uv run python -m unittest -v tests.test_toolkit.ToolkitStructureTests.test_readme_documents_remote_marketplace_installation_contract` | 1/1 pass; exact remote, sparse, SSH, lifecycle, credential, mutable-ref, no-direct-URL, and maintainer-clone assertions passed | 2026-08-07 |
| RM-001–RM-008 | `0f1ac59db8f4bdca3e7fe1a1b527d73fd1ec2ccf` | Filtered `uv run python` unittest loader excluding `test_codex_plugin_clean_room_install_discover_remove_and_reinstall` | 89/89 deterministic tests pass; the prohibited plugin-install integration test was not loaded | 2026-08-07 |
| RM-001–RM-004, RM-008 | n/a | `codex plugin marketplace add --help`; `codex plugin add --help`; `codex plugin marketplace upgrade --help` | Codex CLI 0.144.4 documents `owner/repo[@ref]`, HTTPS and SSH Git sources, `--ref`, repeatable `--sparse`, marketplace upgrade, and selector-only plugin installation; no plugin was installed | 2026-08-07 |
| RM-006 | n/a | `git tag --list` | No local Git tags are present; documentation records the governing current limitation that no Git tags are published yet | 2026-08-07 |
| RM-001–RM-008 | n/a | Official plugin validator and official skill validator for every `plugins/tuxedo/skills/*` skill through isolated UV/PyYAML | Plugin validation passed; 17/17 skill validations passed | 2026-08-07 |
| RM-001–RM-008 | n/a | `uv run python evals/run.py --dry-run` | 48 deterministic configurations generated; current fingerprint `b030bf3e0fa391e232330c54aef6d1366df8c35a95b60cf7e016046e17f356a5`; no model call | 2026-08-07 |
| RM-001–RM-008 | n/a | `pnpm run promptfoo:validate` | Configuration is valid; no model call | 2026-08-07 |
| RM-001–RM-008 | n/a | `git diff --check` | pass for the current worktree candidate | 2026-08-07 |

## Post-authorization remote clean-room evidence

After the original task completed, the maintainer explicitly authorized push
and remote installation testing. The evidence commit was available at
`origin/main` before these probes ran.

| Criterion | Test-tree digest | Command or probe | Result | Timestamp or run identifier |
| --- | --- | --- | --- | --- |
| RM-009 | `3ad1a6aceff88c332da0e7a86360bee38aeb7805` | Isolated `HOME` and `CODEX_HOME`; `codex plugin marketplace add woliveiras/tuxedo --ref main --json` with both API-key variables removed | Expected transport-authentication failure: the shorthand cloned over HTTPS, the repository was private, and terminal credential prompts were disabled | 2026-08-07 |
| RM-003–RM-005, RM-009 | `3ad1a6aceff88c332da0e7a86360bee38aeb7805` | Isolated remote SSH lifecycle using `git@github.com:woliveiras/tuxedo.git`, marketplace upgrade, plugin add, app-server `skills/list`, remove, reinstall, and final plugin/marketplace removal | pass; package contained only `.codex-plugin` and `skills`, all 17 expected Tuxedo skills were enabled and resolved inside the isolated plugin cache, no `auth.json` was created, and final configured state was empty | 2026-08-07 |
| RM-001–RM-009 | `3ad1a6aceff88c332da0e7a86360bee38aeb7805` | `uv run python -m unittest -v tests.test_toolkit.ToolkitStructureTests.test_readme_documents_remote_marketplace_installation_contract` | 1/1 pass after the private-access clarification | 2026-08-07 |

## Documentation decision

- Decision: `required`
- Rationale: The change is a public installation and credential-boundary contract. A consumer needs executable commands and explicit limitations, while maintainers need the local clone path preserved separately.
- Updated artifacts: `README.md`, `docs/development.md`, and this specification's matrix, evidence, and review records.

## Original execution boundary

- No plugin installation or reinstallation was run. In particular, the
  existing clean-room test that invokes `codex plugin marketplace add` and
  `codex plugin add` was not executed because the user explicitly prohibited
  installation.
- No GitHub network fetch, SSH authentication, Codex login, model call, tag,
  release, publication, or push was performed.
- The full repository unittest discovery command was not run because it would
  execute the prohibited clean-room installation test while the Codex CLI is
  available. The focused deterministic test and a later filtered deterministic
  suite excluding that integration test are the applicable local evidence.

Those constraints describe commit `c092f1f`. They were superseded only for the
later, separately authorized remote clean-room probes recorded above; the
history is retained rather than rewritten as if the original task had broader
authority.

## Residual limitations

- Remote SSH installation and Codex CLI discovery are now verified. Anonymous
  HTTPS access remains unavailable while the repository is private; machines
  using the shorthand need separately configured GitHub HTTPS credentials.
- Codex desktop installation and UI discovery remain unexecuted.
- `main` remains mutable and no immutable Git ref is documented because no Git
  tags are published yet. A future tag must be verified before documentation
  can recommend it.
- The existing ignored `plugins/tuxedo/.DS_Store` remains outside this task's
  commit and is preserved without cleanup. A concurrent pre-existing commit
  `0e6df59 docs(catalog): add Mermaid contract views` was observed and is not
  part of this task's candidate.
