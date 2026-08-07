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
