# Phase 1 review: specification without implementation

Date: 2026-08-07

## Review context

This review considered the reproduced advisory inventory, the governing
evaluation ADR, WP-10 from the repository audit, and SPEC-0006 without using a
candidate code diff as justification.

## Spec

- The problem is a maintainer-only installed graph with 14 known advisories,
  not a consumer plugin runtime defect.
- Success requires both zero final advisories and explicit compatibility risk;
  scanner output alone cannot establish correctness.
- Updating the Codex SDK is outside the causal path and would introduce an
  unrelated provider compatibility change. Exact direct versions must remain.

## Standards

- Parent-scoped overrides are the narrowest available PNPM mechanism for the
  three paths and must be coupled to a frozen lockfile, provenance/license
  evidence, removal conditions, and deterministic graph assertions.
- Native build authority and provider/model execution are withheld. Their
  absence must be reported rather than inferred from static validation.

## Risk

- All three fixed versions cross a parent-declared range. The change is
  acceptable only as a documented temporary compatibility exception.
- Optional packages remain in Promptfoo's installed graph even when Tuxedo does
  not select their providers; omitting them from audit evidence would conceal
  supply-chain exposure.

No blocking specification finding remains.
