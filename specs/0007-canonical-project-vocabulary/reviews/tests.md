# SPEC-0007 phase 2 review: tests without implementation

Date: 2026-08-08

## Review context

Reviewed the approved specification, behavior matrix, fail-first output, and
test source without consulting the candidate documentation or package changes.

## Spec

- The test directly parses the root and plugin manifests for TV-001 and TV-006.
- Glossary markers and the curated active-surface scan cover TV-002 and TV-003.
- Explicit user-authority markers cover TV-004 independently of generic term
  replacement.
- TV-005 is intentionally completed by diff and hash inspection because a test
  that treats historical language as forbidden would contradict the spec.

## Standards

- The first run failed before implementation on the old package identity:
  expected `tuxedo`, observed `tuxedo-maintainer-evals`.
- The retired-compound list targets known semantic misuse rather than banning
  the legitimate stewardship role.
- Whitespace is normalized only for prose marker assertions, so Markdown line
  wrapping cannot create a false failure.

## Risk

- The curated surface list requires review when a new active documentation or
  configuration surface is added. The repository-wide audit remains a review
  complement rather than an overly broad historical rewrite oracle.

No blocking test finding remains.
