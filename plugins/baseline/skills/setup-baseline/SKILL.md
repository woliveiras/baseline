---
name: setup-baseline
description: Create, audit, or safely reconcile a repository-root AGENTS.md with the Baseline engineering contract and observed project facts. Use only when the user explicitly asks to initialize, set up, adopt, audit, or update Baseline project instructions; do not activate for ordinary software work or general questions about AGENTS.md.
---

# Setup Baseline

Read [the AGENTS contract](./references/agents-contract.md) completely before
editing project instructions.

## Establish the project boundary

1. Resolve the repository root from the authorized workspace and inspect its
   worktree state. Work only on the root instruction file unless the user names
   another scope.
2. Read an existing root `AGENTS.md` and relevant project-local instructions,
   README, contribution guide, manifests, lockfiles, CI, architecture, security,
   release, and test documentation. Do not inspect personal or global agent
   configuration.
3. Derive project identity, boundaries, authoritative sources, non-obvious
   structure, and commands only from current repository evidence. Do not install
   dependencies, call a model or provider, or access another workspace to fill
   gaps without specific authority.

## Select the safe operation

- When `AGENTS.md` is absent, create it at the repository root.
- When it already conforms, leave it unchanged and report the evidence.
- When it is incomplete, preserve stronger and project-specific instructions
  and apply the smallest task-owned diff that reconciles the missing contract.
- When a material conflict would change behavior, scope, authority, security,
  or verification, stop and request the smallest human decision.

Do not overwrite an existing file wholesale, weaken a local rule, add managed
blocks, or copy Baseline's own repository instructions. Do not invent commands,
paths, architecture, tools, or guarantees.

## Write and validate

1. Express the applicable semantic requirements from the contract with concise,
   specific, verifiable project language. Omit sections for which no durable
   project fact exists instead of leaving placeholders.
   Preserve the contract's activity-routing semantics without requiring the
   user to name a skill. Do not omit or generalize an applicable owner mapping.
2. Create the optional Claude adapter only under the contract's explicit
   condition. Never duplicate the `AGENTS.md` body into another client file.
3. Re-read every changed instruction as one contract. Check conflicts, local
   links, command provenance, sensitive values, scope, and the complete diff.
4. Run only authorized static or repository checks that meaningfully validate
   the instructions. Treat unavailable behavioral validation as a limitation,
   not passing evidence.

Report whether the file was created, reconciled, or already conforming; list
the repository evidence used, checks actually run, preserved unrelated changes,
open decisions, and residual limitations. Do not stage, commit, push, publish,
release, deploy, or mutate production without authority for that exact action.
