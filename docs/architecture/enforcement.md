# Workflow and command boundaries

Baseline separates three responsibilities:

1. `AGENTS.md` and skills provide portable, declarative engineering guidance.
2. Tests and CI execute repository-specific checks and produce fresh results.
3. Optional Codex Rules govern a narrow set of direct command-authority decisions.

Baseline distributes no lifecycle hooks, launch scripts, chronology gate, scope monitor, review-file generator, or consumer runtime. Guidance cannot prove chronology, semantic adequacy, review independence, scope fidelity, or staged ownership.

## Proportional work

For a software task, the agent:

1. derives expected behavior, scope, constraints, and authority from the governing input;
2. uses `measurer` to classify the highest applicable risk, never line count;
3. invokes `refine` only when material ambiguity remains and records a durable decision only when its timing and reversibility justify it;
4. runs the smallest suitable verification fail-first before production behavior changes;
5. implements only the authorized task-owned behavior and synchronizes durable documentation when applicable;
6. reviews the governing input, expected behavior, tests, complete diff, relevant risks, fresh results, unrelated changes, rollback, and limitations at `inline`, `focused`, `expanded`, or `independent` depth;
7. performs a Git operation only when that operation is explicitly authorized.

A suitable verification can be unit, integration, contract, end-to-end, static, inspection, or another executable check at the real boundary. Documentation and configuration work must not add a meaningless unit test to satisfy a label. Baseline does not require a specification, behavior/oracle matrix, provenance record, evidence file, or review file.

## Codex Rules

Baseline ships `templates/codex/baseline.rules` as an optional project template. Copy it to `.codex/rules/baseline.rules` in a trusted project and restart Codex.

For the exact standard command forms listed in the template, it:

- forbids a narrow set of broad recursive deletions;
- prompts before push, destructive Git cleanup, release, package publication, deployment, selected direct remote database and project mutations, cluster and infrastructure mutation, and selected direct device mutations;
- includes `match` and `not_match` examples validated by Codex.

Rules do not validate TDD order, task scope, review quality, test adequacy, or commit ownership. Absolute executables, wrappers, global options, and complex shell programs can fall outside literal prefix coverage. Sandbox, project trust, approval configuration, and organizational policy remain authoritative. Because the most restrictive matching decision wins, non-mutating flags after a protected prefix can still prompt.

## Gate threshold

A future mechanical gate is justified only when a failure recurs, the invariant is objectively observable, false-positive and false-negative cases can be tested, and the solution neither mutates the consumer checkout nor introduces an installed runtime dependency. Semantic judgments remain in governing inputs, skills, tests, review, and human authority.

The development-only Promptfoo boundary is documented in [evaluation architecture](evaluations.md) and [ADR 0001](../decisions/0001-use-promptfoo-as-evaluation-orchestrator.md); the product boundary decision is [ADR 0003](../decisions/0003-separate-foundation-and-optional-sdd.md). Superseded experiments and outcomes remain available through Git history rather than the current documentation tree.
