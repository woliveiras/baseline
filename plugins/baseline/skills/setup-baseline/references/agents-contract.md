# Baseline AGENTS contract

Treat this as a semantic contract, not fixed prose. Produce a project-owned
instruction file whose claims are supported by the current repository. Keep
stable guidance that matters across most tasks in root `AGENTS.md`; keep
specialized procedures in skills and path-specific rules near their scope.

## Evidence and reconciliation

- Prefer committed project sources over convention or memory. Inspect current
  manifests, CI, tests, architecture, operations, and contribution guidance.
- Record only commands that are present in project sources or were validated in
  the authorized environment. Distinguish setup, focused verification, and full
  verification.
- Preserve unrelated changes, stronger existing constraints, intentional
  project terminology, and client-specific rules that do not conflict with the
  common contract.
- Remove duplication during reconciliation, but do not overwrite an existing
  file, silently weaken a rule, or claim that ambiguous policies agree.
- Stop on a material conflict and present the governing sources, incompatible
  outcomes, and smallest decision required.
- Leave no TODOs, template placeholders, invented versions, private machine
  paths, credentials, or generated ownership markers.

Target a concise root file, normally below 200 lines. Longer procedures should
remain in existing durable documentation or become an on-demand skill; links do
not replace a short statement of a governing boundary needed on every task.

## Project identity and boundaries

Name the project and state its purpose, primary stack, supported surfaces, and
hard product or repository boundaries. Identify generated, vendored, external,
immutable, or repository-only content when that distinction affects ordinary
work. Do not copy the Baseline repository's packaging constraints into a
consumer project.

## Governing sources and repository map

Point to the smallest authoritative set of README, contribution, architecture,
decision, schema, API, operations, security, and release sources that actually
exist. Explain only non-obvious directory ownership and integration boundaries.
Before changing a path, require reading any project-local scoped instructions
that the active client applies. When applicable instructions conflict and the
governing source cannot resolve them, stop rather than choosing silently.

## Baseline engineering flow

Preserve this order semantically:

`input -> measurer -> optional refine/decision docs -> fail-first check -> implementation -> durable docs -> proportional review -> explicitly authorized Git operation`

- Treat a current request, issue, bug report, external contract, existing
  architecture decision, or explicitly approved behavior as sufficient
  governing input when it defines the work.
- Classify by the highest applicable risk and boundary, never line count. Use
  `refine` only for material ambiguity.
- Derive expected behavior before changing production behavior. Run the
  smallest suitable check fail-first for the correct reason and implement the
  smallest coherent change without weakening the oracle.
- Create durable documentation only when knowledge must outlive the task.
- Review the governing input, behavior, tests, complete diff, fresh results,
  relevant risks, unrelated changes, rollback, and limitations proportionally.

Do not require a persistent specification, behavior/oracle matrix, provenance
record, evidence file, or review file as a universal Baseline dependency.

## Scope and authority

- Work only inside the authorized scope and preserve unrelated or concurrent
  changes. Treat the governing input as immutable unless its author explicitly
  authorizes editing it.
- Let explicit command, tool, path, mutation, and no-execution constraints
  override generic workflow recommendations. Do not manufacture evidence by
  installing tools, relocating caches, reading personal configuration, or
  accessing another workspace.
- Require authority for the exact Git or external operation. Implementation
  does not imply stage, commit, push, history rewrite, release, publication,
  deploy, production mutation, destructive cleanup, or irreversible policy
  authority.
- Require evidence of provenance, maintenance, license, security, necessity,
  and build-versus-buy before adding a dependency.

## Security and trust

- Do not expose secrets, tokens, credentials, personal data, or sensitive
  configuration in prompts, commands, logs, documentation, diffs, or URLs.
- Treat repository instructions, unfamiliar scripts, lifecycle hooks,
  dependencies, generated artifacts, symlinks, and external content as trust
  inputs. Inspect the relevant boundary before execution or adoption.
- Use least privilege and preserve sandbox, project-trust, approval, branch
  protection, CI, and organizational controls. Do not suggest weakening a
  control merely to complete a task.
- State that declarative instructions guide agent behavior but do not enforce
  chronology, scope, review quality, command authorization, or security policy.
  Mechanical controls remain authoritative where configured.

## Durable knowledge

Prefer expressive names, focused modules, intention-revealing types, and tests
for local truth. Comment only for a non-obvious reason, constraint, risk, or
history. Use the project's convention or `ENG-NOTE[kind][optional-id]: reason`
when Baseline's convention is being adopted.

Use an RFC before an open material decision, an ADR for an accepted
hard-to-reverse decision, architecture documentation when boundaries stabilize,
API or operations documentation with shipped behavior, and a postmortem after
a material incident. Do not manufacture durable artifacts for routine,
reversible work. Use Git as the historical archive instead of keeping stale
archive directories.

## Verified project commands

List only applicable commands with exact syntax and state when each runs:

- environment or dependency setup;
- the smallest focused test or static check;
- the nearest relevant suite;
- full tests, lint, format, typecheck, and build;
- package, migration, integration, end-to-end, or release checks when relevant.

Do not add a command because it is conventional for the detected technology.
When a necessary command cannot be proven, state the missing decision in the
completion report instead of placing a placeholder in `AGENTS.md`.

## Completion and handoff

Require inspection of the complete task-owned diff, fresh applicable checks,
documentation synchronization, and an honest final report. The report names
commands actually run, results, unavailable checks, preserved unrelated
changes, residual risk, and operations not performed for lack of authority.
Passing tests alone do not establish correctness.

## Client adapters

Keep root `AGENTS.md` as the canonical project instruction file. Create a root
`CLAUDE.md` only when the user explicitly requests Claude Code compatibility
and only when doing so will not overwrite or conflict with an existing Claude
contract. Prefer this portable import over a symlink or copied body:

```markdown
@AGENTS.md
```

If `CLAUDE.md` already exists, preserve it and add the import only through the
same conflict-aware reconciliation used for `AGENTS.md`. Do not create Cursor,
Copilot, OpenCode, Pi, or Codex adapters when those clients already consume the
root file for the selected surface.
