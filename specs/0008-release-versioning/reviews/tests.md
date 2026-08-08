# SPEC-0008 test review

## Review boundary

This phase reviewed the new and reconciled test oracles against SPEC-0008 and
the behavior matrix without using the production workflow/configuration as the
source of expected behavior.

## Spec

- RV-001/RV-002 parse semantic JSON fields instead of relying on filename or
  prose presence alone.
- RV-003/RV-004 assert the durable increment, publication, immutable install,
  and selector-versus-version contracts.
- RV-005/RV-006 assert pinned dependencies, required commands, least privilege,
  write-token checkout isolation, and the exact generated-PR status bridge.
- Existing SPEC-0005 documentation oracles were reconciled only where
  SPEC-0008 explicitly supersedes their public/private and mutable-ref premises.

## Standards

- Fail-first execution produced three errors because the release manifest,
  config, changelog, and workflows did not exist. That is the expected missing
  behavior, not a syntax failure in the tests.
- The workflow oracle does not claim that static text proves GitHub execution;
  fresh Actions and API evidence remain required.
- Test formatting was made whitespace-tolerant for wrapped documentation while
  retaining exact semantic markers.

## Risk

- Finding corrected: the first validator loop used `skills/*`, which included
  `catalog.md`. The official validator printed `SKILL.md not found` but returned
  success, so the static test could have accepted incomplete validation. The
  workflow and oracle now require `skills/*/`, and an external simulation
  validated exactly 17 directories.
- Residual risk: static workflow tests cannot prove Actions expression or
  branch-protection behavior; `actionlint`, a real pull-request run, and GitHub
  API inspection provide those independent oracles.

No blocking test finding remains.
