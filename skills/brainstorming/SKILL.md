---
name: brainstorming
description: Explore a software problem space deeply before choosing a direction. Use only when the user explicitly invokes brainstorming for divergent investigation, alternatives, hidden assumptions, or opportunity discovery; do not trigger for ordinary clarification or implementation.
---

# Brainstorming

Treat this as divergent investigation, not a disguised implementation plan.

1. Establish the problem, desired outcomes, constraints, explicit non-goals, existing spec state, and what would make the exploration useful.
2. Separate known facts, assumptions, unknowns, and ideas. Do not turn community popularity into evidence.
3. Generate materially different approaches, including leaving the system unchanged. Vary responsibility, interface, workflow, and risk rather than renaming one design.
4. Stress each approach with domain invariants, edge scenarios, failure modes, reversibility, authority, and verification cost.
5. Identify decisions that must precede others and the cheapest evidence that could collapse uncertainty.
6. Synthesize clusters, tensions, and promising experiments. Do not select a winner unless the user asks or the evidence and decision policy already authorize selection.
7. Feed stabilized intent into `refine` or `spec`; keep speculative ideas out of approved criteria.

Return `Problem frame`, `Evidence and assumptions`, `Alternatives`, `Stress cases`, `Decision dependencies`, and `Next evidence`. Do not edit implementation unless separately authorized.
