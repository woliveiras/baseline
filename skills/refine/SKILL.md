---
name: refine
description: Resolve material ambiguity in a software request with a proportional decision tree. Use before specification or implementation when objective, behavior, scope, authority, or risk decisions are genuinely unresolved; do not replace explicit brainstorming while the user still requests divergent exploration, and do not use when repository evidence already makes the path clear.
---

# Refine

Turn an ambiguous request into a decision-ready input without making routine work conversationally dependent.

1. Read the request, nearest instructions, existing specs, domain artifacts, code, and tests that can answer questions cheaply.
2. List only decisions that can change observable behavior, scope, authority, compatibility, or a hard-to-reverse boundary.
3. Build the decision tree in [decision tree](./references/decision-tree.md). Record dependencies so downstream questions wait for upstream answers.
4. Resolve branches from evidence. State each inference and its source.
5. Ask one focused question only when two or more materially different paths remain. Explain the consequence of each path without steering through invented certainty.
6. Update the governing PRD, spec, or decision artifact when authorized. Give stabilized criteria or decisions stable identifiers.
7. When an approved and sufficient governing input already defines the work, do not reopen accepted decisions or act as an approval owner. Stop and route directly to the applicable implementation or review workflow.
8. Stop refining when the objective, exclusions, criteria, constraints, authority, and next verification seam are sufficient for the current risk tier.

Continue autonomously when evidence is sufficient. Do not ask about reversible implementation details that can be selected and tested inside the approved objective. Escalate again only when new evidence changes the objective, exposes a contradiction, or crosses withheld authority.

Output `Resolved`, `Assumptions`, `Open decision`, `Decision dependencies`, `Authority`, and `Ready next step`. If nothing material is ambiguous, say so and route directly to the appropriate workflow.
