# 09 — Reconciliation with the current `HEAD`

Reconciliation date: 2026-08-06

Status: **29 findings open; 0 partial; 0 fixed**

Overall decision: **Not ready**

> This checkpoint was superseded by the [reconciliation after lifecycle enforcement removal](10-reconciliation-after-lifecycle-removal.md).

## Scope and classification rule

The original audit evaluated the checkout at `797d72cde47f7b94354af5ed49ede4eeb0ea5fdc`, with three local changes then pre-existing. This reconciliation compares every acceptance criterion from `TUX-AUD-001` to `TUX-AUD-029` with `HEAD` `b46f37643adfa83897427cb2be3c7f383f3b35d9`.

A finding was **fixed** only if its acceptance criterion was implemented and proven. **Partial** required a separable part of that criterion to already be satisfied. Related improvements, green reports, and new documentation receive no partial credit when the mechanism found by the audit remains unchanged.

Only eight files changed between the two commits:

```text
docs/architecture/evaluations.md
docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
docs/evidence/eval-runs.md
evals/promptfoo/assertions/workspace.py
evals/tasks/real-ambiguity.json
skills/git-commit/SKILL.md
skills/git-commit/agents/openai.yaml
tests/test_toolkit.py
```

The changes fixed `git-commit` routing, made an ambiguity oracle deterministic, and recorded new empirical evidence. They did not change hook launchers, receipt schema, staged-index binding, evaluation-system fingerprint, aggregate cardinality, eval-home isolation, legacy runner, security trajectory oracles, spec defaults, or the supply chain cited in the findings.

## New evidence, without extrapolation

An authorized `pnpm run eval:full` execution passed on 2026-08-06:

| Property | Evidence |
| --- | --- |
| Routing | 34/34 |
| Behavior | 40/40 |
| Security | 12/12 |
| Aggregate | 86/86; 0 falhas; status `pass` |
| Duration | 3,376.701 s (56m16.701s) |
| Controls | approval `never`; dedicated home; network/web/remote cache disabled; threads not persisted |
| Privacy | raw responses not saved; no sharing; no remote red-team |
| Artifact | `evals/promptfoo/results/full-aggregate-1786013868505052000.json` |
| SHA-256 | `e6916e05766d7450c45a462b9b6e7a455672fb3595d8a32c1cc9211b4cc23827` |

This result proves that the 86 configured cases passed under the current harness. It neither fixes nor invalidates findings about incomplete snapshot identity, permissive cardinality, or probe false negatives. Therefore, it is behavioral evidence for the configured catalog, not security certification or distribution readiness.

## State of each finding

| Finding | Current state | Reconciliation evidence |
| --- | --- | --- |
| `TUX-AUD-001` | Open | No canonical catalog spec/AC/matrix/evidence/review was added. |
| `TUX-AUD-002` | Open | `hooks/hooks.json` still starts the guard with `uv run` in the consumer cwd. |
| `TUX-AUD-003` | Open | The new `git-commit` trigger does not make the guard read or bind Git-index bytes. |
| `TUX-AUD-004` | Open | Policy still uses `exists()` without a robust `lstat`, type, and containment contract. |
| `TUX-AUD-005` | Open | Root fingerprint remains limited to `AGENTS.md` and `skills/**`; the new full run does not change that identity. |
| `TUX-AUD-006` | Open | The ambiguity change does not cover arbitrary external paths, egress through alternate executables, or transformed canaries. |
| `TUX-AUD-007` | Open | Eval home still accepts unknown top-level entries and does not reject symlinks recursively. |
| `TUX-AUD-008` | Open | Aggregate still does not compare the exact row set or reject missing/duplicate rows. |
| `TUX-AUD-009` | Open | `evals/run.py --execute` remains available, with inheritance/sanitization incompatible with the current path. |
| `TUX-AUD-010` | Open | Receipts remain global, without evidence mapping by criterion. |
| `TUX-AUD-011` | Open | No proof of cross-client installation and behavior was added. |
| `TUX-AUD-012` | Open | Codex onboarding still lacks a reproducible installation/materialization procedure. |
| `TUX-AUD-013` | Open | `premortem` and `technical-research` still lack `allow_implicit_invocation: false`. |
| `TUX-AUD-014` | Open | There is no canonical lifecycle, precedence, and fallback for skill composition. |
| `TUX-AUD-015` | Open | `premortem` may still recommend criteria/tests without explicit writing authority. |
| `TUX-AUD-016` | Open | Spec templates still induce `risk: small` and `single-isolated-reviewer`. |
| `TUX-AUD-017` | Open | Spec/matrix/evidence roles may still point to the same artifact. |
| `TUX-AUD-018` | Open | Test/code review receipt contexts are still incompletely validated. |
| `TUX-AUD-019` | Open | Default policy still makes co-located-test layouts unsatisfiable. |
| `TUX-AUD-020` | Open | Rules and documentation still promise more than the proven literal prefixes. |
| `TUX-AUD-021` | Open | Result validation still lacks complete schema/shape checks beyond file convention. |
| `TUX-AUD-022` | Open | Promptfoo resolves SDK 0.144.6 while the direct dependency is 0.146.0. |
| `TUX-AUD-023` | Open | Minimum Python is still not declared as an executable contract. |
| `TUX-AUD-024` | Open | Migration/provenance ledger remains ignored and tied to a personal path. |
| `TUX-AUD-025` | Open | `pnpm audit` still finds 5 high, 7 moderate, and 2 low; disposition/licenses remain pending. |
| `TUX-AUD-026` | Open | No collision strategy was created for generic cross-client names. |
| `TUX-AUD-027` | Open | Evidence map still does not record reproducible PDF provenance. |
| `TUX-AUD-028` | Open | Template copies still lack a canonical source and derivation check. |
| `TUX-AUD-029` | Open | `technical-research` still lacks a network, offline-mode, and fallback contract. |

## Next steps

The work packages remain pending. The recommended order remains:

1. `WP-01` to make the catalog contract independent of implementation.
2. `WP-02` through `WP-04` to fix the launcher, staged candidate, and fail-closed policy.
3. `WP-05` through `WP-08` to make eval identity, oracles, isolation, and aggregation reliable.
4. `WP-09` through `WP-11` for portability, supply chain, and provenance.
5. Repeat deterministic checks after each slice. A new full run adds useful evidence only after changes affecting the catalog/harness; repeating 86 calls is not needed for this documentation reconciliation.

## Three-phase review

### Spec

The `Not ready` decision follows from the audit's public criteria and claims, not from the implementation or full-run result. No acceptance criterion was reduced to accommodate the current state. The green full run was classified only within what it measures.

### Standards

All 29 states were compared individually with the original criteria. The classification avoids both false closure and “partial” without an independent acceptance unit. The report preserves the historical snapshot and adds this reconciliation as the current overlay.

### Risk

Dominant risks remain an unverified staged index, launcher side effects, incomplete identity/cardinality, and security/isolation false negatives. The main communication risk is confusing 86/86 with certification of these mechanisms; this reconciliation makes that limitation explicit.
