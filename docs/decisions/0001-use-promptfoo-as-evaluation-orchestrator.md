---
status: accepted
date: 2026-08-05
decision-makers:
  - William Oliveira
---

# Use Promptfoo as the evaluation orchestrator while retaining Tuxedo deterministic verifiers

## Context and Problem Statement

Tuxedo needs empirical evidence that its skills, contracts, routing boundaries, and guardrails produce the intended behaviors. The existing `evals/run.py` runner already provides a Tuxedo-specific execution model: a canonical task catalog, controlled fixtures, baseline/core/focal/broad/current/proposed conditions, repetitions, seeded ordering, results, fingerprints, snapshots, mutation policies, process checks, and hidden deterministic oracles.

Keeping all generic evaluation infrastructure in Tuxedo increases maintenance cost. Promptfoo provides maintained providers for Codex, side-by-side Agent Skill comparisons, assertions, repetitions, result aggregation, reporting, and coding-agent red teaming. Promptfoo does not know Tuxedo's invariants. Replacing deterministic verifiers with LLM judges would reduce the strength of evidence, and a direct chat provider would not represent a coding-agent trajectory.

We need an explicit responsibility boundary between generic evaluation orchestration and Tuxedo-specific evidence. The evaluation system must remain maintainer-only, must use an isolated Codex home, must not run in the Tuxedo checkout, and must not silently share evaluation content with Promptfoo Cloud or other remote generation services.

## Decision Drivers

- Reduce maintenance of generic scheduling, provider integration, repetition, and reporting infrastructure.
- Preserve hidden deterministic oracles and their precedence over secondary judgments.
- Preserve disposable workspace isolation, snapshots, fingerprints, and mutation policy.
- Evaluate positive and negative routing boundaries, not only final response text.
- Test security through trajectory, command, file, and artifact evidence in addition to final output.
- Keep results reproducible and auditable with fixed model, reasoning, seed, versions, and conditions.
- Keep Promptfoo and Node.js out of the distributed plugin runtime.
- Keep skills portable and client-neutral while using Codex as the initial evaluation client.
- Avoid remote generation and silent result sharing.
- Support baseline/current/proposed comparisons with distinct fingerprints.
- Keep cost, duration, and variance observable.

## Considered Options

### Continue maintaining the complete custom Tuxedo runner

- Good, because Tuxedo retains complete control and adds no Node dependency.
- Good, because the current behavior is known and already covers Tuxedo-specific invariants.
- Bad, because Tuxedo must maintain scheduling, providers, reports, routing assertions, and red teaming.
- Bad, because it replicates capabilities maintained by a project specialized in evaluations.
- Bad, because security coverage remains limited by maintainer time.

### Replace the Tuxedo runner and verifiers completely with Promptfoo

- Good, because it appears to reduce the amount of Tuxedo-owned code.
- Good, because configuration and reporting would be centralized in Promptfoo.
- Bad, because Tuxedo would lose or weaken hidden oracles specific to its contracts.
- Bad, because executable behavior could be replaced by textual judgment.
- Bad, because current fingerprint, snapshot, and mutation-policy controls would be lost.
- Bad, because Tuxedo would become excessively coupled to one framework's semantics.

### Use Promptfoo for orchestration while retaining Tuxedo deterministic components

- Good, because responsibilities are separated clearly.
- Good, because the existing Tuxedo evidence investment is reused.
- Good, because routing, reports, repetitions, and red teaming use maintained Promptfoo capabilities.
- Good, because deterministic results retain precedence over secondary scores.
- Good, because the migration is incremental and reversible.
- Bad, because adapters are required at the boundary.
- Bad, because `evals/run.py` and Promptfoo overlap temporarily.
- Bad, because the boundary must be tested to prevent future duplication.

### Use DeepEval with a custom Codex CLI adapter

