# Tuxedo engineering contract

Tuxedo is a portable, spec-driven engineering toolkit. The repository is the product. Do not add a CLI, daemon, package manager, sync layer, telemetry, client generator, or any runtime dependency.

## Fidelity chain

Use the [Repository glossary](GLOSSARY.md) for the canonical meaning of specialized workflow terms.

For material behavior changes, preserve traceability through:

`spec -> behavior/oracle matrix -> tests -> implementation -> evidence -> final review`

- Read the complete governing spec before implementing or reviewing it. Metadata is only for routing.
- Treat the spec as canonical intent, not immutable truth. Correct ambiguity, contradiction, or an invalid premise explicitly and reconcile every downstream artifact.
- Give acceptance criteria stable IDs. Link tests and evidence to those IDs.
- Classify each oracle's provenance as `spec-derived`, `independent`, `implementation-aware`, `external`, or `diagnostic-probe`.
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
- Do not edit a governing spec, request, or bug report merely to make implementation or evidence pass. Treat it as immutable task input unless the user explicitly authorizes changing that artifact. When authority is absent, report proposed corrections in the final response unless the task explicitly authorizes a separate writable artifact; an analysis-only or no-write task may inspect with read-only commands but must not execute project code or tests that create caches, or create reconciliation, matrix, proposal, or evidence files.
- Require explicit human authority for push, history rewrite, release, publication, deploy, production mutation, destructive operations, and irreversible policy changes. Use Codex Rules for configured standard direct-command prompts and prohibitions; keep sandbox and approval policy authoritative for other forms.
- Do not add a direct dependency without evidence for provenance, maintenance, license, security, necessity, and build-versus-buy.
- Do not claim completion without fresh commands, outputs, and residual limitations.

## Declarative task flow

- **Oracle before implementation:** For testable behavior, define the expected observable result as the oracle, choose the smallest suitable unit, integration, contract, end-to-end, static, or inspection verification, and run that verification fail-first before production implementation. When automated verification is not appropriate, record the reason, the oracle, and the strongest available manual verification before editing production behavior.
- **Authorized scope:** Derive the allowed files and behavior from the current spec, task, or plan. Preserve pre-existing and unrelated changes; do not broaden the task because adjacent work is useful.
- **Review before completion:** Reconstruct spec review without tests or implementation, test review without the new implementation, and code review with the complete diff and fresh evidence. Passing tests alone do not establish fidelity.
- **Task-owned commit:** Before a local commit, inspect status, unstaged diff, staged diff, and untracked files; stage explicit task-owned paths or hunks and re-read the complete cached diff.
- **Additional work:** Do not begin another task, remediation, cleanup, or refactor unless the user authorized it. Report discoveries separately and request authority when they materially expand scope.
- **Skill composition:** Use client-provided descriptions for routing. Do not scan or open every installed `SKILL.md` to choose a workflow. Select the smallest complete set of applicable workflows from the descriptions, then read each applicable `SKILL.md` completely before acting: every clearly applicable implicit workflow and every explicitly invoked workflow. When one request has multiple outcomes with independently matching skill owners, compose them. Do not stop after the first match, substitute an unaided response for an applicable installed workflow, or make one skill silently own another skill's artifact.
- These are declarative requirements, not mechanical enforcement. Record observed workflow failures during real tasks; consider a narrow gate only after recurring evidence and only without a consumer runtime dependency.

## Toolkit maintenance

- Keep each `SKILL.md` concise and imperative. Put optional detail one level down in `references/`.
- Keep portable workflow logic client-neutral. Put Codex invocation policy in `agents/openai.yaml`.
- Add deterministic tests for every mechanical invariant.
- Keep `evals/` and maintainer research outside installed skill content. Do not run paid or extensive evals without explicit authority.
- Commit coherent task-owned slices locally with Conventional Commits. Never infer push, release, or publication authority.

### Commit convention

- Format local commit subjects as `type(scope): imperative subject`; omit the scope only when no stable subsystem name helps.
- Keep the subject specific, imperative, and under 72 characters. Use a body when the reason, migration, evidence, or residual risk is not obvious from the diff.
- Good: `feat(evals): isolate Codex authentication`, `fix(routing): preserve multi-skill assertions`, `docs(skills): add Codex installation guide`.
- Bad: `fix stuff` (no scope or intent), `Updated files` (not imperative or behavioral), `feat: changes` (not specific).
- A Conventional Commit describes the staged task-owned candidate; it never expands authority to stage unrelated work or to push.

## Toolchain convention

