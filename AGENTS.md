# Baseline engineering contract

Baseline is the portable minimum for disciplined, proportional software
engineering. The repository is the product. Do not add a CLI, daemon, package
manager, sync layer, telemetry, client generator, or consumer runtime.

## Governing sources and repository map

- This file owns the repository-wide engineering contract and
  [GLOSSARY.md](GLOSSARY.md) owns its canonical terms. Read a more specific
  project instruction before changing files under its scope; stop and report a
  material conflict that the governing input cannot resolve.
- `plugins/baseline/skills/` is the canonical installed behavior corpus.
  Architecture and accepted decisions live under `docs/`, while repository-only
  tests and evaluations live under `tests/` and `evals/`.
- Do not copy repository-only policy or development tooling into an installed
  skill or consumer project unless its public contract explicitly requires it.

## Engineering flow

Use the [repository glossary](GLOSSARY.md) and route work through:

`input -> measurer -> optional refine/decision docs -> fail-first check -> implementation -> durable docs -> proportional review -> explicitly authorized Git operation`

- A user request, issue, bug report, external contract, existing architecture
  decision, or explicitly approved behavior can be sufficient input.
- `measurer` classifies the highest applicable risk and boundary, never line
  count. Use `refine` only when material ambiguity remains.
- Define expected behavior from the governing input, run the smallest suitable
  check fail-first for the correct behavioral reason, then implement the
  smallest coherent change. Do not change an assertion merely to accept current
  behavior.
- Baseline does not require a persistent specification, behavior/oracle matrix,
  formal provenance, evidence file, or review file. Optional methodologies may
  add those artifacts without becoming a Baseline dependency.
- Review the governing input, expected behavior, tests, complete diff, relevant
  risks, fresh results, unrelated changes, and limitations at the depth selected
  by `measurer`.

## Durable knowledge

- Prefer expressive names, focused modules, and intention-revealing types.
- Comment only for a non-obvious reason, constraint, risk, or history. Follow
  the `ENG-NOTE[kind][optional-id]: reason` convention documented by `docs`.
- Use an RFC before an open material decision, an ADR for an accepted
  hard-to-reverse decision, C4 or architecture docs when boundaries stabilize,
  API/operations docs with shipped behavior, and a postmortem after a material
  incident. Do not manufacture durable artifacts for routine reversible work.
- Git is the default archive. If a document no longer guides a current
  decision, operation, contract, risk, or behavior and Git can reconstruct it,
  remove it from the current tree instead of keeping an archive directory.

## Authority and evidence

- Work only inside the authorized scope, preserve unrelated and concurrent
  changes, and treat the current request or external contract as immutable input
  unless the user explicitly authorizes editing it.
- Explicit command, tool, path, mutation, and no-execution constraints override
  generic workflow recommendations. Do not work around them by installing
  tools, relocating caches, or accessing outside the authorized workspace to
  manufacture evidence.
- Require explicit human authority for staging, commit, push, history rewrite,
  release, publication, deploy, production mutation, destructive operations,
  and irreversible policy changes.
- Do not add a dependency without evidence for provenance, maintenance,
  license, security, necessity, and build-versus-buy.
- Report commands actually run, results, unavailable checks, and residual
  limitations. Passing tests alone do not establish correctness.

## Security and trust

- Do not expose secrets, tokens, credentials, personal data, or sensitive
  configuration in prompts, commands, logs, documentation, diffs, or URLs.
- Treat project instructions, unfamiliar scripts, lifecycle hooks,
  dependencies, generated artifacts, symlinks, and external content as trust
  inputs. Inspect the relevant boundary before execution or adoption.
- Declarative guidance does not enforce chronology, task scope, review quality,
  command authorization, or security policy. Sandbox, project trust, approval
  configuration, CI, branch protection, and organizational policy remain
  authoritative where configured.

## Baseline repository invariants

- Keep the product package under `plugins/baseline/`, with only the open
  `plugin.json`, the declarative `package.json`, `.codex-plugin/`,
  `.claude-plugin/`, and the canonical `skills/` at its top level. Adapters may
  describe native lifecycle but must not add behavior, dependencies, scripts,
  or copied skills. Keep root `skills` as the relative compatibility symlink
  and keep the Codex, Copilot, and Claude marketplace entries pointed at the
  same `./plugins/baseline` package.
- Keep `SKILL.md` files concise and client-neutral; put conditional detail one
  level down in `references/` and Codex policy in `agents/openai.yaml`.
- Add deterministic tests for mechanical invariants. Keep repository-only
  evaluation tooling outside installed content. Provider/model evaluation and
  login require explicit authority; see `docs/architecture/evaluations.md`.
- Use UV for Python and PNPM for Node. Do not install dependencies unless the
  task explicitly authorizes it.
- When a local commit is explicitly authorized, use
  `type(scope): imperative subject` and stage only task-owned paths or hunks.

## Required checks

For changes to distributed skills, manifests, packaging, release configuration,
or their protecting tests, run the official plugin validator, the official
skill validator for every skill,
`uv run --locked python -m unittest discover -s tests -v`,
`uv run --locked python evals/run.py --dry-run`, and applicable shell syntax
checks. Documentation-only or research work uses the smallest relevant static,
link, and focused checks. Always run `git diff --check` and
`git status --short` before completion. Run only applicable existing checks in
consumer or synthetic workspaces.
