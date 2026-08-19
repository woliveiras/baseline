# Evaluation isolation and authentication

Reference for how the development evaluation harness isolates Codex state,
authentication, and Promptfoo state. Step-by-step usage is in
[the harness guide](../guides/using-the-eval-harness.md); the rationale is in
[ADR 0001](../decisions/0001-use-promptfoo-as-evaluation-orchestrator.md).

## Dedicated Codex home

- The evaluation home defaults to `$HOME/.codex-baseline-evals`.
- `BASELINE_EVAL_CODEX_HOME` overrides it only with an absolute path outside this
  checkout, distinct from the personal `CODEX_HOME` and `$HOME/.codex`, and safe
  after symlink resolution. Relative, personal, checkout, and unsafe-symlink
  paths are rejected.
- `BASELINE_EVAL_CODEX_PATH` selects the Codex executable.
- The checkout is never a provider work directory.

## Authentication

- `pnpm run eval:login` runs the official `codex login` flow once with the
  ChatGPT/Codex account and stores the session in the dedicated home.
- The preflight and `pnpm run eval:auth:status` use `codex login status` as
  evidence. No command reads, copies, prints, or symlinks `auth.json`.
- Only the status label `Logged in using ChatGPT` is accepted. API-key,
  agent-identity, ambiguous, and failed statuses are rejected, so a successful
  exit code alone is not proof of the account-based method.
- Neither `OPENAI_API_KEY` nor `CODEX_API_KEY` is required or accepted as a
  silent substitute.
- Authentication reuse and content isolation are separate guarantees: the
  account session is reused; personal behavior-bearing content is not.

## What the dedicated home may contain

Allowed, because the Codex CLI may materialize them as operational state:
authentication, minimal configuration, logs, history, sessions, state
databases, shell snapshots, `skills/.system`,
`plugins/cache/openai-curated-remote`, and an empty
`plugins/.remote-plugin-install-staging`. Allowed managed entries must be real
directories or files rather than symlinks, so a personal target cannot hide
behind an allowed name.

Rejected, because they can change evaluated behavior: personal or unknown
skill/plugin namespaces, `memories`, `rules`, instruction files, and MCP
configuration.

## `config.toml` fail-closed parsing

- Allowed: `cli_auth_credentials_store` and Codex project `trust_level`
  metadata.
- Rejected: `hooks`, `profiles`, `model`, `model_provider(s)`, MCP,
  instruction, policy, unknown top-level settings, and other project metadata.

The allowlist recognizes the current CLI-managed surfaces; a future surface or
unrecognized status label fails closed. Baseline does not validate the semantics
of the allowed auth-store value, so keep the file minimal.

## Model selection

Provider configurations omit a fixed `model`, so the Codex CLI selects a model
supported by the authenticated ChatGPT/Codex account. Reports record this as
`codex-cli-default`. A model pin requires a fresh compatibility check against
the selected authentication method.

## Promptfoo state

Every Promptfoo provider or red-team process receives a `PROMPTFOO_CONFIG_DIR`
under a disposable run root. Promptfoo persists its evaluation row and linked
trace spans there; the whole state root is removed afterward. Provider runs do
not use `--no-write`, because deep tracing requires the parent evaluation row to
exist. Durable reports contain only sanitized verdict fields, never raw model
output or trace payloads. Personal Promptfoo state is neither read nor written.

## Official validators and PyYAML

The official plugin and skill validators are discovered from the local Codex
installation or environment configuration. They run with the repository's UV
interpreter and locked PyYAML development dependency. The non-package UV
project is repository-only and neither PyYAML nor its environment enters the
installed plugin or any consumer project.

## Network and result paths

Provider runs use `network_access_enabled: false`, no Promptfoo cloud sharing,
and no remote red-team generation. Red-team inputs are versioned frozen
fixtures. Ignored `evals/promptfoo/results/` holds append-only sanitized
reports; the runner validates their shape and does not delete prior evidence.