- Use UV for anything involving Python: run scripts and tests with `uv run python ...`; do not introduce Python virtualenv or pip workflow instructions.
- Use PNPM for anything involving Node.js: install with `pnpm install --frozen-lockfile` and run package commands with `pnpm run` or `pnpm exec`; do not use npm commands or maintain a `package-lock.json`.

## Maintainer evaluations

- Promptfoo and `@openai/codex-sdk` are development-only; never add them to the distributed plugin or installed skill content.
- Discover official validators from the local Codex installation or `TUXEDO_PLUGIN_VALIDATOR`/`TUXEDO_SKILL_VALIDATOR`; use `TUXEDO_VALIDATOR_PYTHON` for an isolated validator interpreter when PyYAML is unavailable. Never version personal absolute paths.
- Use `$HOME/.codex-tuxedo-evals` by default, or an explicit absolute `TUXEDO_EVAL_CODEX_HOME` outside this checkout and outside personal `CODEX_HOME`/`$HOME/.codex`; the resolver checks symlink targets. Run `pnpm run eval:login` explicitly for the ChatGPT/Codex login and `pnpm run eval:auth:status` to verify `codex login status`. Never copy, inspect, print, or symlink personal `auth.json` into the evaluation home.
- The dedicated home may retain Codex operational state such as authentication, minimal configuration, logs, history, sessions, state databases, and shell snapshots. Allow only Codex-managed `skills/.system`, `plugins/cache/openai-curated-remote`, and empty `plugins/.remote-plugin-install-staging`; reject personal or unknown skill/plugin namespaces, memories, rules, instruction files, and MCP configuration because they can change evaluated behavior. Tuxedo parses `config.toml` fail-closed: `cli_auth_credentials_store` and Codex project `trust_level` metadata are allowed; hooks, profiles, model/model_provider(s), MCP, instruction, policy, unknown top-level settings, and other project metadata are rejected. This recognizes current CLI-managed surfaces; future surfaces fail closed. The allowed auth-store value is not semantically validated.
- Allowed managed evaluation-home entries must be real directories/files rather than symlinks, so a personal target cannot hide behind an allowed name.
- Neither `OPENAI_API_KEY` nor `CODEX_API_KEY` is a requirement or fallback for the dedicated evaluation flow. The preflight removes both from Codex child environments, accepts only the `Logged in using ChatGPT` status label, and requires that evidence before creating workspaces or making provider calls; API-key, agent-identity, ambiguous, or failed statuses are rejected.
- Provider configurations omit a fixed `model`; the Codex CLI selects an account-supported model for the authenticated ChatGPT/Codex session, and reports label this as `codex-cli-default`. Do not pin a model without a fresh compatibility check for the selected authentication method.
- Run `pnpm run eval:full` only with explicit maintainer authority because it invokes model calls and consumes quota. It runs the official validators, deterministic checks, config validation, then all routing, behavior, frozen security, and task-specific secondary rubric cases before proving Git status is unchanged. The current upper bound is 117 model calls: 92 target trials plus 25 semantic judges. Routing and behavior may use disjoint shards with at most two active processes; do not reduce coverage or reasoning to optimize elapsed time. It is an explicit empirical evaluation, not a pre-push hook or an automatic Git gate.
- Treat `evals/promptfoo/generated/` as reviewable generated probes and `evals/promptfoo/results/` as append-only local reports. Persist a sanitized checkpoint for every completed shard, including Promptfoo exit 100 assertion failures; aggregate verdicts only after all authorized suite outcomes are available. Never persist raw model output, prompts, traces, or credentials. Do not make `eval:full` require either directory to be empty or delete prior evidence silently.
- Give each Promptfoo provider or red-team process a disposable `PROMPTFOO_CONFIG_DIR`. Deep tracing requires Promptfoo to persist the parent evaluation row in that disposable database, so do not combine tracing with `--no-write`; remove the entire temporary state after extracting sanitized evidence.
- Frozen security probes require a concrete adversarial fixture stimulus and a legitimate deterministic oracle. A refusal or “done” response without the requested edit is not a pass. The canary check covers exfiltration/copying; it does not establish silent reads without reliable trajectory evidence.
- Keep `evals/run.py` and `evals/verifiers.py` authoritative until a separately reviewed parity decision is evidenced.

## Required checks

These required checks apply to the Tuxedo maintainer checkout. In a consumer project or synthetic evaluation workspace, run only checks already present and applicable; do not install dependencies or access paths outside the authorized workspace to manufacture evidence. Report unavailable checks honestly.

Run the official plugin validator, the official skill validator for every skill, `uv run python -m unittest discover -s tests -v`, `uv run python evals/run.py --dry-run`, shell syntax checks, `git diff --check`, and `git status --short` before completion.
