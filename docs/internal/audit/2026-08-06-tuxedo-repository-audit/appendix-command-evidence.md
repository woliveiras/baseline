# Appendix — Command evidence

All commands are sanitized. Personal validator/checkout paths were replaced with descriptive variables. No output contains credentials, raw prompts, or model responses.

## Snapshot and inventory

| Command | Objective | Exit/duration | Result | Coverage/limit | Type |
| --- | --- | --- | --- | --- | --- |
| `pwd; git rev-parse HEAD; git branch --show-current; date -Iseconds; git status --short` | Fix snapshot | 0 / <0.1 s | checkout; `797d72c…`; `main`; three modified docs | BSD `date --iso-8601` failed earlier and was replaced by `date -Iseconds`; no writes | `external` |
| `git ls-files | sort` | Tracked inventory | 0 / <0.1 s | 126 files | Ledger base; excludes ignored files | `external` |
| `git ls-files -z | xargs -0 wc -l` | Tracked volume | 0 / <0.1 s | 16,387 lines | Physical lines | `diagnostic-probe` |
| `rg --files -uu` + `du`/`find` | Untracked/ignored inventory | 0 / ~10 s | ~108,000 entries; `node_modules` dominant | Count may vary with external execution | `diagnostic-probe` |
| `git diff -- <3 docs>` | Separate pre-existing changes | 0 / <0.1 s | only evidence-doc updates | Does not modify state | `external` |

## Versions

| Command | Exit/duration | Result |
| --- | --- | --- |
| `node --version` | 0 / <0,1 s | `v26.3.1` |
| `pnpm --version` | 0 / <0,1 s | `11.13.1` |
| `uv --version` | 0 / <0,1 s | `uv 0.9.5` |
| `uv run python --version` | 0 / <0,1 s | `Python 3.14.0` |
| `git --version` | 0 / <0,1 s | `2.50.1 (Apple Git-155)` |
| `zsh --version; bash --version` | 0 / <0,1 s | zsh 5.9; bash 5.3.9 |
| `codex --version` | 0 / <0,1 s | codex-cli 0.144.4 |
| package metadata/CLI Promptfoo | 0 / ~1 s | Promptfoo 0.122.0 |

## Official validators

Temporary setup, outside the checkout:

```bash
VALIDATOR_ENV="$(mktemp -d)/validator-env"
uv venv "$VALIDATOR_ENV"
uv pip install --python "$VALIDATOR_ENV/bin/python" 'PyYAML==6.0.2'
```

The first attempt stored `uv run ...` as a single string and returned exit 127 (`command not found`); it was classified as an orchestration error, not a product failure. The correct rerun:

```bash
TUXEDO_VALIDATOR_PYTHON="$VALIDATOR_ENV/bin/python" \
  "$VALIDATOR_ENV/bin/python" "$OFFICIAL_PLUGIN_VALIDATOR" .
for skill in skills/*; do
  TUXEDO_VALIDATOR_PYTHON="$VALIDATOR_ENV/bin/python" \
    "$VALIDATOR_ENV/bin/python" "$OFFICIAL_SKILL_VALIDATOR" "$skill"
done
```

| Objective | Exit/duration | Result | Coverage | Limit | Type |
| --- | --- | --- | --- | --- | --- |
| Official plugin validator | 0 / included in 1.02 s | pass | manifest/plugin layout | Does not validate hook semantics | `external` |
| Official validators for 17 skills | 0 / included in 1.02 s | 17/17 pass | frontmatter/shape of each package | Does not prove routing/behavior | `external` |

## Tests and dry-run

| Command | Objective | Exit/duration | Result | Coverage/limit | Type |
| --- | --- | --- | --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -v` | Deterministic suite | 0 / 2.121 s | 65/65 pass | Does not cover real cwd, staged index, deep symlink, or mutation cases | mixed |
| `PYTHONDONTWRITEBYTECODE=1 uv run python evals/run.py --dry-run` | Legacy matrix without provider | 0 / <0.1 s | 48 runs; fingerprint `1796ac…5bec` | Does not call a model or prove behavior | `diagnostic-probe` |

## Static Promptfoo checks

Executed with `PROMPTFOO_CONFIG_DIR=$(mktemp -d)`, telemetry/share/remote generation disabled, and no API keys in the child environment:

```bash
for config in evals/promptfoo/{compare-config,redteam-config,routing-config,security-config,smoke-config,promptfooconfig}.yaml; do
  pnpm exec promptfoo validate -c "$config"
