---
id: SPEC-0001
title: Validate the declarative workflow before adding lifecycle enforcement
summary: Remove Tuxedo lifecycle hooks and evaluate the strict AGENTS and skill workflow in real tasks before considering mechanical gates.
status: approved
scope:
  - distributed plugin surface
  - repository engineering contract
  - workflow documentation and deterministic tests
risk: medium
risk_domains: [compatibility, workflow-integrity]
reversibility: easy
change_surfaces: [AGENTS.md, skills, plugin manifest, hooks, templates, tests, docs]
contracts: [portable Agent Skills, no runtime dependency, fidelity chain, task authority]
review_policy: reconstructed-three-phase-review
test_provenance: [spec-derived, independent]
documentation: required
authority:
  granted: [local-edit, local-test, local-commit]
  withheld: [push, release, publish, deploy, production, destructive]
dependencies: []
---

# Intent

Tuxedo must first validate its strict declarative workflow in real engineering tasks. The distributed plugin must not install or execute lifecycle hooks, Python, UV, policies, receipts, or review-hash machinery in a consumer checkout during this experiment.

`AGENTS.md` and the skills remain responsible for workflow guidance. Codex Rules remain an optional command-authority layer. Tests and CI remain responsible for executable product behavior. None of those layers may be described as a mechanical lifecycle gate.

# Behavior and invariants

- Start from the authorized spec, task, or plan and do not silently expand it.
- Define the most economical observable test or oracle before production implementation for testable behavior.
- When a conventional unit test is not appropriate, define the relevant integration, contract, end-to-end, static, or inspection oracle and record why.
- Do not change unrelated files or begin another task without user authority.
- Before completion, reconstruct spec review, test review without the new implementation, and code review with the complete evidence.
- Before a local commit, inspect the staged candidate and include only task-owned changes.
- Treat these requirements as declarative instructions, not proof that chronology, reviewer independence, scope, or commit ownership was mechanically enforced.

# Acceptance criteria

- **DW-001** Given a Tuxedo plugin installation, when the installed surface is inspected, then it contains skills but no lifecycle hooks, hook launcher, consumer Python/UV runtime, policy template, completion receipt template, or review-receipt JSON assets.
- **DW-002** Given a material authorized task, when an agent follows the repository contract, then it defines a suitable fail-first oracle before production implementation, stays inside the authorized scope, performs the three reconstructed review phases, and inspects the staged candidate before committing.
- **DW-003** Given work that is not part of the authorized task, when the agent discovers it, then the agent leaves it unchanged and requests authority before beginning it.
- **DW-004** Given the absence of lifecycle hooks, when Tuxedo describes its guarantees, then it identifies AGENTS and skills as declarative guidance, Rules as optional command authority, and tests/CI as product evidence without claiming mechanical workflow enforcement.
- **DW-005** Given a future proposal for a hook, when it is evaluated, then it is deferred until real-task observations show a recurring mechanically detectable failure and the proposed gate does not introduce a runtime dependency or mutate the consumer checkout.
- **DW-006** Given the empirical experiment, when users assess 10–20 real repository tasks, then they record occurrences of implementation-before-oracle, unauthorized scope expansion, implementation-aware weak tests, missing review, unrelated staged content, and unauthorized additional work before deciding whether any hook is needed.

# Explicit exclusions

- Removing Codex Rules, sandboxing, approvals, tests, CI, skills, or the three-phase review workflow.
- Claiming that declarative instructions are unbreakable or equivalent to policy enforcement.
- Designing or retaining a dormant hook implementation for hypothetical future use.
- Running model evaluations solely because this contract changed; a fresh empirical suite requires separate authority when useful.

# Edge and failure scenarios

- Documentation, configuration, and research tasks may use a non-unit oracle; they must not invent a meaningless unit test.
- A pre-existing dirty worktree is preserved and excluded from the task-owned commit.
- A later discovered requirement is not automatically in scope.
- A future hook proposal that merely restates semantic judgment remains rejected even if a workflow failure recurs.

# Evidence and review

- Behavior matrix: [behavior-matrix.md](behavior-matrix.md)
- Evidence: [evidence.md](evidence.md)
- Spec review: [reviews/spec.md](reviews/spec.md)
- Test review: [reviews/tests.md](reviews/tests.md)
- Code review: [reviews/code.md](reviews/code.md)
