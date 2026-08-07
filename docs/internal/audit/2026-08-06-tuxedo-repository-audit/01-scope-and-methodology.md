# 01 — Scope and methodology

## Scope, authority, and snapshot

The audit covered Tuxedo as a single distributable product: the engineering contract, plugin, 17 skills, Codex metadata, hooks, Rules, policies, receipts, templates, documentation, tests, the legacy harness, Promptfoo, ignored sanitized results, toolchain, dependencies, license, and provenance.

The audit respected the authority boundary limiting writes to the report. No pre-existing file was edited; no destructive command, commit, branch, push, login, or model call was executed. Temporary installations occurred only outside the checkout: an isolated interpreter received `PyYAML==6.0.2` for the official validators, as specified by `AGENTS.md:55-56`. Promptfoo state directories and probes were also created with `mktemp` outside the checkout.

The snapshot was:

- absolute checkout: `<absolute-tuxedo-checkout>` (local value omitted for portability);
- commit: `797d72cde47f7b94354af5ed49ede4eeb0ea5fdc`;
- branch: `main`;
- start: `2026-08-06T10:27:55+02:00`;
- pre-existing local state: three modified eval documents, as shown by the index;
- external-source lookup date: 2026-08-06.

## Three-phase method

### Phase 1 — intent without implementation

`AGENTS.md`, `README.md`, `docs/README.md`, architecture, ADR, development documentation, guide, research/evidence map, license, manifest, the contracts of all 17 skills, and the spec/review templates were read in full. Intent was reconstructed before hooks, tests, or the eval runner were used as justification.

Phase result: the central contract requires a durable chain, stable criteria, oracle provenance, isolated review phases, explicit authority for sensitive actions, and separation between portable content, Codex integration, and maintainer infrastructure. The catalog itself, however, does not provide a traced spec/AC/matrix; this was recorded before reading the implementation (`TUX-AUD-001`).

### Phase 2 — tests and evals without using the implementation as the oracle

Fixtures, assertions, tasks, rubrics, configurations, unit tests, sanitized results, and documentation of the eval design were evaluated. The families received the following classification:

| Family | Classification | Rationale |
| --- | --- | --- |
| Official validators | `external` | Official local implementation of the plugin/skill format. |
| Manifest/skill/template tests | `spec-derived` + `implementation-aware` | Derived from contracts, but many mirror the current shape and equality. |
| Hook tests | `spec-derived` + `implementation-aware` | Cover declared invariants; the helper repeats execution outside the consumer cwd. |
| Promptfoo routing | `spec-derived` + `implementation-aware` heuristic | Expected skill comes from the catalog; `skill-used`/`skillCalls` is a provider heuristic. |
| Mechanical behavior | `spec-derived` | AST, filesystem, and exit status do not depend on the final text. |
| Semantic behavior | `spec-derived` + `diagnostic-probe` | The rubric is declared, but the judge belongs to the same model family. |
| Security | `spec-derived` + `implementation-aware` + `diagnostic-probe` | Canary/trajectory and the canonical patch measure specific probes, not general security. |
| Ignored results | `external`/historical empirical | They are provider observations; without complete identity they do not prove the snapshot. |

The conceptual mutation-testing point was applied through safe counterexamples: a divergent staged index, broken policy symlink, future top-level entry in `CODEX_HOME`, nested symlink, `~/.ssh` path, encoded canary, and incomplete results matrix.

### Phase 3 — integrated comparison

Only after the previous phases were skills, `agents/openai.yaml`, hooks, Rules, receipts, tests, the legacy runner, the Promptfoo runner, the lockfile, and documentation compared. Each divergence was classified as a promise without a mechanism, a mechanism without a contract, a test without a requirement, a requirement without an oracle, or a claim stronger than the evidence.

## Inventory and explicit sampling

All 126 tracked files received a disposition in the [coverage ledger](02-inventory-and-coverage.md). Homogeneous families — agent YAML, JSON tasks, Promptfoo configs, duplicated templates, and the lockfile — were inventoried mechanically and reviewed by schema, consistency, and representative samples; this is indicated per file, without silent sampling.