done
```

| Objective | Exit/duration | Result | Coverage/limit | Type |
| --- | --- | --- | --- | --- |
| Validate six configurations | 0 / 12.36 s | 6/6 valid | YAML/config/static references | Does not execute provider/assertions | `diagnostic-probe` |

## Syntax, schemas, and links

| Command | Objective | Exit/duration | Result | Coverage/limit | Type |
| --- | --- | --- | --- | --- | --- |
| Python `json.loads` over tracked JSON | JSON | 0 / included in 21.14 s | 24 valid + 1 deliberately invalid fixture excluded | Documented exception: `pretool-malformed.json` | `diagnostic-probe` |
| `pnpm exec js-yaml` over tracked YAML | YAML | 0 / included in 21.14 s | 28 valid | Parse, not semantic schema | `diagnostic-probe` |
| `ast.parse` over tracked Python | Static Python | 0 / included in 21.14 s | 13 parseable scripts | Not type/lint/security proof | `diagnostic-probe` |
| `git ls-files '*.sh'` + shell syntax | Shell | N/A | 0 tracked shell scripts | Hook is Python; no `bash -n` applicable | `diagnostic-probe` |
| Local Markdown/anchor checker | Internal links | 0 / initial <1 s | 54 tracked docs, 77 local links, 9 external, 0 broken | Rerun after report, below | `diagnostic-probe` |
| `git grep` for absolute paths/secrets | Hygiene | 0 / <1 s | zero tracked absolute personal paths; only synthetic names/key contracts | Does not replace a dedicated scanner | `diagnostic-probe` |

## Hook and eval-validity probes

| Sanitized probe | Exit/result | Criterion | Type |
| --- | --- | --- | --- |
| Run the real hook command in a temporary UV project without policy | hook 0; `.venv` + `uv.lock` created | zero side effect | `diagnostic-probe` |
| Same with invalid `pyproject.toml` | UV 2 before guard | independent launcher | `diagnostic-probe` |
| Temporary Git: WT receipt `VALUE=1`, index `VALUE=999` | PreToolUse 0; Stop 0 | staged candidate | `diagnostic-probe` |
| Broken/external policy symlink/directory | allow; external read; traceback exit 1 | fail-closed | `diagnostic-probe` |
| Receipt without AC/aliased roles/contrary context | all passed the described mutations | fidelity/review schema | `diagnostic-probe` |
| `codex execpolicy check` on wrappers/options | decision `null` in listed cases | Rules claim | `external` |
| Synthetic trajectory `cat ~/.ssh/id_rsa` | `violations=[]` | outside-read probe | `diagnostic-probe` |
| Base64 canary | literal not detected | steganographic claim | `diagnostic-probe` |
| Synthetic eval home future directory/nested symlink | preflight accepted | fail-closed isolation | `diagnostic-probe` |

The probes did not touch credentials, personal home, network, or provider.

## Ignored results

```bash
find evals/promptfoo/results -maxdepth 1 -name '*.json' -print0
# parse, aggregate schema/suite/status/size/hash; sample oldest/newest + suite/shard/aggregate/focused
```

Independent checkpoint: exit 0; 127 JSON; 1,618,535 bytes; all parseable; documented hashes match; no duplicate content hash. Approximate duration <2 s. Concurrent external execution increased the count during the audit; the final count is in “Final state.”

## Supply chain

| Command | Objective | Exit/duration | Result | Limit | Type |
| --- | --- | --- | --- | --- | --- |
| `pnpm audit --json` | Current advisories | 1 / 1.4 s | 0 critical, 5 high, 7 moderate, 2 low | Registry scanner; exploitability unconfirmed | `external` |
| `pnpm outdated --format json` | Direct drift | 1 / ~1 s | SDK 0.146.0 → 0.146.1 | Exit 1 expected when outdated | `external` |
| Parse lockfile/package metadata | Effective graph/integrity/license | 0 / <2 s | 792 packages, 595 snapshots; SDK 0.144.6 and 0.146.0; license aggregation | License metadata, not legal opinion | `diagnostic-probe` |

## PDFs/external source

```bash
pdfinfo "$TMP_PDF"
pdftotext -layout "$TMP_PDF" "$TMP_TXT"
```

Exit 0 for the five arXiv PDFs. Pages: 12, 22, 12, 14, and 12 according to IDs/titles recorded in `01-*`. Objective: reconstruct missing sources and check their connection to the claims. Limit: bytes cannot be compared with the originally mentioned attachments because they were inaccessible. Type: `external` + `diagnostic-probe`.

## Explicitly unexecuted checks

- `pnpm run eval:full`, smoke/security/skills/compare with provider, semantic judges, and red-team: prohibited without separate human authority and would consume quota.
- `pnpm run eval:login`/auth status on the real home: login/credentials outside authority; no credential was read.
- Sandbox/network/browser empirical certification: would require an external provider/runtime.
- Windows hooks: environment unavailable.
- Destructive mutation/race/performance checks: out of scope; only safe fixtures.
- Project dependency upgrade/install: unauthorized; lockfile preserved.

## Final state

Checkpoint de fechamento: `2026-08-06T10:54:43+02:00`.

| Command | Exit/duration | Result |
| --- | --- | --- |
| Local link/anchor checker over tracked Markdown + report | 0 / 0.2 s | 65 files, 90 local links, 41 external, 0 broken |
| `git diff --check` | 0 / <0.1 s | pass |
| `git diff --no-index --check /dev/null <each report file>` | 0 aggregate / 0.2 s | 11/11 without whitespace error; exit 1 for “diff exists” handled separately |
| Headings/findings parser | 0 / <0.1 s | 29 unique IDs: 10 P1, 16 P2, 3 P3 |
| `git status --short` | 0 / <0.1 s | same three pre-existing modifications + only `?? docs/reviews/` |
| `find .../results -name '*.json'` at 10:53:58 checkpoint | 0 / <0.1 s | 132 JSON, 1,681,782 bytes |
| Filtered `ps` | 0 / <0.1 s | one external routing/provider still active; not started by the audit |

The external `eval:full` that started at 09:46:36 ended during the audit and wrote a sanitized 85/86 aggregate, status `fail` (routing 33/34; behavior 40/40; security 12/12; 3,780.371 s). It was **excluded from the conclusions**: it was not authorized/controlled by the audit, and the fingerprint, cardinality, isolation, and security-oracle findings remain. A new external routing run started afterward; therefore 132 is the checkpoint count, not a claim that ignored evidence is immutable.

State comparison:

```text
Inicial:
 M docs/architecture/evaluations.md
 M docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
 M docs/evidence/eval-runs.md

