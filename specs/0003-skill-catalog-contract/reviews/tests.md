# SPEC-0003 phase 2 — test review

## Context boundary

Reviewed SPEC-0003, its matrix, fail-first record, and the tests without using the new implementation as justification. No independent reviewer process was available; the context was reconstructed manually.

## Spec

No actionable finding after correction. Tests map all 11 criteria: exact 17-skill inventory and six fields; overlap/authority language; explicit-only metadata; neutral spec defaults; Conventional Commit examples; documentation assets and sources; GitHub Actions security topics; Codex onboarding; indirect/composed generation; case-specific fixture; and historical reconciliation.

## Standards

One actionable test-design finding was corrected before this review: Promptfoo expands arrays in vars, so a list-valued `expected_skills` duplicated composed cases and broke the custom assertion. The oracle now transports a non-expanding string, parses it explicitly, proves both expected calls pass, and proves a missing second call fails.

The tests do not treat model text as proof of skill use. They require Codex SDK skill-call metadata through both the custom adapter and Promptfoo's blocking `skill-used` assertions.

## Risk

- Static tests prove source URLs and required template sections, not that external pages will remain available.
- Marketplace shape and validators do not prove clean-room installation on every Codex surface.
- Skill-call metadata is heuristic and does not prove that every loaded instruction changed the result.
- The original 5/6 result was preserved and investigated rather than retried until green. Dedicated operational trajectories proved two false negatives: a missing linked glossary made a compound skill-read command fail, and a macOS `/var` versus `/private/var` alias escaped the structural path matcher. Tests now require both fixture completeness and canonical provider roots; two fresh affected batches passed 6/6.

Verdict: deterministic oracles and focused empirical SC-010 approved; the complete evaluation remains separate evidence.