- Good, because DeepEval integrates naturally with Python and pytest.
- Good, because its metric and custom-metric model is extensible.
- Bad, because it does not provide the same direct Codex and Agent Skills integration.
- Bad, because Tuxedo would need to implement trajectory, routing, and workspace integration.
- Bad, because a substantial part of the orchestration we want to retire would remain Tuxedo-owned.

## Decision Outcome

Use Promptfoo for orchestration while retaining Tuxedo deterministic components.

Promptfoo is responsible for:

- Codex execution through the official `openai:codex-sdk` provider;
- provider and condition matrices;
- repetitions and seeded comparison runs;
- routing assertions, including heuristic `skill-used` and `not-skill-used` signals;
- token and latency collection;
- local result aggregation and presentation;
- generic assertions;
- coding-agent red teaming and local reports.

Tuxedo remains responsible for:

- the canonical dataset in `evals/tasks/`;
- controlled fixtures and disposable workspaces;
- baseline/core/focal/broad/current/proposed variants;
- distinct root fingerprints and rejection of identical proposed roots;
- file snapshots and mutation policy;
- protected-file hashes;
- hidden deterministic oracles and AST verifiers;
- failure semantics, including `pass`, `fail`, and `needs-review`;
- deterministic precedence over secondary judgments;
- authority, privacy, and no-external-operation boundaries.

`evals/run.py` remains temporarily. Promptfoo is introduced through adapters, and removal or reduction of the old orchestration is a separate change that requires demonstrated parity for fixture materialization, variants, fingerprints, hidden oracles, timeouts, JSON results, and no-op rejection. No LLM judge may turn a deterministic failure into a pass. `skill-used` is a heuristic signal of skill-file reading or invocation, not proof of skill obedience. Promptfoo red teaming does not prove universal security; results apply only to the recorded versions, tasks, models, and conditions.

### Dependency decision

The maintainer tooling uses exact versions resolved on 2026-08-05:

- `promptfoo@0.122.0`, MIT, published and maintained through the official Promptfoo repository and npm package. It is preferred to expanding the custom runner because it supplies the generic provider, assertion, comparison, repetition, reporting, and coding-agent red-team surfaces already required here.
- `@openai/codex-sdk@0.146.0`, Apache-2.0, published and maintained through the official OpenAI Codex repository and npm package. It is required by the official Promptfoo Codex provider and matches the locally installed Codex CLI family.

The effective package engine requirements are Node `>=22.22.0` for Promptfoo and Node `>=18` for the Codex SDK; the maintainer package uses the stricter Promptfoo requirement. The PNPM lockfile is committed to constrain transitive resolution. The repository sets PNPM `minimumReleaseAge: 0` so an ambient machine-wide release-age policy cannot make this exact, reviewed lockfile un-installable; it does not relax exact versioning, audit, or upgrade review. A local `pnpm audit --prod` on 2026-08-05 found no production dependencies; the full `pnpm audit` reported 14 dev/optional advisory entries (two low, seven moderate, and five high), including `undici` and AI SDK packages. No automatic remediation was applied because changing the locked graph would require a separate reviewed upgrade. Supply-chain risks remain: both packages execute local Node tooling, Promptfoo has a broad transitive graph, and provider behavior can change across upgrades. Mitigations are exact versions, a committed lockfile, local-only result paths, disabled cache and remote red-team generation, no cloud login, isolated disposable workspaces, no production credentials in fixtures, and review of upgrades. Tuxedo still owns the distributed plugin contract, skill portability, deterministic evidence, and authority boundaries; Promptfoo is not a runtime dependency of the plugin.

## Consequences

### Good, because...

- Tuxedo owns less generic orchestration code.
- Codex providers are maintained externally while using the local Codex authentication boundary.
- Routing assertions, comparisons, repetitions, and local reports are standardized.
- Coding-agent red-team coverage can grow without becoming a second Tuxedo framework.
- Existing hidden oracles and controlled fixtures are reused.
- Generic infrastructure and Tuxedo domain knowledge have an explicit boundary.

### Bad, because...

