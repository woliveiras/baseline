# SPEC-0008 specification review

## Review boundary

This phase reviewed the user's authorized release-bootstrap outcome, the complete
SPEC-0008 text, and the superseded assumptions identified from SPEC-0005. Tests,
workflow implementation, and resulting command output were excluded as
justification.

## Spec

- The product boundary is one Tuxedo version, not a version per skill and not a
  version encoded in the `tuxedo@tuxedo` selector.
- The bootstrap from an already-declared plugin `0.1.0` to the first `v0.1.0`
  release is explicit; future releases are separate human merge decisions.
- Stable installation, pre-1.0 increments, no-npm publication, rollback, and
  tag immutability have observable acceptance criteria.
- SPEC-0008 supersedes only the mutable-main/no-tag and private-repository
  assumptions of SPEC-0005. It does not rewrite that earlier governing record.

## Standards

- The change is correctly classified `large/high-risk` because it mutates
  publication and branch-protection surfaces.
- The matrix assigns stable `RV-*` IDs and includes spec-derived, independent,
  and external oracles.
- Release, tag, push, merge, branch protection, and clean-room installation are
  explicitly granted by the user's selected bootstrap request; model calls,
  npm publication, history rewriting, and unrelated destructive actions remain
  excluded.

## Risk

- Correction made during this phase: the archive note now names the Git tag
  object ID rather than implying that the tag is cryptographically signed.
- Residual risk: RV-010's first empirical Release Please feature bump can occur
  only after bootstrap; current confidence comes from the pinned official
  action/config contract and must be replaced with live evidence on the first
  post-bootstrap `feat`.

No blocking specification finding remains.
