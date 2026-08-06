# Using the maintainer evaluation harness

The evaluation harness is maintainer-only. It is not installed with the plugin
and is not a runtime dependency of any skill. This is the step-by-step path; see
[the evaluation architecture](../architecture/evaluations.md) for how it works,
[ADR 0001](../decisions/0001-use-promptfoo-as-evaluation-orchestrator.md) for
why, and [the isolation model](../architecture/eval-isolation.md) for how Codex
and Promptfoo state are isolated.

## Prerequisites

- Node `>=22.22.0`, UV for Python, and PNPM for Node.
- Install Node dependencies: `pnpm install --frozen-lockfile`.

## 1. Authenticate a dedicated Codex home (once)

```bash
pnpm run eval:login        # official codex login with the ChatGPT/Codex account
pnpm run eval:auth:status  # verify; prints the dedicated home and login command if absent
```

The session is stored in `$HOME/.codex-tuxedo-evals` by default. To use another
home, set an absolute `TUXEDO_EVAL_CODEX_HOME` outside this checkout. See
[the isolation model](../architecture/eval-isolation.md) for the resolution and
rejection rules.

## 2. Sanity check

```bash
pnpm run eval:smoke        # narrow provider sanity check
```

## 3. Run the suites you need

```bash
pnpm run eval:skills       # routing + behavior
pnpm run eval:security     # frozen security probes
pnpm run eval:compare      # requires TUXEDO_EVAL_PROPOSED_ROOT
```

`eval:compare` performs three independent repetitions. Each repetition receives
new current/proposed workspaces; the harness never reuses a workspace mutated by
an earlier trial.

## 4. Full stack (explicit and expensive)

To run only routing, use `pnpm run eval:routing`. Maintainers diagnosing an
affected subset can keep the same isolated runner and sanitized report path:

```bash
uv run python evals/promptfoo/scripts/run-evaluations.py \
  --suite routing \
  --case-pattern '^(implicit-|composition-)'
```

The pattern matches case descriptions. It does not weaken their assertions or
change the full-suite inventory.

```bash
pnpm run eval:full
```

`eval:full` runs the official validators, deterministic suites, 40 routing
cases, 40 behavior trials, and 12 security probes, then checks that the Git
status is unchanged. Five semantic behavior tasks across five conditions add
25 secondary rubric calls, so the upper bound is 92 target-agent calls plus 25
judgments: 117 model calls. It is not a pre-push hook, is not invoked by
installation, and a passing result does not itself authorize a push.

If the official validators require PyYAML, keep it out of the repository by
supplying an isolated interpreter:

```bash
validator_env_path="$(mktemp -d -t tuxedo-validators.XXXXXX)"
uv venv "$validator_env_path"
uv pip install --python "$validator_env_path/bin/python" PyYAML
TUXEDO_VALIDATOR_PYTHON="$validator_env_path/bin/python" pnpm run eval:full
```

## 5. Red-team (explicit maintainer actions)

```bash
pnpm run eval:redteam:generate
pnpm run eval:redteam:review
pnpm run eval:redteam:full   # expensive; never implied by eval:full
```

## Reading results

Sanitized, append-only JSON reports land in `evals/promptfoo/results/`, which is
ignored by Git. Raw model output, prompts, traces, and credentials are never
written there. Measured wall duration and per-run outcomes are recorded in
[the run log](../evidence/eval-runs.md).

## What each suite establishes

- Routing: does the agent route positive requests to the named skill and avoid
  unrelated skills? The assertion uses structured Codex provider metadata for
  observed skill-file reads. This is a routing and invocation signal, not proof
  of full instruction adherence.
- Behavior: does the skill change the assigned workspace as required across
  baseline/core/focal/broad/current conditions? Fresh workspaces, protected
  hashes, hidden deterministic oracles, completed-turn checks, and no-op
  rejection make a refusal or "done" response insufficient. Semantic cases add
  task-specific `llm-rubric` judgments through the dedicated Codex login. The
  grader is read-only, has no network, starts in an empty isolated directory,
  and cannot override a deterministic failure.
- Security: does the agent complete the legitimate `src/app.py` task while
  resisting a distinct adversarial stimulus? Missing inspectable trajectory data
  stays `needs-review`; it is not inferred from output text or fixture contents.

## Cleanup and switching accounts

To switch accounts, set a different `TUXEDO_EVAL_CODEX_HOME` and run
`pnpm run eval:login`. To remove a dedicated session, delete that home manually
after confirming it is not needed. No login secret enters this repository.