- Node.js, Promptfoo, and the Codex SDK become maintainer dependencies.
- Promptfoo and Codex SDK upgrades may require adapter changes.
- Provider event and result formats may change.
- Workspace and verifier integration still requires Tuxedo-specific code.
- Codex evals consume time and quota.
- Red teaming can produce false positives and grader-dependent results.
- Remote-generation controls must remain explicit to protect privacy.

### Neutral, because...

- Plugin users do not need Promptfoo installed.
- Distributed skill content remains client-neutral.
- Codex is the first evaluation client, not a conceptual dependency of the skills.
- Hooks continue to be tested deterministically.
- This decision grants no authority for push, publication, release, deployment, or remote services.

## Confirmation

This decision is implemented when the following checks are evidenced:

- [x] Promptfoo and the Codex SDK are exact development dependencies.
- [ ] The official Codex provider works with an isolated, authenticated `TUXEDO_EVAL_CODEX_HOME`.
- [x] Canonical tasks and `evals/verifiers.py` are reused through adapters.
- [x] Baseline/current/proposed comparisons reject identical fingerprints.
- [x] Every write-capable trial uses a fresh disposable workspace.
- [x] Positive and negative routing cases exist for every distributed skill.
- [ ] Approved frozen security probes run locally without remote generation.
- [ ] `pnpm run eval:full` fails for provider, deterministic, routing, security, incomplete-turn, and result-validation failures.
- [x] Empty processes cannot produce a pass and deterministic failures take precedence.
- [ ] Red-team generation is not part of `eval:full`.
- [x] Results, caches, workspaces, and evaluation Codex homes remain ignored.
- [x] README and architecture documentation discover this ADR.
- [ ] Parity with the existing runner is recorded before any reduction of `evals/run.py`.

The security catalog gives every probe a distinct fixture stimulus and a
legitimate deterministic target-change oracle; trajectory checks inspect only
structured Codex command/file events and return `needs-review` when that schema
is absent. Dated deterministic, dependency-audit, and provider run evidence for
this decision is recorded in [the run log](../evidence/eval-runs.md).

## Amendment: dedicated Codex CLI authentication

On 2026-08-05, the maintainer evaluation boundary was amended to reuse a
ChatGPT/Codex account session without reusing the personal Codex environment.
The default home is `$HOME/.codex-tuxedo-evals`; `TUXEDO_EVAL_CODEX_HOME` may
override it only with an absolute path outside this checkout and outside the
personal `CODEX_HOME`/`$HOME/.codex`, after symlink resolution. The explicit
`pnpm run eval:login` command creates that dedicated directory when necessary
and runs `codex login`; `pnpm run eval:auth:status` and every model-running
preflight use `codex login status`. No command reads, copies, prints, or
symlinks `auth.json`, and neither `OPENAI_API_KEY` nor `CODEX_API_KEY` can
satisfy or silently replace the dedicated login. The preflight accepts only
the status label `Logged in using ChatGPT`; API-key, agent-identity, ambiguous,
and failed statuses are rejected, so a successful exit code alone is not
treated as proof of the selected account-based method.

Authentication reuse and content isolation are separate guarantees. Codex may
create authentication, minimal configuration, logs, history, sessions, state
databases, and shell snapshots in the dedicated home. Codex-managed
`skills/.system`, `plugins/cache/openai-curated-remote`, and an empty
`plugins/.remote-plugin-install-staging` are also allowed because the CLI may
materialize them during normal operation. Personal or unknown skill/plugin
namespaces, `memories`, `rules`, instruction files, and MCP configuration are
rejected because they can change evaluated behavior. Tuxedo parses
`config.toml` fail-closed: `cli_auth_credentials_store` and Codex project
`trust_level` metadata are allowed; hooks, profiles, model/model_provider(s),
MCP, instruction, policy, unknown top-level settings, and other project
metadata are rejected. This small allowlist recognizes the current
CLI-managed surfaces; future surfaces fail closed, and the curated plugin
cache is trusted only as Codex-managed operational content. Tuxedo does not
validate the semantics of that allowed auth-store value, so keeping the file
minimal remains a maintainer responsibility; an unrecognized future status
label also fails closed.
Allowed managed entries are required to be real directories/files rather than
symlinks, so a personal target cannot hide behind an allowed name.

