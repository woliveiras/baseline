# SPEC-0001 test review

Context reconstructed from SPEC-0001, its behavior matrix, the fail-first output, and the three new structure tests. The new implementation was excluded as a justification.

## Findings

The initial tests proved named paths and public claims but did not independently establish the future-hook criteria or the complete observation taxonomy. The tests were strengthened to inspect installed Python/UV surfaces, ADR reintroduction requirements, the real-task trial log, and all six failure categories.

No actionable finding remains. A plausible wrong implementation that merely removes `hooks/hooks.json` while retaining the launcher elsewhere, manifest capability, receipt assets, or enforcement claims fails at least one oracle. Deterministic tests cannot prove that agents follow declarative instructions; SPEC-0001 records that as an empirical limitation.

## Decision

Approved for code review after the strengthened tests pass and the full deterministic suite remains green.
