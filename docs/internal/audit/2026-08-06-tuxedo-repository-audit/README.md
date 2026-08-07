# Full audit of the Tuxedo repository

Audit date: 2026-08-06

Status: **complete for the audited local snapshot, with explicit empirical limitations**

Overall decision: **Not ready**

Most recent reconciliation: `HEAD` `8776a6a`; **22 findings open and 7 closed by scope removal**. See [the reconciliation after lifecycle enforcement removal](10-reconciliation-after-lifecycle-removal.md). The [previous reconciliation](09-reconciliation-2026-08-06.md) and the snapshot below remain as historical records.

## Index

1. [Scope and methodology](01-scope-and-methodology.md)
2. [Inventory and coverage ledger](02-inventory-and-coverage.md)
3. [Product, architecture, and contracts](03-product-architecture-and-contracts.md)
4. [Skills, agents, and documentation](04-skills-agents-and-documentation.md)
5. [Hooks, Rules, templates, and tests](05-hooks-rules-templates-and-tests.md)
6. [Evals, security, dependencies, and license](06-evals-security-dependencies-and-license.md)
7. [Findings](07-findings.md)
8. [Remediation work packages](08-remediation-work-packages.md)
9. [Traceability matrix](appendix-traceability-matrix.md)
10. [Command evidence](appendix-command-evidence.md)
11. [Reconciliation with the current HEAD](09-reconciliation-2026-08-06.md)
12. [Reconciliation after lifecycle enforcement removal](10-reconciliation-after-lifecycle-removal.md)

## Audited snapshot

| Field | Value |
| --- | --- |
| Checkout | `<absolute-tuxedo-checkout>` (local value omitted for portability) |
| Commit | `797d72cde47f7b94354af5ed49ede4eeb0ea5fdc` |
| Branch | `main` |
| Start | `2026-08-06T10:27:55+02:00` |
| Tracked files | 126 files, 16,387 lines |
| Skills | 17 |
| Initial Git state | three pre-existing modifications, listed below |

Pre-existing modifications, preserved and not attributed to the audit:

```text
 M docs/architecture/evaluations.md
 M docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
 M docs/evidence/eval-runs.md
```

The audit subject was the real checkout — the commit plus these local modifications — rather than an abstraction of a clean `HEAD`.

## Executive conclusion

Tuxedo has a clear proposal and an unusually disciplined foundation: the distributed content is small and client-neutral, with no accidental runtime; the 17 skills are concise; authority boundaries are explicit; and deterministic tests, validators, dry-run checks, and static validations pass. The documentation also correctly distinguishes behavioral evidence from runtime certification.

However, the system is not ready for responsible distribution under its current guarantees. The fidelity chain that the product requires from third parties does not exist as a durable artifact for the catalog itself. Two critical gates do not bind the fact their names imply: the hook may modify the consumer project on startup, and the commit receipt validates the working tree rather than staged bytes. In addition, historical green evidence does not identify the complete harness; security probes have deterministic false negatives; isolation accepts unknown surfaces; and the aggregator may approve an incomplete matrix. Therefore, “mechanically verified” and “current stack green” are claims stronger than the implementation supports.

## Finding count

| Severidade | Quantidade |
| --- | ---: |
| P0 — Critical | 0 |
| P1 — High | 10 |
| P2 — Medium | 16 |
| P3 — Low | 3 |
| **Total** | **29** |

## Five dominant risks

1. A receipt can approve working-tree content while different content is already staged for commit (`TUX-AUD-003`).
2. A hook launcher executed in the session cwd can create `.venv` and `uv.lock` in the consumer repository, violating the “no runtime dependency” contract (`TUX-AUD-002`).
3. Old eval results retain the same fingerprint after changes to tasks, assertions, the runner, or dependencies (`TUX-AUD-005`).
4. Security probes may allow reads from `~/.ssh`, egress through executables outside the blacklist, and encoded exfiltration (`TUX-AUD-006`).
5. The catalog has no durable spec, criteria, and matrix from which intent can be reconstructed without reading the implementation itself (`TUX-AUD-001`).

## Readiness by dimension

| Dimension | Decision | Main reason |
| --- | --- | --- |
| Product | Ready with conditions | Clear proposal and scope; the catalog lacks a traceable contract. |
| Distribution | Not ready | Installation is not reproducible and the hook may mutate the consumer. |
| Documentation | Ready with conditions | Clear and honest, but onboarding, composition, and provenance have gaps. |
| Tests | Ready with conditions | 65/65 pass; oracles do not cover the staged index, host cwd, or several bypasses. |
| Evals | Not ready | Fingerprint, isolation, cardinality, and probes invalidate the current green claim. |
| Security | Not ready | Confirmed false negatives and a legacy path inherit the personal environment. |
| Maintenance | Not ready | There is no spec → criteria → evidence chain for the product itself. |
| Portability | Ready with conditions | Portable format; installation and cross-client behavior are unproven. |

## Checks in one line

Passed: the official plugin validator; official validators for all 17 skills; 65 unit tests; the legacy dry-run with 48 runs; six Promptfoo configurations; valid JSON/YAML except for the deliberately malformed fixture; AST checks for 13 Python scripts; links/anchors for 65 Markdown documents including the report; `git diff --check`; and whitespace checks for the 11 new files. No shell script was tracked. `pnpm audit` returned 14 advisories (5 high, 7 moderate, 2 low), and `pnpm outdated` found one SDK patch update. Details, duration, limits, and exit codes are in the [command appendix](appendix-command-evidence.md).

Login, `eval:full`, provider/model calls, a real red-team, deployment, publication, and any external Git action were not executed. An `eval:full` execution started by another process before this audit was observed and explicitly excluded from the evidence.

Later, an authorized execution passed 86/86 in 56m16.701s. This evidence is reconciled without extrapolation in [09](09-reconciliation-2026-08-06.md): it proves the configured cases, but does not close the findings about harness validity and completeness.

## Recommended order

Start with `WP-01` (catalog contract), while `WP-02` (hook launcher), `WP-03` (staged-index binding), and `WP-04` (fail-closed policy) proceed in parallel. Then execute `WP-05` through `WP-08` to correct eval validity and isolation. Only then produce new authorized empirical evidence. The complete sequence is in [work packages](08-remediation-work-packages.md).

No pre-existing code, skill, test, template, configuration, spec, or documentation was corrected by this audit. The only authorized writes are the files in this report directory.
