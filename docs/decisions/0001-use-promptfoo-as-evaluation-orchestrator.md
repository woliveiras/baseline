---
status: accepted
date: 2026-08-05
decision-makers:
  - William Oliveira
---

# Use Promptfoo as the evaluation orchestrator while retaining Baseline deterministic verifiers

## Context

Baseline needs controlled empirical evaluation of skill routing, behavior, and
security without maintaining generic provider orchestration or weakening
repository-specific checks. Promptfoo supplies provider execution, matrices,
and aggregation; it does not know Baseline's invariants.

The evaluation stack is development-only. It must not enter the distributed
plugin, run in the development checkout, inherit personal agent configuration,
share results remotely, or turn model judgment into proof of deterministic
behavior.

## Decision

Use Promptfoo for generic orchestration and the official Codex SDK provider.
Retain Baseline-owned fixtures, disposable workspaces, fingerprints, snapshots,
mutation policies, hidden executable checks, verdict semantics, and authority
boundaries.

Promptfoo owns:

- provider execution and condition matrices;
- local aggregation, latency, and token collection;
- generic assertions used by the configured local suites.

Baseline owns:

- canonical tasks and controlled fixtures;
- isolated control, core, focal, broad, current, and proposed workspaces;
- protected paths, snapshots, and deterministic behavior/security checks;
- frozen red-team probes and independent repetition policy;
- `pass`, `fail`, and `needs-review` precedence;
- sanitized report extraction and checkout-drift detection;
- privacy, cost, login, and external-operation authority.

A deterministic failure cannot be overridden by a semantic judge. Routing
metadata is a heuristic invocation signal, not proof of instruction adherence.
Red-team results apply only to the exact recorded task, fixture, provider, and
model conditions.

## Isolation and authentication

Provider execution requires a dedicated Codex home outside the checkout and
personal Codex state. The preflight accepts only explicit ChatGPT/Codex login,
rejects behavior-bearing configuration and symlinks, strips API-key fallbacks,
and creates no provider workspace before authentication succeeds.

Every writing trial and repetition starts from a fresh temporary Git workspace.
Every Promptfoo process receives disposable local state. Persisted reports are
sanitized and exclude prompts, raw responses, traces, credentials, and canaries.

## Dependency and authority boundary

Promptfoo and the Codex SDK remain exact, lockfile-constrained development
dependencies. They are not consumer dependencies. Dependency upgrades require
normal provenance, license, advisory, compatibility, and validation review.

### Transitive override policy

The reviewed PNPM overrides for `undici`, `sharp`, and `adm-zip` cross the
parent-declared range to avoid known vulnerable resolutions in optional or
development-only Promptfoo branches. The exception is narrow: when an upstream
parent declares and resolves a non-vulnerable child in its supported range,
remove the corresponding override, regenerate the lockfile, and repeat the
audit plus deterministic harness checks. Exact graph tests must accompany any
zero-advisory claim. Native lifecycle scripts remain disabled and unverified;
the overrides do not establish unused-provider or native-build compatibility.

Provider/model execution, login, red-team execution, and `eval:full` require
explicit human authority. Installation, ordinary validation, commit, and push
must never invoke them implicitly. A passing evaluation does not authorize Git
or release operations.

## Consequences

- Generic orchestration is maintained externally while Baseline preserves its
  stronger deterministic boundary.
- The adapter and isolation layers remain Baseline maintenance responsibilities.
- The legacy deterministic runner remains until a separately reviewed parity
  change proves that its unique comparison behavior can be removed.
- Current claims require fresh results from the current catalog and harness;
  superseded run logs remain in Git history rather than current documentation.

## Revisit triggers

Revisit this decision if Promptfoo or the Codex provider cannot preserve local
isolation, sanitized evidence, exact authority gates, deterministic precedence,
or the required task/fixture coverage; or if maintaining the adapter becomes
more expensive than a smaller controlled alternative.

See [evaluation architecture](../architecture/evaluations.md), [evaluation
isolation](../architecture/eval-isolation.md), and the [harness
guide](../guides/using-the-eval-harness.md) for the current executable contract.
