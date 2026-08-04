# Tuxedo engineering contract

Tuxedo is a portable, spec-driven engineering toolkit. The repository is the product. Do not add a CLI, daemon, package manager, sync layer, telemetry, client generator, or Geremmyas runtime dependency.

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

Classify work by behavioral blast radius and risk, never line count: `trivial`, `small`, `medium`, or `large/high-risk`. A small diff can be high-risk. Medium and larger testable changes require at least one `spec-derived`, `independent`, or `external` oracle. Use explicit context separation for medium and larger review work.

## Authority and evidence

- Work autonomously inside the authorized local scope and preserve unrelated changes.
- Require explicit human authority for push, history rewrite, release, publication, deploy, production mutation, destructive operations, and irreversible policy changes.
- Hooks enforce only mechanical conditions. They cannot establish architecture quality, semantic completeness, human authorization provenance, runtime safety, or empirical effectiveness.
- Do not add a direct dependency without evidence for provenance, maintenance, license, security, necessity, and build-versus-buy.
- Do not claim completion without fresh commands, outputs, and residual limitations.

## Toolkit maintenance

- Keep each `SKILL.md` concise and imperative. Put optional detail one level down in `references/`.
- Keep portable workflow logic client-neutral. Put Codex invocation policy in `agents/openai.yaml` and Codex lifecycle behavior in `hooks/`.
- Add deterministic tests for every mechanical invariant.
- Keep `evals/` and maintainer research outside installed skill content. Do not run paid or extensive evals without explicit authority.
- Commit coherent task-owned slices locally with Conventional Commits. Never infer push, release, or publication authority.

## Required checks

Run the official plugin validator, the official skill validator for every skill, `python3 -m unittest discover -s tests -v`, `python3 evals/run.py --dry-run`, shell syntax checks, `git diff --check`, and `git status --short` before completion.
