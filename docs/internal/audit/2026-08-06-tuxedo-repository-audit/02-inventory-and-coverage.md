# 02 — Inventory and coverage ledger

## Mechanical summary

| Tracked surface | Files |
| --- | ---: |
| Root/manifest/license/toolchain | 8 |
| `docs/` | 11 |
| `evals/` | 34 |
| `hooks/` | 2 |
| `skills/` | 58 |
| `templates/` | 9 |
| `tests/` | 4 |
| **Total** | **126** |

The recalculated total was 16,387 lines. No PDF, shell script, symlink, or binary file was tracked. `rg --files -uu` found approximately 108,000 entries because of `node_modules/`; that tree occupied approximately 3.8 GiB and is not distributed product content.

## Disposition legend

- `RI`: reviewed in full, with content reading and contextual comparison.
- `FH`: reviewed as a member of a homogeneous family, with complete inventory, parsing/schema, mechanical comparison, and explicit samples.
- `GO`: placeholder/generated; validated by origin, convention, and invariants, with no semantic content to read.
- `NE`: not reviewed. **No tracked file was in this category.**

## Complete coverage ledger

Each line below represents a tracked file and its disposition. The list was derived from `git ls-files`, not `rg --files`.

### Root, plugin, and toolchain

```text
RI  .codex-plugin/plugin.json
RI  .gitignore
RI  AGENTS.md
RI  LICENSE
RI  README.md
RI  package.json
FH  pnpm-lock.yaml
RI  pnpm-workspace.yaml
```

The lockfile was parsed in full as YAML, aggregated by packages/snapshots/integrity/license, and sampled at the direct Promptfoo and Codex SDK nodes. The 792 dev entries were not read manually line by line.

### Documentation

```text
RI  docs/README.md
RI  docs/architecture/enforcement.md
RI  docs/architecture/eval-isolation.md
RI  docs/architecture/evaluations.md
RI  docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
RI  docs/decisions/README.md
RI  docs/development.md
RI  docs/evidence/eval-runs.md
RI  docs/guides/using-the-eval-harness.md
RI  docs/internal/skill-creator-limitations.md
RI  docs/research/evidence-map.md
```

Local links in all tracked Markdown documents were validated, including anchors. The three eval documents modified before the audit were read as actual state, and the diff against `HEAD` was preserved as provenance evidence.

### Evals — harness, assertions, configs, and fixtures

```text
FH  evals/fixtures/catalog.json
RI  evals/promptfoo/assertions/routing.py
RI  evals/promptfoo/assertions/security.py
RI  evals/promptfoo/assertions/trajectory.py
RI  evals/promptfoo/assertions/workspace.py
FH  evals/promptfoo/compare-config.yaml
GO  evals/promptfoo/generated/.gitkeep
FH  evals/promptfoo/promptfooconfig.yaml
RI  evals/promptfoo/prompts.py
FH  evals/promptfoo/redteam-config.yaml
GO  evals/promptfoo/results/.gitkeep
FH  evals/promptfoo/routing-config.yaml
RI  evals/promptfoo/scripts/codex_auth.py
RI  evals/promptfoo/scripts/prepare-workspaces.py
RI  evals/promptfoo/scripts/run-evaluations.py
FH  evals/promptfoo/security-config.yaml
FH  evals/promptfoo/smoke-config.yaml
RI  evals/promptfoo/tests.py
FH  evals/promptfoo/tests/behavior.yaml
FH  evals/promptfoo/tests/routing-contract.json
FH  evals/promptfoo/tests/routing.yaml
FH  evals/promptfoo/tests/security-regressions.yaml
GO  evals/results/.gitkeep
FH  evals/rubrics/secondary.json
RI  evals/run.py
FH  evals/tasks/bug-with-regression.json
FH  evals/tasks/clear-local-change.json
FH  evals/tasks/multi-module-change.json
FH  evals/tasks/no-change-correct.json
FH  evals/tasks/post-hoc-contamination.json
FH  evals/tasks/real-ambiguity.json
FH  evals/tasks/security-authority.json
FH  evals/tasks/spec-inconsistent.json
RI  evals/verifiers.py
```

All JSON/YAML files were parsed; the eight tasks and six configs were compared with the catalog of 48 dry-runs and the 34/40/12 matrix. Explicit semantic samples: `spec-inconsistent`, `post-hoc-contamination`, `security-authority`; positive, negative, and collision routing; the first and last security probes; and smoke, full behavior, and red-team configs. Assertions and all three runners were read in full.

### Hooks

```text
RI  hooks/hooks.json
RI  hooks/scripts/guard.py
```

In addition to reading, they were exercised with temporary fixtures for missing/malformed policy symlinks, a host cwd with a UV project, scope overlap, artifact/review aliases, a divergent staged index, and Git command forms.

### Skills — all 58 files

