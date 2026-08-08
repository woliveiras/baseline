# Phase 2 review: tests without the new implementation

Date: 2026-08-07

## Review context

This review examined the acceptance criteria, behavior matrix, fail-first
outputs, and test source without treating the resolved lockfile as proof.

## Spec

- The external audit oracle covers DS-001 but cannot prove direct-version
  scope, exact parent-child resolution, documentation, or consumer isolation.
- The deterministic test separately checks those invariants and failed before
  implementation because the reviewed overrides were absent.

## Standards

- The test parses `package.json`, workspace policy, lockfile package keys and
  effective edges, ADR requirements, and Git-tracked plugin inventory.
- The existing real Codex clean-room test independently exercises the installed
  package boundary. The new test does not replace it.
- A local ignored `.DS_Store` initially caused the new package assertion to
  fail. The oracle was corrected to inspect Git-tracked product content, while
  the clean-room test still rejects extra installed content.

## Risk

- Lockfile text assertions intentionally couple the test to PNPM lock format;
  a future lockfile-format migration requires explicit test review.
- No test can prove compatibility of every unused provider or unexecuted native
  addon. Those remain documented limitations rather than softened assertions.

No blocking test finding remains.
