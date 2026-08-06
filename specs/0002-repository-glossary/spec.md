---
id: SPEC-0002
title: Define the repository vocabulary
summary: Make Tuxedo's specialized workflow terms understandable without relying on assumed testing jargon.
status: approved
scope:
  - repository engineering contract
  - maintainer documentation
risk: medium
risk_domains: [documentation-contract]
reversibility: easy
change_surfaces: [AGENTS.md, GLOSSARY.md, README.md, docs/README.md, templates/spec, skills/spec/assets, skills/spec/references, skills/verify/assets, tests, specs/0002-repository-glossary]
contracts: [fidelity chain, declarative task flow]
review_policy: reconstructed-three-phase-review
test_provenance: [spec-derived]
documentation: required
authority:
  granted: [local-edit, local-test, local-commit]
  withheld: [push, release, publish, deploy, production, destructive]
dependencies: []
---

# Intent

An agent or maintainer reading Tuxedo's engineering contract must not need prior knowledge of testing theory to interpret specialized terms. The repository must provide one canonical glossary and link to it from the contract before using those terms as requirements.

# Acceptance criteria

- **GL-001** Given an agent reading `AGENTS.md`, when it encounters the fidelity chain, then it can follow a direct link to the root glossary.
- **GL-002** Given the term “oracle”, when an agent reads its definition, then it learns that an oracle is the expected observable result used to decide whether behavior is correct, that it must be derived independently of the new implementation where possible, and that a test is only one mechanism for evaluating it.
- **GL-003** Given the phrase “behavior/oracle matrix”, when an agent reads its definition, then it learns that the matrix maps each acceptance criterion and scenario to its invariant, observable oracle, provenance, planned verification, and evidence.
- **GL-004** Given adjacent Tuxedo workflow vocabulary, when an agent consults the glossary, then it distinguishes: acceptance criterion as obligation; invariant as rule; oracle as expected observable result; verification or test as the mechanism that evaluates an oracle; evidence as the record of what happened; provenance as the origin and implementation exposure of each oracle; fail-first as pre-implementation verification that fails for the expected reason; governing input as the authorized source of intent and scope; task-owned change as an authorized in-scope change; and three-phase review as deliberately separated information contexts.
- **GL-005** Given maintainer documentation, when its navigation is inspected, then the glossary is discoverable without first reading `AGENTS.md`.

# Explicit exclusions

- Replacing precise domain language with less accurate wording.
- Defining general software engineering terms that Tuxedo does not use as part of its workflow contract.
- Treating a passing test as proof that its oracle faithfully represents the governing requirement.

# Evidence and review

- Behavior matrix: [behavior-matrix.md](behavior-matrix.md)
- Evidence: [evidence.md](evidence.md)
- Spec review: [reviews/spec.md](reviews/spec.md)
- Test review: [reviews/tests.md](reviews/tests.md)
- Code review: [reviews/code.md](reviews/code.md)
