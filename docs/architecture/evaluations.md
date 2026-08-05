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

## Runner behavior and oracle matrix

| ID | Required behavior | Oracle | Evidence class |
| --- | --- | --- | --- |
| `EV-RPT-01` | Promptfoo exit 100 is an assertion verdict; preserve a failed local report before returning failure. | Mocked exit 100 plus a completed failing result produces a `fail` outcome and JSON report. | spec-derived |
| `EV-RPT-02` | Provider errors, empty output, incomplete turns, missing result files, and exit codes other than 0/100 remain infrastructure failures. | Unit tests exercise malformed provider results; the runner accepts only 0 and 100 for `promptfoo eval`. | spec-derived |
| `EV-AGG-01` | Assertion failures do not suppress later authorized suites; the aggregate command fails after collecting their outcomes. | A mocked full run invokes routing, behavior, and security before raising one summarized verdict. | independent |
| `EV-ISO-01` | Promptfoo evaluation rows and traces use one disposable local state root, never the maintainer's personal Promptfoo state. | Command/environment capture proves `PROMPTFOO_CONFIG_DIR` is under the disposable run root and `--no-write` is absent. | implementation-aware |
| `EV-SHD-01` | Shards are disjoint, cover every routing/behavior case, run with concurrency at most two, and retain completed shard reports if a peer fails. | Range and checkpoint tests cover the fixed shard catalog and a peer infrastructure error. | spec-derived |
| `EV-PRV-01` | Persist only sanitized verdict evidence, never model output, prompts, traces, credentials, or raw responses. | A synthetic secret in provider output is absent from the persisted report while the assertion reason remains. | independent |
| `EV-TIM-01` | Record actual suite wall time and do not claim the two-hour target until measured by a fresh full provider run. | Aggregate reports record the measured wall duration for each run. | external |

## Isolation and repeatability

Each write-capable provider call receives a fresh temporary Git workspace under
a fresh temporary root. The runner records before-snapshots, protected hashes,
outside synthetic sentinels, current/proposed fingerprints, model, reasoning
effort, Codex version, Promptfoo version, seed, repetition count, and duration.
The checkout is not a work directory for the provider.

Every Promptfoo provider or red-team process also receives a
`PROMPTFOO_CONFIG_DIR` below a temporary root. Promptfoo may write its
evaluation row and linked trace spans there while the process runs; the whole
state root is removed afterward. This is why provider runs do not use
`--no-write`: deep tracing requires the parent evaluation row to exist in the
same disposable database. The durable report contains only sanitized verdict
fields and never raw model output or trace payloads.

The dedicated Codex home, authentication reuse, `config.toml` fail-closed
parsing, model selection, and the isolated `TUXEDO_VALIDATOR_PYTHON` interpreter
are specified in [the isolation model](eval-isolation.md). Content isolation and
authentication reuse are separate properties: the account session is
intentionally reused, while personal behavior-bearing content is not.

Ignored `generated/` and `results/` have different responsibilities. Generated
red-team probes are review inputs and may persist. JSON result reports are
append-only local evidence and may persist across runs. The evaluation runner
validates their shape without deleting either kind of evidence.

## Failure semantics

The provider must produce a non-empty completed response. Provider errors,
empty responses, incomplete turns, a missing/malformed result file, timeout,
and Promptfoo exit codes other than 0 or 100 are infrastructure failures.
Promptfoo exit 100 means assertions failed: the runner parses it, writes the
sanitized failed report, and returns a failed suite outcome. Failed assertions
and `needs-review` are verdicts, not reasons to discard evidence. Tuxedo
assertions apply deterministic checks: no-op behavior
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
Routing is split into two disjoint shards and behavior into four disjoint
shards. At most two shards execute concurrently; each Promptfoo process still
uses provider concurrency one. Security remains a single sequential suite.
Each completed shard writes a checkpoint report, and a successful set of
shards writes a suite aggregate. Thus a later assertion failure or peer
infrastructure failure does not erase already completed evidence. After all
three suite outcomes exist, `eval:full` writes a full aggregate with total wall
duration and returns one aggregate failure if any outcome failed or needs
review.

The 86 provider calls remain the expected upper bound for one non-repeated
run; sharding changes scheduling, not coverage. Authoritative wall duration
and per-row evidence are recorded in ignored JSON reports under
`evals/promptfoo/results/`, and dated run outcomes with the open sub-two-hour
target are recorded in [the run log](../evidence/eval-runs.md). `eval:full` is
not invoked by installation, hooks, or Git push, and a passing result does not
itself authorize a push.

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