Final:
 M docs/architecture/evaluations.md
 M docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
 M docs/evidence/eval-runs.md
?? docs/reviews/
```

No tracked changes appeared outside the authorized directory. Ignored reports created by external processes were not removed, moved, rewritten, or attributed to the audit.

## Later relocation

At `2026-08-06T11:32:56+02:00`, at the maintainer's request, the report directory was moved from `docs/reviews/2026-08-06-tuxedo-repository-audit/` to `docs/internal/audit/2026-08-06-tuxedo-repository-audit/`. The preceding lines preserve the status observed at the original close. After relocation, the three pre-existing modifications remained unchanged and the 11 report files appeared exclusively under the new path; no product file was edited.

## Later reconciliation with HEAD

Checkpoint: 2026-08-06; `HEAD` `b46f37643adfa83897427cb2be3c7f383f3b35d9`.

| Command/evidence | Result | Use and limit |
| --- | --- | --- |
| `git diff --name-status 797d72c..HEAD` | 8 files changed | Delimited mechanisms that could have changed; none implements acceptance of the 29 findings. |
| `uv run python -m unittest discover -s tests -v` | 66/66 pass | Current deterministic evidence; does not replace missing oracles. |
| `uv run python evals/run.py --dry-run` | 48 runs | Current legacy catalog; does not prove provider or isolation. |
| Authorized full aggregate | routing 34/34; behavior 40/40; security 12/12; total 86/86 in 3,376.701 s | Evidence for configured cases, not certification of disputed identity/cardinality/oracles. |
| SHA-256 of full aggregate | `e6916e05766d7450c45a462b9b6e7a455672fb3595d8a32c1cc9211b4cc23827` | Identifies the local ignored artifact; does not complete the internal fingerprint. |
| `pnpm why @openai/codex-sdk --depth 2` | Promptfoo uses 0.144.6; root uses 0.146.0 | Confirms `TUX-AUD-022` remains open. |
| `pnpm audit --json` | 5 high, 7 moderate, 2 low, 0 critical | Confirms `TUX-AUD-025` remains open; severity is not exploitability. |
| `pnpm outdated --format json` | Direct SDK 0.146.0 → 0.146.1 | Drift observed; no dependency changed. |

The complete reconciliation and its Spec/Standards/Risk review are in [09 — Reconciliation](09-reconciliation-2026-08-06.md).

## Later lifecycle-enforcement removal

At `HEAD` `8776a6a`, SPEC-0001 and ADR 0002 removed hooks, the Python launcher, policies, completion receipts, review JSONs, and their tests/fixtures. The deterministic suite passed 63/63, dry-run retained 48 runs, Promptfoo validated the configuration, and official validators approved the plugin and 17/17 skills. The new fingerprint was `4268cf00971d61b58c59fb31b133f61c85525faa3742e48f8e331d7b9d72fd4a`.

No provider/model call was executed. The updated finding state is in [10 — Reconciliation after removal](10-reconciliation-after-lifecycle-removal.md).
