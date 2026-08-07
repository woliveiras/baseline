# Appendix — Traceability matrix

> This matrix preserves the original snapshot. The latest overlay is in [10 — Reconciliation after removal](10-reconciliation-after-lifecycle-removal.md); the intermediate checkpoint remains in [09](09-reconciliation-2026-08-06.md).

`—` means observed absence, not “out of scope.” Classification follows the Tuxedo contract.

| Contract/expectation | Test/eval/oracle | Implementation | Current evidence | Classification | Divergence/finding |
| --- | --- | --- | --- | --- | --- |
| Product is a portable toolkit without runtime | validators, structure tests | skills + manifest + hooks | validators pass | `external` + `spec-derived` | UV hook is consumer runtime: `002`; cross-client operation: `011`. |
| 17 skills distributed | manifest/catalog tests | `skills/*` | 17 validators pass | `external` | Conformant. |
| Concise `SKILL.md`, one-level refs | official validators + link check | 17 packages | all pass | `external` | Conformant; canonical copies `028`. |
| Deep work explicit-only | routing configs | `agents/openai.yaml` | configs validate | `spec-derived` | Premortem/research default implicit: `013`. |
| Authority does not expand | security/routing behavior | skill texts + AGENTS | historical behavior | mixed | Ambiguous standalone premortem: `015`; partial Rules: `020`. |
| Material change has spec and ACs | template/structure tests | templates, not actual artifact | — | `implementation-aware` | Catalog without spec: `001`. |
| AC → oracle → test → evidence | receipt unit tests | global fail/passing receipt | trivial fixture passes | `implementation-aware` | No AC mapping: `010`. |
| Three review phases | hook receipt tests | review templates + guard | unit tests pass | `spec-derived` | Incomplete test/code contexts: `018`. |
| Spec/matrix/evidence separate | hashes/path presence | guard roles | alias probe passes | `diagnostic-probe` | Roles may alias: `017`. |
| Risk tier by highest boundary | template/skill guidance | spec template | default `small` | guidance | Default bias: `016`. |
| Missing-policy hook is a no-op | missing hook fixture | `uv run` → guard | unit passes in wrong cwd | `implementation-aware` | `.venv`/lock created: `002`. |
| Malformed policy fails closed | malformed JSON fixture | exists/load_object | malformed JSON blocks | `spec-derived` | symlink/type/OSError do not: `004`. |
| Exact/stale tree detection | scope/stale tests | glob + hashes | unit passes | `spec-derived` | Impossible default overlap: `019`; residual races. |
| Commit gate protects reviewed slice | direct commit test | working-tree hashes | unit passes | `implementation-aware` | Staged index not read: `003`. |
| Rules protect external/destructive commands | `codex execpolicy check` | prefix rules | seven cases pass | `external` | Wrappers/options uncovered: `020`. |
| Routing covers catalog | 34 Promptfoo cases | routing assertion | historical reports | `spec-derived` + heuristic | Explicit Codex only; names/clients `011`,`026`. |
| Behavior covers configured tasks | 40 target + judges | AST/workspace assertions | historical aggregates | `spec-derived` | Only 7/17; docs are honest. |
| Security frozen probes detect named attack | 12 probes | security/trajectory assertion | historical 12/12 | diagnostic | False negatives `006`. |
| Dedicated home rejects unknown content | unit configs/known paths | `codex_auth.py` | tests pass | `spec-derived` | Unknown/nested symlink accepted: `007`. |
| API keys are not fallback | env filtering tests/current runner | Promptfoo env | static review | `spec-derived` | Legacy execute inherits env: `009`. |
| Raw prompts/output do not persist | sanitized report builder | current runner | samples sanitized | `implementation-aware` | Legacy writes raw: `009`; shape only suffix: `021`. |
| Full covers 34/40/12 | config range tests | aggregate sums rows | docs count matches | `spec-derived` | Missing/duplicate passes: `008`. |
| Evidence matches snapshot | report fingerprint | AGENTS+skills hash | same hash across harness changes | `implementation-aware` | Incomplete identity: `005`. |
| Fresh evidence after upgrades | docs policy | manual evidence log | green full pre-change | external historical | `005`. |
| Failed shard persists checkpoint | runner unit/static review | sanitized checkpoint | result families present | `implementation-aware` | Conformant on current path. |
| Git unchanged after full | before/after status | runner | historically declared | `diagnostic-probe` | By design, does not identify untracked/ignored evidence as product change. |
| Toolchain declared | docs + version commands | package/UV imports | current env passes | external | Missing minimum Python `023`; SDK mismatch `022`. |
| Dev-only dependencies not distributed | grep/package manifest | package.json/lockfile | confirmed | `external` | advisories/licenses `025`. |
| Clear MIT/provenance | license text/manifest/readme | LICENSE | consistent | external/SPDX | Ignored ledger `024`; paper metadata `027`. |
| Sufficient README onboarding | link/manual walk-through | README | not reproducible | diagnostic | `012`. |
| Templates represent common/blocked/authorized | hook tests + manual scenarios | policy/receipts/reviews | normal/stale covered | `spec-derived` | co-location/context/alias gaps `017`–`019`. |
| Skill composition terminates | — | informal cross-references | — | — | lifecycle/deadlock `014`. |
| Current research is reproducible | evidence map bibliography | technical-research skill | PDFs reconstructed | external + diagnostic | metadata/method `027`; offline compatibility `029`. |

## Gaps in both directions

### Promise without sufficient implementation

- “Commit gate” without staged index.
- “Fail-closed” without unknown surfaces, symlinks, and filesystem errors.
- “34/40/12” without an expected-row set.
- “Steganographic exfiltration” with literal search.
- “Portable” without cross-client installation/behavior.

### Implementation without canonical contract

- Specific receipt/digest/glob algorithms have no versioned AC.
- Sanitized report schema and aggregate shape have no formal schema.
- Current eval-home allowlist has no surface/version-compatibility matrix.
- Policy and Rules defaults have no declared support scenario.

### Test without independent requirement

- Byte-for-byte template equality preserves current state, but does not choose a canonical source.
- Digest/receipt helpers repeat implementation without an independent oracle.
- Shard range tests do not require raw rows to materialize the range.

### Requirement without test

- Staged commit candidate.
- Real hook cwd/zero filesystem side effect.
- Unknown eval-home top-level/nested symlink.
- AC-by-AC receipt mapping.
- Composition state machine and fallback.
- Cross-client discovery/collision.
