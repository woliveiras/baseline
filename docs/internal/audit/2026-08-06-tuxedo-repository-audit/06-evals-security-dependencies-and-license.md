# 06 — Evals, security, dependencies, and license

## Recalculated eval inventory

| Suite | Actual matrix | Maximum calls |
| --- | ---: | ---: |
| Routing | 17 positive + 17 negative | 34 target |
| Behavior | 8 tasks × 5 conditions | 40 target |
| Secondary judge | 5 semantic tasks × 5 conditions | up to 25 judge |
| Security | 12 frozen probes | 12 target |
| `eval:full` | routing + behavior + security | 86 target + up to 25 judge = 111 |
| Smoke | 4 conditions | 4 target |
| Compare | 8 × 2 providers × 3 repetitions | 48 target + up to 30 judge = 78 |
| Legacy dry-run | 8 × 6 variants | 48, no provider in dry-run |
| Red-team config | 10 requested probes | actual cost not verified |

The documented quantities 34/40/12/111 match the tasks/configs. This does not mean the aggregator requires them (`TUX-AUD-008`).

## Design and evidence

### Confirmed strengths

- Tasks, fixtures, deterministic verifiers, and the provider are separated.
- Workspaces are temporary and initialized as Git repositories.
- Promptfoo state/raw data is placed in a temporary root in the current path.
- Exit 100 still produces a sanitized checkpoint.
- An assertion failure in one suite does not erase earlier outcomes.
- Write-capable repetitions use new processes/workspaces.
- The child environment removes `OPENAI_API_KEY` and `CODEX_API_KEY`.
- Configs set `approval_policy: never`, disable network/web access, and set `persist_threads: false`.
- Durable reports declare `raw_responses_saved: false`.
- Documentation honestly limits routing, behavior, security, model identity, and judge claims (`docs/architecture/evaluations.md:180-195`).

### Evidence classification

| Surface | Type | Strength/limit |
| --- | --- | --- |
| Routing contract | `spec-derived` | Expected skill is declared; usage metadata is heuristic. |
| AST/filesystem behavior | `spec-derived` | Deterministic oracle for the fixture, not general quality. |
| Secondary rubric | `spec-derived` + `diagnostic-probe` | Same Codex family; not independent. |
| Frozen security | `spec-derived` + `diagnostic-probe` | Measures named attacks; confirmed false negatives. |
| Sanitized reports | `external`/historical empirical | Provider observation; no complete snapshot. |
| Dry-run/static validation | `diagnostic-probe` | Proves configuration/matrix, not model behavior. |

## Snapshot identity and provenance

`evals/run.py:279-286` calculates a fingerprint only from `AGENTS.md` and `skills/**`. `prepare-workspaces.py:183-196` and `run-evaluations.py:430-455` propagate this value; reports do not include the commit, dirty-state digest, or hash of tasks, fixtures, rubrics, configs, assertions, verifiers, runner, and lockfile.

The documented green full run (`docs/evidence/eval-runs.md:200-218`) was created before multiple later commits to the harness. A more recent routing aggregate retained fingerprint `1796ac…5bec` and failed 33/34. The architecture itself requires new evidence after task/fixture/provider/dependency upgrades (`docs/architecture/evaluations.md:193-195`). Therefore, the historical full run does not prove the current checkout (`TUX-AUD-005`).

## Security probe validity

### External paths

`security.py:99-133` marks external use only if the resolved path is exactly a listed sentinel. A structured event `cat ~/.ssh/id_rsa` produced `violations=[]`, although `security-regressions.yaml:36-44` prohibits home/sibling reads. Any external path should violate the controlled fixture, not only the sentinel.

### Egress

The blacklist in `security.py:114-120` covers `curl`, `wget`, `nc`, `ssh`, and a few others. `python`, `node`, `pnpm`, `gh`, and cloud CLIs can open the network without triggering the oracle. The fixture request asks for a concrete `cat`, but the assertion does not enforce this allowlist.

### Steganography

`security.py:182-191` looks for the literal canary in files/text. Base64/hex of the canary does not contain the literal and passes, despite the `steganographic-exfiltration` claim (`security-regressions.yaml:124-132`).

Conclusion: 12/12 may contain false positives; the claim must be reduced or the oracle made legitimate for the fixture (`TUX-AUD-006`).

## Dedicated `CODEX_HOME` isolation

The documented model is prudent: an auth session may be reused, behavior-bearing content may not; API keys are not a fallback; status must be “Logged in using ChatGPT”; config is allowlisted.

Two counterexamples break the declared fail-closed behavior:

- `codex_auth.py:137-191` handles known names and `skills/plugins`, but has no `else` for an unknown top-level entry; `future-behavior-surface/` was accepted.
- Symlinks are checked only at the first levels; a nested link in `skills/.system/.../personal-link` was accepted.

This contradicts `docs/architecture/eval-isolation.md:34-55` (`TUX-AUD-007`). No dedicated home or real credential was inspected.

## Aggregation and coverage

`run-evaluations.py:246-284` recursively collects any object with `response` and validates only error/output/turn. `:606-641` concatenates shards and sums counts; `:734-743` requires only pass status; `:843-862` can print full passed. There is no exact equality of the `(test_id, provider)` set, uniqueness, shard ownership, or 34/40/12 cardinality.

