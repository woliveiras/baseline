---
status: accepted
date: 2026-08-06
decision-makers:
  - William Oliveira
---

# Defer lifecycle hooks pending empirical need

## Context and Problem Statement

Tuxedo initially shipped Codex `PreToolUse` and `Stop` hooks that invoked a Python guard through UV. Projects could opt into policy, completion receipt, tree-hash, evidence-hash, and review-receipt validation.

The mechanism introduced UV and Python into the consumer execution path and could let UV discover or synchronize the consumer project. It also attempted to enforce a workflow that had not yet been exercised by the maintainer across ordinary real tasks. The existing evaluations measure skill routing and configured behavior; they do not establish the incremental value of lifecycle hooks.

Tuxedo needs to validate whether strict declarative guidance is sufficient before accepting a runtime dependency and a second policy system.

## Decision Drivers

- Keep installed skills free of runtime dependencies.
- Avoid modifying or discovering consumer project environments during plugin lifecycle events.
- Validate an actual recurring failure before designing enforcement.
- Preserve strict oracle-first development, scope authority, three-phase review, and task-owned commits.
- Avoid receipts that prove hashes or declared exposure while appearing to prove semantic quality or chronology.
- Keep command authority in Codex Rules, approvals, sandboxing, and human decisions.

## Considered Options

### Keep the current UV and Python hooks

- Good, because some stale artifact relationships are mechanically detectable.
- Bad, because the launcher participates in the consumer environment.
- Bad, because the current commit gate does not bind the staged Git index.
- Bad, because no real-task baseline establishes that the mechanism solves a recurring problem.

### Rewrite the guard in shell

- Good, because macOS and Linux provide a shell.
- Bad, because portable JSON parsing, path containment, globbing, SHA-256, and filesystem error handling become fragile.
- Bad, because reimplementation complexity remains without evidence that the gate is needed.

### Isolate UV and retain Python

- Good, because `--no-project`, `--no-config`, offline execution, and disabled Python downloads can avoid consumer-project synchronization.
- Bad, because UV and Python remain runtime prerequisites.
- Bad, because it preserves the receipt system before its value is established.

### Remove lifecycle enforcement and run a declarative experiment

- Good, because the installed product returns to skills and optional native Rules without a runtime.
- Good, because real tasks can reveal which failures, if any, recur.
- Good, because a future hook can be narrow and evidence-driven.
- Bad, because AGENTS and skills guide behavior but cannot mechanically block a violation.

## Decision Outcome

Remove Tuxedo lifecycle hooks, their launcher, policy and completion-receipt templates, review-receipt JSON assets, hook fixtures, and hook-specific tests. Remove lifecycle-hook capabilities and enforcement claims from the plugin manifest and public documentation.

Strengthen the declarative contract instead:

1. establish the authorized task and exclusions;
2. define an appropriate observable oracle before production implementation;
3. keep changes within authorized scope;
4. perform reconstructed spec, test, and code review;
5. inspect the staged candidate and commit only task-owned changes;
6. request authority before beginning additional work.

Retain Codex Rules as an optional command-authority template. Retain deterministic tests, CI, evaluations, skills, spec/matrix/evidence artifacts, and semantic review guidance.

## Empirical checkpoint

Observe 10–20 real maintainer tasks and record, without adding hidden enforcement:

- production implementation started before a suitable oracle;
- unauthorized files or behavior changed;
- tests derived from the implementation rather than the specification;
- required review omitted;
- staged content included unrelated changes;
- additional work began without user authority.

A future lifecycle hook requires all of the following:

- a recurring observed failure;
- a narrow mechanically observable invariant;
- a deterministic false-positive/false-negative test matrix;
- no consumer-project mutation;
- no installed runtime dependency;
- documentation that does not claim semantic guarantees from a mechanical check.

## Consequences

- The workflow is strict but declarative; it is not a technical gate.
- Consumers need no UV or Python to use Tuxedo skills.
- Tuxedo temporarily gives up mechanical stale-receipt detection.
- Review quality, chronology, and task ownership remain agent and human responsibilities supported by tests, Git inspection, and evidence.
- The removed implementation remains recoverable from Git history; no dormant copy is kept in the installed product.

## Validation

The governing acceptance criteria and oracle matrix are in [`SPEC-0001`](../../specs/0001-declarative-workflow/spec.md).