```text
RI  skills/brainstorming/SKILL.md
FH  skills/brainstorming/agents/openai.yaml
RI  skills/bugfix/SKILL.md
FH  skills/bugfix/agents/openai.yaml
RI  skills/bugfix/references/feedback-loops.md
RI  skills/ci-workflow/SKILL.md
FH  skills/ci-workflow/agents/openai.yaml
RI  skills/decision-framework/SKILL.md
FH  skills/decision-framework/agents/openai.yaml
RI  skills/decision-framework/references/evidence-types.md
RI  skills/design-deep-modules/SKILL.md
FH  skills/design-deep-modules/agents/openai.yaml
RI  skills/design-deep-modules/references/boundary-options.md
RI  skills/docs/SKILL.md
FH  skills/docs/agents/openai.yaml
RI  skills/docs/references/decision-record.md
RI  skills/docs/references/project-docs.md
RI  skills/docs/references/proposal.md
RI  skills/git-commit/SKILL.md
FH  skills/git-commit/agents/openai.yaml
RI  skills/improve-architecture/SKILL.md
FH  skills/improve-architecture/agents/openai.yaml
RI  skills/improve-architecture/references/architecture-diagrams.md
RI  skills/premortem/SKILL.md
FH  skills/premortem/agents/openai.yaml
RI  skills/refine/SKILL.md
FH  skills/refine/agents/openai.yaml
RI  skills/refine/references/decision-tree.md
RI  skills/security-review/SKILL.md
FH  skills/security-review/agents/openai.yaml
RI  skills/security-review/references/threat-model.md
RI  skills/session-bridge/SKILL.md
FH  skills/session-bridge/agents/openai.yaml
RI  skills/session-bridge/assets/handoff-template.md
RI  skills/shape-domain/SKILL.md
FH  skills/shape-domain/agents/openai.yaml
RI  skills/shape-domain/references/context-mapping.md
RI  skills/spec/SKILL.md
FH  skills/spec/agents/openai.yaml
RI  skills/spec/assets/behavior-matrix-template.md
RI  skills/spec/assets/spec-template.md
RI  skills/spec/references/behavior-matrix.md
RI  skills/spec/references/metadata.md
RI  skills/spec/references/scope-tiers.md
RI  skills/tdd/SKILL.md
FH  skills/tdd/agents/openai.yaml
RI  skills/tdd/references/provenance.md
RI  skills/technical-research/SKILL.md
FH  skills/technical-research/agents/openai.yaml
RI  skills/technical-research/references/source-quality.md
RI  skills/verify/SKILL.md
FH  skills/verify/agents/openai.yaml
RI  skills/verify/assets/code-review.json
RI  skills/verify/assets/evidence-template.md
RI  skills/verify/assets/spec-review.json
RI  skills/verify/assets/test-review.json
RI  skills/verify/references/review-contract.md
RI  skills/verify/references/scope-tiers.md
```

Each `SKILL.md`, reference, and asset was read individually. The 17 YAML files were parsed and compared as a family by name, description, `allow_implicit_invocation`, dependencies, and the corresponding `SKILL.md`. All passed the official validator.

### Templates

```text
RI  templates/codex/tuxedo.rules
RI  templates/policy/policy.json
RI  templates/policy/receipts.json
RI  templates/review/code.json
RI  templates/review/spec.json
RI  templates/review/tests.json
RI  templates/spec/behavior-matrix.md
RI  templates/spec/evidence.md
RI  templates/spec/spec.md
```

The templates were compared with hooks, skills/assets, documentation, and normal, blocked, and authorized cases. The seven copy pairs were compared byte for byte; they were identical in the snapshot.

### Tests

```text
FH  tests/fixtures/hooks/pretool-malformed.json
FH  tests/fixtures/hooks/pretool-missing.json
FH  tests/fixtures/hooks/pretool-valid.json
RI  tests/test_toolkit.py
```

`pretool-malformed.json` is intentionally invalid JSON; it was therefore excluded, with justification, from global JSON validation. The 65-test file was read by family and executed in full.

## Relevant untracked/ignored surfaces

| Surface | Observed state | Disposition and risk |
| --- | --- | --- |
| `node_modules/` | ~107,529 files; ~3.8 GiB | Mechanical inventory and supply-chain review through lockfile/package metadata; not distributed. |
| `evals/promptfoo/results/*.json` | 127 reports/1,618,535 bytes at checkpoint; count grew during external execution | All 127 parsed and aggregated; explicit sample. Final new files inventoried, but not used as evidence. |
| `evals/promptfoo/generated/` | only `.gitkeep` at checkpoint | No generated probes persisted. |
| `evals/results/` | only `.gitkeep` | No ignored legacy report at checkpoint. |
| `docs/tmp/v0.1-map.md` | 89 lines, ignored by `.gitignore:16` | Read in full; only migration disposition ledger, containing personal paths and `never-commit`; finding `TUX-AUD-024`. |
| `__pycache__/`, `*.pyc` | pre-existing ignored artifacts | Not removed; checks were run with `PYTHONDONTWRITEBYTECODE=1`. |
| Dedicated eval home | outside the checkout | Not inspected to avoid touching auth/credentials; only validation code and synthetic fixtures were audited. |
| Context PDFs | absent locally | Reconstructed from arXiv URLs in an external temp directory; original bytes unverifiable. |

## Integrity, secrets, and personal paths

- No absolute personal path was found in a tracked file.
- Occurrences of `OPENAI_API_KEY`, `CODEX_API_KEY`, auth, and canaries in tracked files are contracts/tests, not real values.
- No real secret was identified by the pattern-oriented text scan; this is not equivalent to complete cryptographic secret scanning.
- The only personal path observed is in the ignored `docs/tmp/v0.1-map.md`.
- All 595 observed lockfile snapshots had integrity where applicable; the lockfile was not changed.

## Residual coverage risk

No tracked file lacks a disposition. Residual risk is concentrated in: legal interpretation of transitive licenses; actual behavior of clients that were not executed; sandbox/network/auth surfaces that could not be exercised empirically; and ignored results created concurrently after the checkpoint.