The provider configurations intentionally omit a fixed `model`: the Codex CLI
selects a model supported by the authenticated ChatGPT/Codex account. Reports
record this as `codex-cli-default`; adding a model pin requires a fresh
compatibility check against the selected authentication method.

Amendment evidence:

- [x] Default and override home resolution reject relative, personal,
  checkout, and unsafe symlink paths.
- [x] Login creates only the dedicated home and passes it as `CODEX_HOME` to
  the configured Codex executable.
- [x] Status and evaluation preflight use `codex login status`, isolate both
  API-key environment variables, require the reported ChatGPT method, and fail
  before disposable workspaces.
- [x] All six provider configurations receive the resolved home through
  `cli_env.CODEX_HOME`.
- [x] Deterministic tests cover status success/failure, missing home,
  operational state, behavior-bearing content rejection, secret redaction, and
  non-implicit login.
- [ ] The dedicated home is authenticated and the official provider smoke run
  has passed.
- [ ] `pnpm run eval:full` has run with maintainer authority.

The dated smoke result is recorded in [the run log](../evidence/eval-runs.md).
The smoke checkbox remains unchecked because that suite did not pass, and
`eval:full` requires separate maintainer authority.

## Amendment: explicit full evaluation stack

The maintainer provider suites are exposed through `pnpm run eval:full`. This
command is an explicit empirical evaluation stack, not a pre-push hook and not
an automatic Git gate. It runs the official validators, deterministic checks,
Promptfoo configuration validation, fixture checks, 34 routing cases, 40
behavior trials, and 12 frozen security probes before checking that the Git
status is unchanged. The expected upper bound is 86 provider calls; local JSON
reports under `evals/promptfoo/results/` preserve per-row evidence without
entering the repository.

The evidence has three distinct meanings. Routing checks positive and negative
requests for every distributed skill and uses structured provider metadata for
observed skill-file reads; this indicates routing/invocation, not complete
instruction adherence. Behavior trials use fresh workspaces, controlled
variants, protected hashes, hidden deterministic oracles, completed-turn
checks, and no-op rejection to verify that a legitimate task was actually
performed. Security probes combine a distinct adversarial fixture stimulus
with the legitimate `src/app.py` target-change oracle, protected paths, outside
sentinels, canary checks, and structured trajectory events when available.
Unavailable trajectory data remains a review limitation rather than a pass.

PyYAML is not a Tuxedo dependency. When the official local validators require
it, the maintainer supplies an isolated interpreter through
`TUXEDO_VALIDATOR_PYTHON`, created with UV. The provider stack itself remains
Node/PNPM-managed and the distributed plugin remains free of both Promptfoo
and the Codex SDK.

This full-stack provider evidence was not green. The routing, behavior, and
security outcomes, the recorded wall times, and the lost routing-identifier
limitation are recorded in [the run log](../evidence/eval-runs.md).

## Amendment: durable verdict evidence and bounded sharding

The earlier execution exposed two orchestration defects independently of the
skill verdicts. Promptfoo uses exit code 100 when assertions fail, but the
runner treated every nonzero exit as infrastructure failure and deleted the raw
export before writing sanitized evidence. In addition, security enabled deep
tracing while passing `--no-write`; trace rows then lacked their required
persisted parent evaluation and produced `TraceStore`/`EvaluatorTracing`
errors. A sequential rerun of the three provider suites also measured beyond the
intended two-hour review window; its timing is recorded in
[the run log](../evidence/eval-runs.md).

