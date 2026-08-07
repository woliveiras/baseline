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
