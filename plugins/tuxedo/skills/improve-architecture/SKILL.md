---
name: improve-architecture
description: Audit a codebase for evidence-backed architecture improvements, leverage, seams, locality, and reversibility. Use when the user explicitly requests an assessment of the existing architecture, including when the request defers new module-boundary design; do not implement changes, create a refactor spec, or infer broad authority from the audit.
---

# Improve Architecture

1. Establish requested area, business goal, pain, exclusions, authority, and evidence threshold. Read the governing input, vocabulary, tests, dependency direction, and recent relevant change history.
2. Trace representative behavior end to end. Look for scattered invariants, coordination-heavy callers, leaky adapters, duplicated policy, hidden ownership, unstable surfaces, weak seams, implementation-coupled tests, and low locality.
3. Use `shape-domain` when responsibility or language is unclear and `design-deep-modules` when comparing interfaces.
4. Support every opportunity with paths, behavior, repeated change pattern, failure mode, test limitation, or measured cost. Aesthetic preference is not architecture evidence.
5. Compare a credible leave-as-is option. Rank by leverage, risk, reversibility, migration cost, and evidence strength.
6. Load [architecture diagrams](./references/architecture-diagrams.md) only when relationships are materially clearer visually. Show dependencies, seams, and direction of change in Mermaid; never emit interactive HTML.
7. For the leading opportunity, describe preserved contracts, alternative interfaces, dependency placement, reversible slices, test seams, rollback, authority, and residual risk.

Return `Evidence`, `Impact`, `Boundary options`, `Leverage`, `Risk and reversibility`, and `Validation`. Separate correctness defects and route them to `bugfix`. Do not edit production code without a separate authorization.
