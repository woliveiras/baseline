# Maintainer evaluation architecture

Promptfoo is a maintainer-only orchestration layer. It is not installed with
the plugin and is not a runtime dependency of any distributed skill. The
official `openai:codex-sdk` provider supplies Codex execution; Tuxedo supplies
the tasks, fixtures, workspace lifecycle, deterministic oracles, and authority
boundaries.

## Responsibility matrix

| Concern | Owner | Evidence and boundary |
| --- | --- | --- |
| Provider execution, repetitions, latency, tokens, and local aggregation | Promptfoo adapter | `evals/promptfoo/promptfooconfig.yaml`, provider result validation |
| Canonical behavior tasks and hidden deterministic checks | Tuxedo | `evals/tasks/`, `evals/verifiers.py`, `assertions/workspace.py` |
| Routing positive/negative cases | Tuxedo catalog plus Promptfoo skill assertions | `tests/routing.yaml`, `tests.py`, `assertions/routing.py`; metadata remains heuristic |
| Variant comparisons | Tuxedo workspace preparation | baseline/core/focal/broad/current/proposed roots and distinct fingerprints |
| Security regression probes | Tuxedo fixtures and assertions | every frozen probe has a distinct stimulus, a legitimate `src/app.py` oracle, and outside-canary checks |
| Red-team generation and review | Promptfoo, explicitly invoked | `eval:redteam:generate`, `eval:redteam:review`; never part of `eval:full` |
| Authority and privacy | Tuxedo runner and provider config | dedicated `TUXEDO_EVAL_CODEX_HOME`, no cloud share, no remote red-team generation, no external operations |

## Isolation and repeatability

Each write-capable provider call receives a fresh temporary Git workspace under
a fresh temporary root. The runner records before-snapshots, protected hashes,
outside synthetic sentinels, current/proposed fingerprints, model, reasoning
effort, Codex version, Promptfoo version, seed, repetition count, and duration.
The checkout is not a work directory for the provider.

The evaluation home resolves to `$HOME/.codex-tuxedo-evals` by default and may
be overridden with `TUXEDO_EVAL_CODEX_HOME`. It must be absolute, outside the
repository, distinct from personal `CODEX_HOME` and `$HOME/.codex`, and safe
after symlink resolution. Run `pnpm run eval:login` once to execute the
official `codex login` flow with the ChatGPT/Codex account, then use
`pnpm run eval:auth:status` to verify it. The runner uses `codex login status`
as evidence and never copies, reads, or prints `auth.json`. It accepts only
the status label `Logged in using ChatGPT`; API-key, agent-identity, ambiguous,
and failed statuses are rejected. Neither `OPENAI_API_KEY` nor
`CODEX_API_KEY` is a requirement or fallback for this path.
`TUXEDO_EVAL_CODEX_PATH` can select the Codex executable.
Provider configurations omit a fixed `model` so the Codex CLI selects a model
supported by the authenticated ChatGPT/Codex account; result metadata records
`codex-cli-default`. A future model pin requires a fresh compatibility check
against the selected authentication method.

The home may contain operational state created by Codex, including
authentication, minimal configuration, logs, history, sessions, state
databases, and shell snapshots. Codex-managed `skills/.system`,
`plugins/cache/openai-curated-remote`, and an empty
`plugins/.remote-plugin-install-staging` are also allowed because the CLI may
materialize them during normal operation. Personal or unknown skill/plugin
namespaces, `memories`, `rules`, instruction files, and MCP configuration are
rejected because they can change evaluated behavior. Tuxedo parses
`config.toml` fail-closed: `cli_auth_credentials_store` and Codex project
`trust_level` metadata are allowed; `hooks`, `profiles`, `model`,
`model_provider(s)`, MCP, instruction, policy, unknown settings, and other
project metadata are rejected. This small allowlist recognizes the current
CLI-managed surfaces; a future surface fails closed and the curated plugin
cache is trusted only as Codex-managed operational content. Tuxedo does not
validate the semantics of the allowed auth-store value, so the maintainer must
keep the file minimal; an unrecognized future status label also fails closed.
Allowed managed entries are required to be real directories/files rather than
symlinks, so a personal target cannot hide behind an allowed name.
Content isolation and authentication reuse are separate properties:
the account session is intentionally reused, while personal behavior-bearing
content is not.

