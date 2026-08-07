# SPEC-0004 spec review

## Review boundary

Reviewed the user request, the initial clean-room observations, SPEC-0004, its matrix, and the current OpenAI Codex plugin packaging contract without using the implementation as justification.

## Spec

- The intent directly addresses the observed failure: the marketplace must name a package directory rather than the maintainer checkout root.
- The installed-content allowlist is explicit and cannot be expanded merely to make installation pass.
- Authentication isolation and model-effectiveness evidence remain separate from package installation.
- Finding corrected: the first intent sentence promised preservation of the old standalone path for users while CP-003 and README selected the canonical package path. The intent now preserves the root link for maintainer compatibility and directs users to the canonical path.

## Standards

- The selected `plugins/tuxedo/` plus `.agents/plugins/marketplace.json` layout follows the official repo-marketplace structure.
- A committed package root avoids generated artifacts, copy scripts, stale duplication, and consumer runtime dependencies.

## Risk

- Remaining scope is explicit: Codex desktop UI, non-Codex clients, and actual model adherence are not established by this spec.
- No unresolved spec finding remains.

## 2026-08-07 link-integrity amendment

### Review boundary

Reviewed the new link-integrity objective, CP-008/CP-009, the installed-content boundary, compatibility requirement, and explicit dependency and network constraints without consulting new tests or implementation.

### Spec

- CP-008 distinguishes containment from existence, so an existing path outside `plugins/tuxedo/` cannot satisfy the package contract.
- CP-009 makes heading anchors observable and keeps external reachability outside the deterministic oracle.
- Fragment-only and percent-encoded local references are specified as edge behavior; external URL content remains an explicit exclusion.

### Standards

- The change remains maintainer-only validation and adds no distributed file, package generator, consumer runtime, or dependency.
- CP-003 remains the compatibility contract: scanning through `skills/` must resolve to the canonical package without weakening confinement.

### Risk

- The amendment is medium because it strengthens a public installed-package contract and a compatibility seam, despite a localized implementation.
- No unresolved specification finding remains.
