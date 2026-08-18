---
name: measurer
description: Classify software work by risk, boundaries, reversibility, ambiguity, validation difficulty, and rollout exposure, then route only the proportional refinement, documentation, and review depth. Use implicitly at the start of software implementation, repair, review, or delivery work; do not use line count as a size proxy or create persistent planning artifacts.
---

# Measurer

Classify the highest applicable risk before work begins. Do not reopen clear decisions or ask about reversible details.

1. Inspect the governing input and nearby repository evidence.
2. Preserve an explicitly requested activity phase: route divergent exploration to `brainstorming`, current external technical evidence to `technical-research`, semantic reconciliation to `shape-domain`, and a pause or handoff to `session-bridge`. Topic overlap with security, documentation, or ambiguity does not replace the requested owner.
   Keep that owner selected when evidence access or execution authority is unavailable; the owning workflow reports the gap.
3. Set `size` to `S`, `M`, `L`, or `XL` from blast radius, crossed boundaries, reversibility, ambiguity, persistence, public compatibility, sensitive domains, validation difficulty, rollout, and rollback.
4. Require `refine` only when material ambiguity leaves incompatible behavior, scope, constraints, or authority unresolved.
5. Select the smallest durable documentation needed and the proportional review depth. An accepted hard-to-reverse decision uses an ADR; rollback uncertainty alone does not make it an open RFC. An `L` or `XL` task does not automatically require refinement or every documentation type.
6. Load [classification guidance](./references/classification.md) only when classification is uncertain or resolves to `L` or `XL`.

Return exactly one valid JSON object with no text before or after it. Use only `size`, `drivers`, `refine`, `documentation`, and `review`. `refine` contains `required` and contains `reason` only when required is true. Documentation entries contain only `type` (`rfc`, `adr`, `c4`, `api`, `operations`, or `postmortem`) and `timing` (`before-implementation`, `during-implementation`, or `after-incident`). Review is `inline`, `focused`, `expanded`, or `independent`.

Keep drivers and reason concise. Keep the result only in the conversation. Do not create, write, or save a file, artifact, persistent plan, or specification.
