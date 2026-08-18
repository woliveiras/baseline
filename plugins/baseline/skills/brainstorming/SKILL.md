---
name: brainstorming
description: Explore a software problem space deeply before choosing a direction. Use when the user explicitly requests divergent investigation, materially different alternatives, hidden assumptions, or opportunity discovery, even without naming this skill; that request takes precedence over refine while exploration remains divergent. Do not trigger for ordinary clarification or implementation.
---

# Brainstorming

Treat this as divergent investigation, not a disguised implementation plan.

1. Establish the problem, desired outcomes, constraints, explicit non-goals, existing decision state, and what would make the exploration useful.
2. Separate known facts, assumptions, unknowns, and ideas. Do not turn community popularity into evidence.
3. Generate materially different approaches, including leaving the system unchanged. Vary responsibility, interface, workflow, and risk rather than renaming one design.
4. Stress each approach with domain invariants, edge scenarios, failure modes, reversibility, authority, and verification cost.
5. For a nebulous problem that needs iterative questioning or experiments, load [the bounded discovery frontier](./references/discovery-frontier.md).
6. Identify decisions that must precede others and the cheapest evidence that could collapse uncertainty.
7. Synthesize clusters, tensions, and promising experiments. Do not select a winner unless the user asks or the evidence and decision policy already authorize selection.
8. Feed stabilized intent into `refine` or the applicable decision/implementation workflow; keep speculative ideas out of approved behavior.

Return `Problem frame`, `Evidence and assumptions`, `Alternatives`, `Stress cases`, `Decision dependencies`, and `Next evidence`. Do not edit implementation unless separately authorized.