Ignored results were handled separately. The independent checkpoint contained 127 valid JSON files, 1,618,535 bytes, with no duplicate content hash. They were aggregated by `suite/status/schema`, compared with the hashes cited in the documentation, and sampled by age, recency, suite, shard, aggregate, and focused run. An external concurrent `eval:full` execution continued creating reports after this checkpoint; the new files were inventoried at the end, but no result from that execution was used as audit evidence.

## Tools and versions

| Tool | Observed version |
| --- | --- |
| Git | `git version 2.50.1 (Apple Git-155)` |
| Node.js | `v26.3.1` |
| PNPM | `11.13.1` |
| UV | `0.9.5` |
| Python | `3.14.0` |
| zsh | `5.9` |
| bash | `5.3.9` |
| Codex CLI | `0.144.4` |
| Promptfoo | `0.122.0` |
| Poppler | local installation used for `pdfinfo`/`pdftotext` |

The versions above are the environment actually audited, not inferred minimum requirements. The repository declares Node `>=22.22.0` (`package.json:7-9`) and does not declare a minimum Python version (`TUX-AUD-023`).

## Primary external sources

Consulted on 2026-08-06:

- [Agent Skills specification](https://agentskills.io/specification) — `SKILL.md`, metadata, references, and assets contract.
- [OpenAI — Build skills](https://developers.openai.com/codex/skills/) — discovery, progressive disclosure, and name collisions.
- [OpenAI — Package plugins](https://developers.openai.com/plugins/build/plugins) — marketplace, installation, manifest, and restart.
- [OpenAI — Hooks](https://developers.openai.com/codex/hooks) — discovery, cwd, `PLUGIN_ROOT`, timeouts, and exit-code semantics.
- [OpenAI — Rules](https://developers.openai.com/codex/rules) — prefix matching and `codex execpolicy check`.
- [GitHub Copilot — Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), [OpenCode — Skills](https://opencode.ai/docs/skills), and [Claude — Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — cross-client surfaces.
- [Promptfoo — Assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/) — assertion shape and semantics.
- [UV — Running commands](https://docs.astral.sh/uv/concepts/projects/run/) — `uv run` syncs the project environment in cwd, the external basis for probe `TUX-AUD-002`.
- [PNPM settings](https://pnpm.io/settings) and [GitHub Advisory Database](https://github.com/advisories) — supply chain.
- [SPDX MIT](https://spdx.org/licenses/MIT.html) — license identifier and normative text.
- Primary evidence-map PDFs: [2604.01518](https://arxiv.org/pdf/2604.01518), [2607.05139](https://arxiv.org/pdf/2607.05139), [2602.07900](https://arxiv.org/pdf/2602.07900), [2602.20048](https://arxiv.org/pdf/2602.20048), and [2605.20049](https://arxiv.org/pdf/2605.20049).

## PDFs and context limitation

No attached PDF was accessible in the checkout, the visualization directory, or as a local attachment. To avoid turning absence into omission, the five IDs cited in `docs/research/evidence-map.md:9-13` were downloaded directly from arXiv to an external temporary directory, identified with `pdfinfo`, and extracted with `pdftotext`. The audit checked titles, versions, page counts, and the general connection to the claims, but does not treat this reconstruction as proof that the bytes are the same PDFs originally “supplied.” This limitation motivates `TUX-AUD-027`.

## Honest limitations

- No real provider, browser/network sandbox, auth, model judge, smoke, security, or red-team execution took place.
- The concurrent `eval:full` was not started, interrupted, or used by the audit.
- No legal audit was performed; the license analysis is engineering-focused and recommends review when necessary.
- The 792 dev entries in the lockfile were aggregated mechanically; no manual legal review of each transitive license was performed.
- Ignored/generated coverage is an inventory of the observed state, not a guarantee about files created after the audit ended.
- The audit does not prove cross-client behavior; it compares official layouts and contracts with the absence of local fixtures/executions.
