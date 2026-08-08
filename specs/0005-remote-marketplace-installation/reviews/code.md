# SPEC-0005 code review

## Review boundary

Reviewed the complete task-owned candidate against SPEC-0005, its matrix, the
fail-first and passing evidence, the documentation test, the README and
development-guide diff, the pre-existing catalog commit, and the ignored file
that remains outside the candidate.

## Spec

- README now gives the exact remote GitHub marketplace flow, optional sparse
  paths, SSH alternative, update/reinstall/removal lifecycle, separate auth
  boundaries, mutable-main/no-tags limitation, and direct-URL exclusion.
- The local clone flow remains explicit under maintainer development, while
  standalone skill installation remains available as a separate option.
- `.agents/plugins/marketplace.json` and the plugin manifest are unchanged; the
  remote flow therefore resolves the existing `./plugins/tuxedo` package.

## Standards

- The deterministic focused test passes, the filtered deterministic suite passes
  89/89, and the installed CLI help confirms the documented source forms,
  `--ref`, repeated `--sparse`, marketplace upgrade, and selector-only plugin
  add syntax.
- The official plugin validator passes, all 17 official skill validators pass,
  the eval dry-run generates 48 configurations without model calls, and
  `pnpm run promptfoo:validate` reports a valid configuration.
- No distributed plugin file, dependency, credential, tag, release, network
  operation, model call, or push was added. The pre-existing `0e6df59` catalog
  commit was not modified or absorbed into this candidate.
- The README's duplicate option label was reconciled to keep the local clone
  route and standalone skill route distinct.

## Risk

- Remote installation, private SSH access, Codex desktop behavior, and tag
  publication remain unexecuted and are not claimed as validated.
- Full unittest discovery was intentionally withheld because the available
  clean-room test would install the plugin, contrary to the user constraint;
  the filtered deterministic suite excluding that test is the applicable
  broader local check.
- No unresolved in-scope finding remains.

## Post-authorization amendment review

### Spec

- README now leads with the verified SSH route for the repository's current
  private state and conditions the HTTPS shorthand on the access it requires.
- The original exact shorthand and marketplace-first selector remain
  documented; the clarification does not invent direct URL plugin installation.

### Standards

- The focused RM-001–RM-009 documentation test passes after a valid fail-first
  run. The external SSH lifecycle installed only the package boundary,
  discovered all 17 enabled skills, removed, reinstalled, and cleaned final
  marketplace/plugin state without a model call.

### Risk

- Codex desktop remains unexecuted. `main` remains mutable, and SSH availability
  remains a machine-level GitHub configuration responsibility.

## 2026-08-08 marketplace identity reconciliation

### Review boundary

Reviewed the complete task-owned diff, reconciled specifications and matrix,
test-review record, fail-first and passing evidence, current documentation,
Codex CLI lifecycle output, installed content digests, and preserved pre-existing
ignored-file state.

### Spec

- No findings. The committed marketplace now identifies and displays only
  Tuxedo, while the plugin remains `tuxedo`; every maintained lifecycle command
  selects `tuxedo@tuxedo`.
- The local Codex state contains one configured `tuxedo` marketplace and one
  installed, enabled `tuxedo@tuxedo` plugin at version `0.1.0`. The retired
  empty cache directory is absent.

### Standards

- No findings. The change adds no runtime, dependency, package copy, generated
  distribution, authentication state, model call, remote mutation, or push.
- Official plugin validation, 17/17 skill validations, 91/91 unit tests, the
  48-configuration eval dry-run, shell applicability check, and diff check pass.
- Current installation docs contain no location-branded marketplace identity;
  two historical records retain the prior selector as observed evidence.

### Risk

- No in-scope findings. Source and installed package digests match, and the
  manifest SHA-256 matches exactly between checkout and cache.
- The remote GitHub marketplace still reflects the last pushed commit; the
  canonical name becomes remotely installable only after separately authorized
  push.
- The pre-existing ignored `.DS_Store` remains in both local source and installed
  package. It is outside the naming change and still causes package-boundary
  checks unless preserved outside the package for validation.