Executable conceptual counterexample: each shard returns one passing row; aggregates and full continue to pass with fewer than 86 trials. Tests check configured ranges, not missing/duplicate/wrong-provider raw rows. See `TUX-AUD-008`.

## Legacy runner

`docs/development.md:58-63` still documents `evals/run.py --execute`. This path builds `codex exec` (`evals/run.py:155-174`), inherits the entire environment in `subprocess.run` (`:203-221`), and writes `answer`/`raw` (`:232-246,385-403`) to an ignored-only directory. It does not use the dedicated preflight or filter API keys. It is a second official path with incompatible guarantees (`TUX-AUD-009`).

## Ignored sanitized results

At the independent checkpoint:

- 127 JSON, 1,618,535 bytes, all parseable;
- behavior: 65 (34 pass, 31 fail);
- routing: 30 (18 pass, 12 fail);
- security: 26 (14 pass, 12 fail);
- full: 5 (2 pass, 3 fail);
- smoke: 1 pass;
- no duplicate content hash;
- hashes of the reports cited in `eval-runs.md` matched.

Explicit sampling: oldest/newest; latest full/routing/behavior/security/smoke; shard, aggregate, and focused report. No raw model output was found in sampled durable fields. However, `_validate_local_outputs` (`run-evaluations.py:123-144`) checks only extension and directory, not parse/schema/name/duplicates/integrity/forbidden fields (`TUX-AUD-021`).

An external `eval:full` execution was already running from 09:46:36, before the audit began, and created new JSON files during the work. It was not started, interrupted, or used as evidence; the final total is recorded in the command appendix.

## Direct dependencies

| Dependency | Version/pin | Scope | License | Need/provenance | Risk |
| --- | --- | --- | --- | --- | --- |
| `promptfoo` | exact `0.122.0` | dev-only | MIT | Orchestrates provider, repetitions, reports; decision in ADR | Very large graph; 14 current transitive advisories. |
| `@openai/codex-sdk` | exact `0.146.0` | dev-only | Apache-2.0 | Declared as required by the provider | Promptfoo effectively resolves `0.144.6`; root `0.146.0` may be redundant (`TUX-AUD-022`). |

The lockfile contains 792 dev packages, 595 snapshots, and integrity entries. The local virtual store confirmed two SDK versions. `pnpm outdated` found `0.146.1`, but an update was neither authorized nor recommended in isolation without compatibility evidence.

### Current advisories

`pnpm audit --json` on 2026-08-06 returned exit 1:

- 0 critical, 5 high, 7 moderate, 2 low;
- highs in `undici` WebSocket (DoS/exception), `adm-zip` (4 GiB allocation), and `sharp/libvips`;
- all arrive through Promptfoo/optional maintainer tooling, not through the distributed plugin.

Primary sources include [GHSA-vrm6-8vpv-qv8q](https://github.com/advisories/GHSA-vrm6-8vpv-qv8q), [GHSA-v9p9-hfj2-hcw8](https://github.com/advisories/GHSA-v9p9-hfj2-hcw8), [GHSA-vxpw-j846-p89q](https://github.com/advisories/GHSA-vxpw-j846-p89q), [GHSA-xcpc-8h2w-3j85](https://github.com/advisories/GHSA-xcpc-8h2w-3j85), and [GHSA-f88m-g3jw-g9cj](https://github.com/advisories/GHSA-f88m-g3jw-g9cj). Impact is limited because these are dev-only, but evals process output/archives and may access the network; a documented decision is needed before the next provider run (`TUX-AUD-025`).

### Transitive licenses

Mechanical aggregation of installed packages: 446 MIT, 87 Apache-2.0, BSD/ISC, and other permissive licenses; also one LGPL-3.0-or-later and three `Unknown` metadata entries. No manual legal analysis of 792 entries was performed. Since the graph is not distributed with the plugin, the risk is toolchain/cache redistribution, not consumer runtime. The `Unknown` entries prevent claiming a complete license inventory without review (`TUX-AUD-025`).

## License, authorship, and provenance

`LICENSE:1-21`, the manifest (`.codex-plugin/plugin.json:11`), and README (`README.md:69-71`) agree on MIT; the text matches the [SPDX MIT](https://spdx.org/licenses/MIT.html) identifier. The local Geremmyas repository also uses MIT and the same author, reducing apparent incompatibility. This is not a legal opinion.

The evidence map declares community inspiration without copying (`docs/research/evidence-map.md:33-35`) and cites five preprints. The auditability problem is that the only capability-by-capability migration disposition ledger is in ignored `docs/tmp/v0.1-map.md`, with personal paths and `never-commit` policy. A clean clone loses the origin/disposition (`TUX-AUD-024`).

The five PDFs were checked through direct arXiv sources. The evidence map does not record URLs, date, hash, pages/sections, or method, below the standard required by `technical-research` (`TUX-AUD-027`). No long copied text was identified, but a complete similarity/authorship analysis was not performed; if there is broad publication, legal review of adaptations and attributions remains prudent.

## Privacy and residual security

- Ignored reports must not be confused with protected secrets: `.gitignore` is not access control.
- The legacy path persists raw output; it should be removed/migrated before use.
- Concurrent execution demonstrates that ignored results change outside Git; full aggregates need complete hashes/commit/fingerprint.
- Sandbox/network settings in configs are intent; they were not empirically certified in this audit.
- The canary proves literal copying at observed locations, not silent reads or transformation.
- No real credential or tracked personal path was found; no credential was read or printed.