The official Codex plugin/skill validators are discovered from environment
configuration or the local Codex installation. If the validator requires
PyYAML, provide an isolated interpreter through `TUXEDO_VALIDATOR_PYTHON`; it
is deliberately not a Tuxedo runtime dependency.

Ignored `generated/` and `results/` have different responsibilities. Generated
red-team probes are review inputs and may persist. JSON result reports are
append-only local evidence and may persist across runs. The evaluation runner
validates their shape without deleting either kind of evidence.

## Failure semantics

The provider must produce a non-empty response. The runner rejects provider
errors, empty responses, unsuccessful result flags, and failed Promptfoo
assertions. Tuxedo assertions then apply deterministic checks: no-op behavior
tasks fail when mutation is required, forbidden mutation remains forbidden,
protected hashes must hold, and `needs-review` is not silently promoted to
pass. Security probes additionally require their legitimate target change;
“done” without the requested edit is therefore a failure. A security probe's
canary check detects copying or exposing the synthetic canary. It does not
claim to prove a silent read when a provider trace is unavailable.

When Codex SDK `raw.items` or an equivalent structured trace is present, the
trajectory adapter inspects only command names/arguments and structured file
paths. It does not search command output, agent text, prompts, or fixture
contents. A trace schema without inspectable events is recorded as
`needs-review` for trajectory-sensitive probes.

## Suites and authority

The full empirical evaluation is an explicit maintainer action:

```bash
pnpm run eval:full
```

This runs the official validators, Python and shell checks, all six Promptfoo
config validations, fixture checks, 34 routing cases, 40 behavior-provider
trials, and 12 security probes, then checks that Git status is unchanged. It
requires an authenticated dedicated evaluation home and consumes model quota.
The 86 provider calls are an expected upper bound for one non-repeated run;
the authoritative duration and per-row evidence are recorded in ignored JSON
reports under `evals/promptfoo/results/`. It is not invoked by installation,
hooks, or Git push, and a passing result does not itself authorize a push.

The evidence chain answers three different questions:

1. Routing: does the agent route positive requests to the named skill and avoid
   unrelated skills? The assertion uses structured Codex provider metadata for
   observed skill-file reads. This is a routing/invocation signal, not proof of
   full skill adherence.
2. Behavior: does the skill change the assigned workspace as required across
   controlled baseline/core/focal/broad/current conditions? Fresh workspaces,
   protected hashes, hidden deterministic oracles, completed-turn checks, and
   no-op rejection make a refusal or “done” response insufficient.
3. Security: does the agent complete the legitimate local task while resisting
   the distinct adversarial stimulus? Each frozen probe has a target-change
   oracle plus protected, outside-sentinel, canary, and structured trajectory
   checks. Missing inspectable trajectory data remains a review limitation; it
   is not inferred from output text or fixture contents.

`eval:smoke` is the narrow provider sanity check. `eval:skills` runs routing
and behavior, and `eval:security` runs the frozen security probes. The ordinary
deterministic checks remain the fast local feedback path; the provider suites
are explicit empirical evidence and are not a pre-push gate.

Use the narrower commands when the full gate is disproportionate:

```bash
pnpm run eval:smoke
pnpm run eval:skills
pnpm run eval:security
pnpm run eval:compare      # requires TUXEDO_EVAL_PROPOSED_ROOT
pnpm run eval:redteam:generate
pnpm run eval:redteam:review
```

`pnpm run eval:redteam:full` is intentionally explicit and expensive. No
red-team command is implied by ordinary validation or `eval:full`.

## Residual limitations

The Codex `skill-used` signal and `metadata.skillCalls` are provider heuristics,
not proof of adherence. Security probes exercise frozen local stimuli and a
small deterministic oracle; they do not certify universal security, silent
credential reads, network infrastructure, or all possible prompt-injection
trajectories. Model, provider, CLI, task, fixture, and dependency upgrades
require fresh evidence and review. The existing `evals/run.py` remains until
parity evidence supports a separate reduction change.

See the [decision record](../decisions/0001-use-promptfoo-as-evaluation-orchestrator.md)
for the trade-off and confirmation checklist.
