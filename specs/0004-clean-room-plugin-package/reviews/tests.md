# SPEC-0004 test review

## Review boundary

Reviewed the new oracles against SPEC-0004 without treating the production layout as evidence that their expectations were correct.

## Spec

- Structural assertions prove the exact marketplace source, package top-level allowlist, absence of package symlinks, forbidden maintainer paths, one canonical skill tree, and all 17 skill names.
- The integration oracle invokes the real Codex CLI in empty temporary operating-system and Codex homes with both API-key variables removed.
- App Server `skills/list` proves that all 17 enabled `tuxedo:*` skills resolve from the installed cache, rather than merely existing in the checkout.
- Removal, empty installed state, and reinstallation cover repeatability.

## Standards

- Fail-first execution produced the expected two source-path failures before invoking the expensive old installation path.
- Finding corrected: the first passing run emitted three `ResourceWarning` messages for unclosed App Server pipes. The test now closes all streams and passes with `ResourceWarning` promoted to an error.
- A missing Codex CLI skips the external integration test but not the structural contract; this limitation is explicit in the spec.

## Risk

- The tests intentionally do not call a model and therefore cannot prove routing quality or instruction adherence.
- No assertion was weakened in response to the old package failure. No unresolved test finding remains.

## 2026-08-07 link-integrity amendment

### Review boundary

Reviewed CP-008/CP-009, the amended matrix, the recorded existence-only fail-first run, and the link fixtures without using the strengthened validator implementation as justification.

### Spec

- The fail-first set maps directly to the requested valid link, absent destination, `../` escape, valid anchor, absent anchor, and external URL behaviors.
- Additional fixtures cover fragment-only references, percent-decoded paths and fragments, and an encoded traversal, matching the specified edge behavior.
- The installed-package test enters through the root `skills/` compatibility symlink while passing the canonical plugin root as the confinement boundary.

### Standards

- Missing target, outside-package, and missing-anchor results are distinguishable, so one failure mode cannot satisfy another criterion accidentally.
- The external URL fixture points at an unreachable loopback endpoint and asserts that the standard-library connection seam is unused; it does not assert remote availability.
- Six core fixtures were present for fail-first evidence. The fragment-only and percent-encoded edge fixtures were added after implementation inspection and are classified as implementation-aware supplemental coverage.

### Risk

- Direct and percent-encoded traversal fixtures prevent a plausible string-prefix-only implementation from satisfying CP-008.
- The anchor fixtures cover deterministic heading lookup without claiming full CommonMark parsing or external fragment conformance.
- No unresolved test finding remains.
