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
| Red-team generation and review | Promptfoo, explicitly invoked | `eval:redteam:generate`, `eval:redteam:review`; never part of `verify:push` |
| Authority and privacy | Tuxedo runner and provider config | dedicated `TUXEDO_EVAL_CODEX_HOME`, no cloud share, no remote red-team generation, no external operations |

## Isolation and repeatability

Each write-capable provider call receives a fresh temporary Git workspace under
a fresh temporary root. The runner records before-snapshots, protected hashes,
outside synthetic sentinels, current/proposed fingerprints, model, reasoning
effort, Codex version, Promptfoo version, seed, repetition count, and duration.
The checkout is not a work directory for the provider.

`TUXEDO_EVAL_CODEX_HOME` must be an existing dedicated authenticated directory
outside the repository and distinct from personal `CODEX_HOME`. The runner
does not copy or inspect authentication contents. Use an API key only through
the process environment or a dedicated home; do not place personal skills,
memories, sessions, or history in the evaluation home.

The official Codex plugin/skill validators are discovered from environment
configuration or the local Codex installation. If the validator requires
PyYAML, provide an isolated interpreter through `TUXEDO_VALIDATOR_PYTHON`; it
is deliberately not a Tuxedo runtime dependency.

Ignored `generated/` and `results/` have different responsibilities. Generated
red-team probes are review inputs and may persist. JSON result reports are
append-only local evidence and may persist across runs. The pre-push gate
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

The normal pre-push sequence is:

```bash
npm run verify:push
```

This runs the official validators, Python and shell checks, all six Promptfoo
config validations, fixture checks, 34 routing cases, 40 behavior-provider
trials, and 12 security probes, then checks that Git status is unchanged. It
requires an authenticated dedicated evaluation home and consumes model quota.
The 86 provider calls are an expected upper bound for one non-repeated run;
the authoritative duration and per-row evidence are recorded in ignored JSON
reports under `evals/promptfoo/results/`.

Use the narrower commands when the full gate is disproportionate:

```bash
npm run eval:smoke
npm run eval:skills
npm run eval:security
npm run eval:compare      # requires TUXEDO_EVAL_PROPOSED_ROOT
npm run eval:redteam:generate
npm run eval:redteam:review
```

`npm run eval:redteam:full` is intentionally explicit and expensive. No
red-team command is implied by ordinary validation or `verify:push`.

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