The amended decision distinguishes execution integrity from evaluation
verdicts. Exit 0 and exit 100 may produce valid evidence; exit 100 always
remains a failed command outcome, but only after its sanitized report is
written. Provider errors, timeout, empty output, incomplete turns,
missing/malformed exports, and all other exit codes remain infrastructure
failures. Raw prompts, model output, trace payloads, and credentials remain
ephemeral. Only test identity, provider/condition, pass/fail/needs-review,
sanitized reasons and deterministic component results, timing, token usage,
versions, fingerprints, and heuristic skill metadata may enter durable local
reports.

Every Promptfoo provider or red-team process now uses a
`PROMPTFOO_CONFIG_DIR` inside a disposable run root and may persist the
evaluation row required by linked trace spans. That database is removed with
the workspace after sanitized evidence is extracted; personal Promptfoo state
is neither read nor written. Routing uses
two zero-based, end-exclusive shards (`0:17`, `17:34`) and behavior uses four
(`0:2`, `2:4`, `4:6`, `6:8`). At most two shards run concurrently and each
Promptfoo process keeps provider concurrency one. Security remains a single
suite. The ranges preserve all 86 calls and unchanged reasoning settings.
Completed shard reports are checkpoints; successful shard sets also produce a
suite aggregate. Assertion failures do not prevent later authorized suites,
and `eval:full` writes a full aggregate with total wall duration before it
emits one final summarized failure after all three suite outcomes exist.

Deterministic evidence executed for this amendment proves:

- [x] exit 100 persists a failed sanitized report without raw model output;
- [x] assertion verdicts are separate from provider/incomplete-turn failures;
- [x] all routing, behavior, and security suite outcomes precede the aggregate assertion failure;
- [x] shard ranges are disjoint and complete, concurrency is bounded at two, and a completed checkpoint survives a peer error;
- [x] Promptfoo state is disposable and tracing no longer combines with `--no-write`.
- [ ] a fresh authorized `pnpm run eval:full` confirms trace persistence with the real provider and measures wall time below two hours;
- [ ] routing, behavior, and security verdicts are green.

The two-hour objective is not yet an empirical claim. The amended scheduling
is expected to improve wall time without weakening coverage, but only a fresh
authorized full run can confirm it and replace the prior non-green evidence.

Re-evaluate this decision if Promptfoo drops Codex support, the Codex SDK or App Server changes materially, Promptfoo requires cloud sharing, adapters duplicate more logic than they remove, hidden oracles cannot be integrated, workspace or credential isolation weakens, the full evaluation becomes impractical for empirical review, another framework provides superior integration with less evidence loss, or `evals/run.py` becomes demonstrably redundant.

## More Information

- [Promptfoo: Test Agent Skills](https://www.promptfoo.dev/docs/guides/test-agent-skills/)
- [Promptfoo: OpenAI Codex SDK provider](https://www.promptfoo.dev/docs/providers/openai-codex-sdk/)
- [Promptfoo: OpenAI Codex App Server provider](https://www.promptfoo.dev/docs/providers/openai-codex-app-server/)
- [Promptfoo: Evaluate Coding Agents](https://www.promptfoo.dev/docs/guides/evaluate-coding-agents/)
- [Promptfoo: Red Team Coding Agents](https://www.promptfoo.dev/docs/red-team/coding-agents/)
- [Promptfoo: Coding Agent Plugins](https://www.promptfoo.dev/docs/red-team/plugins/coding-agent/)
- [Promptfoo: Red-Team Configuration](https://www.promptfoo.dev/docs/red-team/configuration/)
- [Codex non-interactive execution](https://developers.openai.com/codex/noninteractive/)
- [Tuxedo enforcement boundaries](../architecture/enforcement.md)
- [Tuxedo evaluation architecture](../architecture/evaluations.md)
- [Tuxedo evaluation isolation model](../architecture/eval-isolation.md)
- [Tuxedo evaluation run evidence](../evidence/eval-runs.md)
- [Tuxedo evidence map](../research/evidence-map.md)
- [`evals/run.py`](../../evals/run.py)
- [`evals/verifiers.py`](../../evals/verifiers.py)
