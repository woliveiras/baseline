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
