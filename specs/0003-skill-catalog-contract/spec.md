---
id: SPEC-0003
title: Define the Tuxedo skill catalog contract
summary: Make skill ownership, composition, invocation, documentation assets, and Codex installation explicit.
status: approved
scope:
  - skills
  - catalog composition contract
  - routing evaluations
  - Codex installation documentation
  - documentation templates and CI references
risk: medium
risk_domains: [public-contract, compatibility, evaluation]
reversibility: easy
change_surfaces: [skills, agents-metadata, tests, evals, docs, templates]
contracts: [Agent Skills, Codex plugin, Tuxedo fidelity chain]
review_policy: separated-contexts
test_provenance: [spec-derived, external]
navigation:
  - skills/catalog.md
  - README.md
  - tests/test_toolkit.py
documentation: required
authority:
  granted: [local-edit, deterministic-tests, focused-routing-eval, full-eval, local-commits]
  withheld: [push, release, publish, deploy, production, destructive]
dependencies: []
---

# Intent

Make the 17-skill catalog predictable without merging useful workflows or adding a runtime state machine. A developer and an agent must be able to identify which skill owns each artifact, when skills compose, which workflow takes precedence, where each skill stops, and what happens when no skill fits.

Provide reusable documentation knowledge instead of command-only reminders, and make Codex installation and automatic skill selection reproducible and honest.

## Behavior and invariants

- The catalog contract is declarative guidance; it does not add hooks, a CLI, a daemon, or mechanical lifecycle enforcement.
- Every skill has one primary owner boundary, required input, output, precedence rule, stop condition, and fallback.
- Before acting, the agent reads every clearly applicable implicit skill and every explicitly invoked skill completely; it does not replace an applicable installed workflow with an unaided response.
- `spec` owns the canonical behavior/oracle matrix. `verify` reviews that matrix and may report corrections, but does not silently replace it.
- Boundary design generates concrete options; the decision workflow selects among material viable options when selection authority exists.
- Explicit-only workflows are never implicitly invoked by Codex metadata.
- A skill cannot grant itself authority to edit governing input, commit, publish, release, deploy, or perform other withheld work.
- Templates must not preselect a lower risk or review policy before classification.
- Installed skills remain portable and contain no consumer runtime dependency.

## Acceptance criteria

- **SC-001** The installed catalog defines owner, input, output, precedence, stop, and fallback for exactly all 17 distributed skills.
- **SC-002** Composition rules require applicable skills to be read before acting, define the normal change sequence, and resolve `spec` versus `verify`, `design-deep-modules` versus `decision-framework`, `refine` versus approved work, and CI versus security review without inventing an executable state machine.
- **SC-003** `premortem` and `technical-research` are explicit-only in Codex metadata; `premortem` proposes governing-artifact changes unless explicit write authority exists.
- **SC-004** `refine` cannot reopen approved decisions or become an approval owner; it stops and routes directly to the applicable workflow when evidence is sufficient.
- **SC-005** Spec templates require classification instead of defaulting to `small` and `single-isolated-reviewer`.
- **SC-006** `git-commit` remains an explicit-only portable skill, while `AGENTS.md` records the local Conventional Commits format and representative valid/invalid examples.
- **SC-007** The docs skill includes reusable MADR ADR, C4 project architecture, RFC, and blameless postmortem assets with primary-source provenance and selection guidance.
- **SC-008** The CI skill conditionally loads a GitHub Actions reference covering workflow syntax, least privilege, immutable action references, untrusted inputs, caches, artifacts, OIDC, and protected deployment authority.
- **SC-009** README documents verified Codex plugin and standalone-skill installation, discovery, implicit versus explicit invocation, updates/removal, and an honest client-support boundary.
- **SC-010** Routing tests include indirect prompts that do not name the expected skill and composition prompts where two skills legitimately apply; deterministic tests prove generated vars and assertions for both shapes.
- **SC-011** Historical audit findings remain intact and a later reconciliation records which findings SPEC-0003 closes, narrows, or leaves open.

## Explicit exclusions

- Removing or merging skills based only on the current audit.
- Adding lifecycle hooks or a runtime state machine.
- Claiming empirical cross-client installation or routing without clean-room evidence.
- Publishing a marketplace, plugin, release, or Git ref.

## Edge and failure scenarios

- If no skill description matches, the agent follows repository instructions and performs normal scoped work; it must not force a catalog workflow.
- If two skills apply, the contract identifies whether they run sequentially, one owns the artifact while another reviews it, or explicit invocation is required.
- If a user asks only for analysis, a skill must not convert a recommendation into an unauthorized repository edit.
- If a repository already has stronger ADR, architecture, RFC, postmortem, CI, or commit conventions, those local conventions take precedence.
- A cloned Tuxedo checkout alone is not described as an installed Codex plugin or standalone skill set.

## Open decisions and assumptions

- Keep all 17 skills until real-task evidence demonstrates recurring harmful overlap.
- Use a declarative transition table rather than a runtime state machine.
- Use the npm RFC structure as the lightweight general RFC basis, supplemented by Tuxedo risk, validation, migration, and rollback fields.
- Use Google SRE's blameless postmortem guidance as the postmortem basis.

## Evidence and review

- Behavior matrix: `behavior-matrix.md`
- Fail-first evidence: `evidence.md#fail-first`
- Documentation decision: required for installation, catalog behavior, templates, and audit reconciliation
- Spec review: `reviews/spec.md`
- Test review: `reviews/tests.md`
- Code review: `reviews/code.md`
