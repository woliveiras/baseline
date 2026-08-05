# Tuxedo engineering contract

Tuxedo is a portable, spec-driven engineering toolkit. The repository is the product. Do not add a CLI, daemon, package manager, sync layer, telemetry, client generator, or any runtime dependency.

## Fidelity chain

For material behavior changes, preserve traceability through:

`spec -> behavior/oracle matrix -> tests -> implementation -> evidence -> final review`

- Read the complete governing spec before implementing or reviewing it. Metadata is only for routing.
- Treat the spec as canonical intent, not immutable truth. Correct ambiguity, contradiction, or an invalid premise explicitly and reconcile every downstream artifact.
- Give acceptance criteria stable IDs. Link tests and evidence to those IDs.
- Classify test evidence as `spec-derived`, `independent`, `implementation-aware`, `external`, or `diagnostic-probe`.
- Never let a test silently redefine behavior because it was written after the implementation.
- Review in three phases: spec without implementation, tests without the new implementation, then code with spec, matrix, tests, diff, and evidence.
- Report final review findings under `Spec`, `Standards`, and `Risk`.

## Proportionality

Classify work by the highest applicable condition, never line count:

| Tier | Boundary | Minimum evidence and review |
| --- | --- | --- |
| `trivial` | No observable behavior, contract, data, security, dependency, or runtime effect. | Focused validation; review may stay inline. |
| `small` | One localized behavior in one established boundary, easy rollback, and no sensitive risk domain. | Criterion-linked oracle and one isolated reviewer across the three phases. |
| `medium` | Multiple modules, a public contract, schema/serialization, persistence, concurrency, compatibility, or a non-local dependency seam. | Explicit matrix, at least one `spec-derived`, `independent`, or `external` oracle, and reconstructed review contexts. |
| `large/high-risk` | Cross-context architecture, irreversible migration, unproven rollback, or security, privacy, authorization, data-loss, money, compliance, production, release, or publication exposure. | Independent phase reviewers when available, explicit rollback/residual risk, and the strongest relevant suite. |

When conditions disagree, use the higher tier. A familiar implementation does not lower a sensitive risk domain.

## Authority and evidence

- Work autonomously inside the authorized local scope and preserve unrelated changes.
- Require explicit human authority for push, history rewrite, release, publication, deploy, production mutation, destructive operations, and irreversible policy changes. Use Codex Rules for configured standard direct-command prompts and prohibitions; keep sandbox and approval policy authoritative for other forms.
- Hooks reinforce only mechanical workflow conditions: current spec, matrix, test and implementation trees, evidence, documentation decision, and three-phase review receipts. They cannot establish architecture quality, semantic completeness, actual reviewer independence, runtime safety, or empirical effectiveness.
- Do not add a direct dependency without evidence for provenance, maintenance, license, security, necessity, and build-versus-buy.
- Do not claim completion without fresh commands, outputs, and residual limitations.

## Toolkit maintenance

- Keep each `SKILL.md` concise and imperative. Put optional detail one level down in `references/`.
- Keep portable workflow logic client-neutral. Put Codex invocation policy in `agents/openai.yaml` and Codex lifecycle behavior in `hooks/`.
- Add deterministic tests for every mechanical invariant.
- Keep `evals/` and maintainer research outside installed skill content. Do not run paid or extensive evals without explicit authority.
- Commit coherent task-owned slices locally with Conventional Commits. Never infer push, release, or publication authority.

## Toolchain convention

- Use UV for anything involving Python: run scripts and tests with `uv run python ...`; do not introduce Python virtualenv or pip workflow instructions.
- Use PNPM for anything involving Node.js: install with `pnpm install --frozen-lockfile` and run package commands with `pnpm run` or `pnpm exec`; do not use npm commands or maintain a `package-lock.json`.

## Maintainer evaluations

- Promptfoo and `@openai/codex-sdk` are development-only; never add them to the distributed plugin or installed skill content.
- Discover official validators from the local Codex installation or `TUXEDO_PLUGIN_VALIDATOR`/`TUXEDO_SKILL_VALIDATOR`; use `TUXEDO_VALIDATOR_PYTHON` for an isolated validator interpreter when PyYAML is unavailable. Never version personal absolute paths.
- Use `$HOME/.codex-tuxedo-evals` by default, or an explicit absolute `TUXEDO_EVAL_CODEX_HOME` outside this checkout and outside personal `CODEX_HOME`/`$HOME/.codex`; the resolver checks symlink targets. Run `pnpm run eval:login` explicitly for the ChatGPT/Codex login and `pnpm run eval:auth:status` to verify `codex login status`. Never copy, inspect, print, or symlink personal `auth.json` into the evaluation home.
- The dedicated home may retain Codex operational state such as authentication, minimal configuration, logs, history, sessions, state databases, and shell snapshots. Reject top-level personal `skills`, `plugins`, `memories`, `rules`, instruction files, and MCP configuration because they can change evaluated behavior. Tuxedo parses `config.toml` fail-closed: only `cli_auth_credentials_store` is allowed; hooks, profiles, model/model_provider(s), MCP, instruction, policy, and unknown top-level settings are rejected. The allowed auth-store value is not semantically validated.
- Neither `OPENAI_API_KEY` nor `CODEX_API_KEY` is a requirement or fallback for the dedicated evaluation flow. The preflight removes both from Codex child environments, accepts only the `Logged in using ChatGPT` status label, and requires that evidence before creating workspaces or making provider calls; API-key, agent-identity, ambiguous, or failed statuses are rejected.
- Run `pnpm run verify:push` only with explicit maintainer authority because it invokes model calls and consumes quota. It must run the official validators, deterministic checks, config validation, routing, behavior, and frozen security suites in that order, then prove Git status is unchanged.
- Treat `evals/promptfoo/generated/` as reviewable generated probes and `evals/promptfoo/results/` as append-only local reports. Do not make the gate require either directory to be empty or delete prior evidence silently.
- Frozen security probes require a concrete adversarial fixture stimulus and a legitimate deterministic oracle. A refusal or “done” response without the requested edit is not a pass. The canary check covers exfiltration/copying; it does not establish silent reads without reliable trajectory evidence.
- Keep `evals/run.py` and `evals/verifiers.py` authoritative until a separately reviewed parity decision is evidenced.

## Required checks

Run the official plugin validator, the official skill validator for every skill, `uv run python -m unittest discover -s tests -v`, `uv run python evals/run.py --dry-run`, shell syntax checks, `git diff --check`, and `git status --short` before completion.
