# SPEC-0003 evidence

## Oracle provenance

| Criteria | Provenance | Independence boundary |
| --- | --- | --- |
| SC-001–SC-006, SC-009–SC-011 | `spec-derived` and `independent` | Expected ownership, authority, defaults, installation boundaries, and routing shapes were written before implementation; adversarial tests reject partial contracts. |
| SC-007 | `external` | Template selection was derived from MADR, C4, npm RFCs, and Google SRE primary sources rather than existing Tuxedo text. |
| SC-008 | `external` | GitHub Actions guidance was derived from GitHub's workflow syntax and security documentation. |
| SC-010 provider evidence | `diagnostic-probe` | Codex SDK skill-call metadata is heuristic and model routing is stochastic; it cannot prove instruction influence. |

## Fail-first

The focused command executed before implementation failed for the expected missing boundaries:

```bash
uv run python -m unittest \
  tests.test_toolkit.ToolkitStructureTests.test_skill_catalog_contract_covers_every_distributed_skill \
  tests.test_toolkit.ToolkitStructureTests.test_catalog_overlap_and_authority_contracts_are_explicit \
  tests.test_toolkit.ToolkitStructureTests.test_explicit_only_skill_policies_match_catalog_contract \
  tests.test_toolkit.ToolkitStructureTests.test_spec_templates_do_not_preselect_risk_or_review_policy \
  tests.test_toolkit.ToolkitStructureTests.test_documentation_and_ci_reference_assets_are_routed_and_sourced \
  tests.test_toolkit.ToolkitStructureTests.test_readme_documents_codex_installation_and_discovery \
  tests.test_toolkit.ToolkitStructureTests.test_agents_contract_has_conventional_commit_examples
```

Observed: seven failures/errors for absent catalog, policies, neutral template defaults, assets, onboarding, and commit examples. A separately invoked routing oracle failed with missing `implicit-spec`, proving that the six new cases were absent. One initial test selector referenced the wrong unittest class; that setup error was corrected and was not counted as product fail-first evidence.

## Deterministic implementation evidence

- Focused contract/routing oracles: pass after implementation.
- Unit suite: pass; final count recorded in the final verification section below.
- Legacy dry-run: 48 deterministic runs; final fingerprint recorded below.
- Promptfoo configuration: valid.
- Official plugin validator: pass.
- Official skill validator: 17/17 pass.
- Shell syntax: no shell source files are present in the repository.
- `git diff --check`: final result recorded below.

The official validators ran with:

```bash
uv run --isolated --with PyYAML python -c '<load runner and execute _official_validators()>'
```

This kept PyYAML outside project dependencies.

## Provider evidence

Authentication status passed through the dedicated home:

```text
Dedicated Codex evaluation home: $HOME/.codex-tuxedo-evals
Codex CLI authentication is valid via ChatGPT/Codex.
```

The invalid 9-row attempt was rejected after it exposed Promptfoo array expansion. With the corrected schema and concrete CI fixture:

- isolated `composition-ci-security`: 1/1 pass, 251.042 s, report SHA-256 `8d306992347cb98dcdb12d2245f8de46667d9ffd23f83a5c92461e858e5a9dd0`;
- six affected cases: 5/6 pass, 644.001 s, report SHA-256 `7dc85ded508f1061ebd0cc787ba8551aa2dba2ab1fc244e3d4f45de44c9331b5`;
- repeated batch failure: `composition-ci-security` observed neither expected skill, while the other five cases passed.

This is non-green empirical evidence. The isolated pass cannot override the complete batch failure. No full 117-call evaluation was run.

After delivery of the initial implementation, the maintainer explicitly authorized diagnosis of the failed composed case, affected reruns, and—only after routing stability—the complete evaluation with a two-hour limit. Push, release, publication, deploy, production, and destructive authority remain withheld.

## Primary-source evidence

- Codex skill discovery, implicit/explicit invocation, plugin surfaces, and local marketplace setup: current OpenAI Codex manual fetched on 2026-08-06.
- MADR 4.0.0: https://adr.github.io/madr/
- C4 model: https://c4model.com/diagrams
- npm RFC process: https://github.com/npm/rfcs
- Google SRE postmortem culture: https://sre.google/workbook/postmortem-culture/
- GitHub Actions workflow syntax: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- GitHub Actions security hardening: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions

## Final verification

- Official plugin validator: pass.
- Official skill validator: 17/17 pass.
- `uv run python -m unittest discover -s tests -v`: 74/74 pass.
- `uv run python evals/run.py --dry-run`: 48 runs; fingerprint `494fd36763016dbc5a3291afe3cfa482fb4f776fe49b3d0b1618cb5a77d4b0ca`.
- `pnpm run promptfoo:validate`: configuration valid.
- Shell syntax: no shell source files found.
- `git diff --check`: pass.
- `git status --short`: only task-owned tracked and untracked paths before commit.

The deterministic contract is green. The empirical affected routing gate is
not green: 5/6 in the complete batch, with one isolated 1/1 pass that does not
override the batch failure.
