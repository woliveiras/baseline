# Workflow and command boundaries

Tuxedo currently separates three responsibilities:

1. `AGENTS.md` and skills provide declarative workflow guidance.
2. Tests and CI provide executable evidence for product behavior.
3. Optional Codex Rules govern a narrow set of command-authority decisions.

Tuxedo does not distribute lifecycle hooks, launch scripts in consumer
checkouts, or claim mechanical enforcement of workflow chronology, scope,
review quality, or staged ownership. The decision and reintroduction criteria
are recorded in [ADR 0002](../decisions/0002-defer-lifecycle-hooks-pending-empirical-need.md).

The maintainer-only Promptfoo evaluation boundary is documented separately in
[the evaluation architecture](evaluations.md) and [ADR 0001](../decisions/0001-use-promptfoo-as-evaluation-orchestrator.md).

## Declarative workflow

For a material task, the active contract requires the agent to:

1. derive scope and exclusions from the authorized spec, task, or plan;
2. define and run the appropriate fail-first oracle before production code;
3. leave unrelated work unchanged and request authority before expanding scope;
4. review the spec without implementation, tests without the new
   implementation, and code with the complete diff and fresh evidence;
5. inspect Git status, unstaged changes, staged changes, and untracked files;
6. commit only the explicit task-owned candidate when local commit authority
   exists.

The appropriate oracle may be a unit, integration, contract, end-to-end,
static, or inspection check. Documentation and configuration work must not add
a meaningless unit test merely to satisfy a label.

These instructions are strict but declarative. They guide the agent and make
review expectations explicit; they do not prove chronology, semantic adequacy,
reviewer independence, scope fidelity, or staged ownership.

## Codex Rules

Tuxedo ships `templates/codex/tuxedo.rules` as an optional project template.
Copy it to `.codex/rules/tuxedo.rules` in a trusted project and restart Codex.

For the exact standard command forms listed in the template, it:

- forbids a narrow set of broad recursive deletions;
- prompts before push, destructive Git cleanup, release, package publication,
  deployment, cluster mutation, and infrastructure mutation;
- includes `match` and `not_match` examples validated by Codex.

Rules do not validate TDD order, task scope, review quality, test adequacy, or
commit ownership. Absolute executables, wrappers, global options, and complex
shell programs can fall outside literal prefix coverage. Sandbox, project
trust, approval configuration, and organizational policy remain authoritative.

## Real-task observation protocol

Before reconsidering lifecycle enforcement, evaluate **10–20 real tasks** with
the declarative workflow and record only observed events:

| Failure category | Record when |
| --- | --- |
| Implementation before oracle | Production behavior changes before a suitable fail-first oracle is defined and run. |
| Scope expansion | Files or behavior outside the authorized task are changed. |
| Implementation-aware weak test | A test is shaped to accept the implementation rather than prove the spec. |
| Missing review | Completion is claimed without the required reconstructed review phases. |
| Unrelated staged content | The commit candidate includes changes not owned by the task. |
| Unauthorized additional work | A newly discovered task begins without user authority. |

Do not count a corrected hesitation or a false alarm as a failure. Preserve the
task, client, relevant workflow stage, observable consequence, and whether an
existing test, Rule, approval, or human review already caught it.

Record trials in the [declarative workflow trial log](../evidence/declarative-workflow-trials.md).

## Reintroducing a gate

A future hook is justified only when a failure recurs, the invariant is
mechanically observable, false-positive and false-negative cases can be tested,
and the solution neither mutates the consumer checkout nor introduces an
installed runtime dependency. Semantic judgments remain in specs, skills,
reviews, tests, and human authority.
