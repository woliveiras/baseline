# SPEC-0003 behavior and oracle matrix

| Criterion | Scenario | Invariant | Observable oracle | Provenance | Planned verification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SC-001 | Catalog inventory | Exactly the distributed skills have complete contracts | Parsed catalog rows equal `EXPECTED_SKILLS`; all six contract fields are non-empty | spec-derived | unit test | pass in 74-test suite |
| SC-002 | Overlapping workflows | One owner per artifact and explicit composition | Contract and affected SKILL files state owner/consumer/precedence boundaries | spec-derived | semantic unit test | pass in 74-test suite |
| SC-003 | Explicit-only and premortem authority | Metadata cannot implicitly invoke explicit workflows; analysis cannot grant writes | Policies are false and premortem defaults to proposals | spec-derived | unit test | pass in 74-test suite and 17/17 validators |
| SC-004 | Refine before approved work | Refinement cannot block or re-approve ready work | Refine stops for approved, sufficient input and names no approval authority | independent | adversarial text test | pass in 74-test suite |
| SC-005 | Spec classification | No lower tier is preselected | Both canonical templates use unresolved placeholders and require classification | independent | synchronized-template unit test | pass in 74-test suite |
| SC-006 | Commit workflow | Portable procedure remains explicit and local contract is concrete | Metadata is false; AGENTS has format plus valid/invalid examples | spec-derived | unit test | pass in 74-test suite |
| SC-007 | Documentation assets | Templates are reusable and sourced | Four assets exist, are routed from docs skill, contain required sections and primary-source URLs | external | structural/semantic unit test | pass in 74-test suite and docs validator |
| SC-008 | GitHub Actions reference | GitHub-specific advice loads only for GitHub Actions | CI routing points to a sourced reference containing required security/evidence topics | external | structural/semantic unit test | pass in 74-test suite and skill validator |
| SC-009 | Codex onboarding | Clone, install, discovery, invocation, update, and removal are distinct | README documents plugin and standalone routes and does not claim clone-only discovery | external | semantic unit test | static pass; clean-room install not executed |
| SC-010 | Indirect and composition routing | Eval does not test only named invocation and can require multiple skills | Indirect requests omit names/paths; composition vars/assertions contain both expected skills | independent | generator unit test; focused Promptfoo cases | deterministic pass; provider batch 5/6, blocked |
| SC-011 | Audit history | Original report remains historical | New reconciliation exists; original audit table is not rewritten | spec-derived | Git diff inspection | pass; overlay added, original preserved |
