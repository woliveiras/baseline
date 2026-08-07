# 10 — Reconciliation after lifecycle enforcement removal

Date: 2026-08-06

State at `HEAD` `8776a6a`: **22 findings open; 7 closed by scope removal; 0 fixed by strengthening the mechanism**

Overall decision: **Not ready**

## Product change

The maintainer decided to validate the declarative workflow first on real tasks. `SPEC-0001`, ADR 0002, and commit `8776a6a` removed:

- `hooks/hooks.json` and the Python launcher `guard.py`;
- policy and completion-receipt templates;
- root and `verify` skill review-receipt JSON files;
- hook-specific fixtures and tests;
- lifecycle-enforcement capabilities and public claims.

`AGENTS.md` now declaratively requires an oracle before implementation, authorized scope, three reconstructed reviews, a task-owned staged candidate, and authorization before additional work. Codex Rules remain optional and limited to command authority. The installed product does not execute UV or Python in the consumer checkout.

## Status rule

“Closed by scope removal” means that the surface and its claim were removed. It does not mean that the previous mechanism was fixed or that the guarantee now exists in another layer. Remaining findings stay open until they satisfy their original criteria or are explicitly replaced by an equivalent product decision.

## Reconciled findings

| Finding | State | Current evidence |
| --- | --- | --- |
| `TUX-AUD-001` | Open, with progress | `SPEC-0001` proves the chain for this decision; the complete 17-skill catalog is not yet mapped. |
| `TUX-AUD-002` | Closed by scope removal | UV/Python launcher and the entire `hooks/` directory were removed. |
| `TUX-AUD-003` | Closed by scope removal | There is no longer a commit-gate claim; staged ownership is a declarative obligation. |
| `TUX-AUD-004` | Closed by scope removal | Policy and policy parser were removed. |
| `TUX-AUD-005` | Open | Evaluation-system fingerprint remains incomplete. |
| `TUX-AUD-006` | Open | Security trajectory oracles were not changed in this slice. |
| `TUX-AUD-007` | Open | Eval-home allowlist and symlink handling were not changed. |
| `TUX-AUD-008` | Open | Aggregate still does not prove the exact row set. |
| `TUX-AUD-009` | Open | Legacy runner remains available; only its workflow metadata was updated. |
| `TUX-AUD-010` | Closed by scope removal | Completion receipts were removed; SPEC-0001 links its own criteria directly to matrix/tests/evidence. |
| `TUX-AUD-011` | Open, with progress | Consumer runtime was removed, but cross-client installation/behavior remains unproven. |
| `TUX-AUD-012` | Open | Reproducible Codex onboarding was not implemented. |
| `TUX-AUD-013` | Open | Deep-work invocation policy did not change. |
| `TUX-AUD-014` | Open | Skill-composition lifecycle and precedence were not defined. |
| `TUX-AUD-015` | Open | Standalone `premortem` authority was not changed. |
| `TUX-AUD-016` | Open | Template classification/review defaults did not change. |
| `TUX-AUD-017` | Closed by scope removal | Completion-receipt roles and hashes were removed. |
| `TUX-AUD-018` | Closed by scope removal | Mechanical context validation was removed; reviews now declare context without an enforcement claim. |
| `TUX-AUD-019` | Closed by scope removal | Policy and its default tree scopes were removed. |
| `TUX-AUD-020` | Open | Rules-prefix limitations remain documented and unchanged. |
| `TUX-AUD-021` | Open | Result shape validation did not change. |
| `TUX-AUD-022` | Open | Direct/effective SDK divergence did not change. |
| `TUX-AUD-023` | Open | Maintainer-toolchain minimum Python is still not an executable contract. |
| `TUX-AUD-024` | Open | Migration/provenance ledger did not change. |
| `TUX-AUD-025` | Open | Supply-chain disposition was not performed. |
| `TUX-AUD-026` | Open | Cross-client collision strategy was not created. |
| `TUX-AUD-027` | Open | Reproducible PDF provenance did not change. |
| `TUX-AUD-028` | Open | Remaining templates still need an explicit canonical source. |
| `TUX-AUD-029` | Open | `technical-research` offline/network contract did not change. |

## Deterministic evidence

| Evidence | Result |
| --- | --- |
| SPEC-0001 fail-first tests | 3/3 failed at the expected boundaries before implementation |
| Focused tests after implementation | 3/3 passed |
| Unit suite | 63/63 passed; six hook tests removed and three declarative oracles added |
| Legacy dry-run | 48 runs; current fingerprint `4268cf00971d61b58c59fb31b133f61c85525faa3742e48f8e331d7b9d72fd4a` |
| Promptfoo config | valid |
| Official validators | valid plugin; 17/17 valid skills |
| Installed inventory | no `hooks/`, Python, UV project, policy, completion receipt, or review JSON |

## Empirical evidence

The previous 86/86 full run remains valid only for the snapshot in which it was executed. `AGENTS.md`, `verify`, `git-commit`, `ci-workflow`, and the fingerprint changed; no new model call was authorized by this decision. The real-task ledger is empty and will be filled in [declarative-workflow-trials.md](../../../evidence/declarative-workflow-trials.md).

## Next rational order

1. Execute 10–20 real tasks and record only observed failures of the declarative workflow.
2. Continue `WP-01` to cover the complete catalog, without recreating receipts.
3. Address `WP-05`–`WP-11` by priority; hook/policy/receipt-only items were removed.
4. Reconsider a hook only if a recurring failure has a narrow mechanical oracle and a solution without consumer runtime.

## Review

### Spec

SPEC-0001 preserves the user's objective: rigor of oracle, scope, review, commit, and authority without representing instructions as enforcement. No old criterion was weakened to declare a mechanism green; the mechanism was explicitly removed.

### Standards

The slice uses UV/PNPM only as maintainer toolchain, keeps Rules/tests/CI within their responsibilities, and records fail-first, passing evidence, and three reconstructed contexts. The audit history remains intact; this document is a later overlay.

### Risk

The accepted risk is the absence of mechanical blocking during the experiment. 22 unrelated or only partially benefited findings remain. The historical full run must not be presented as evidence for the new contract.
