---
name: premortem
description: Anticipate plausible failure modes for a proposed software change and convert them into proportional mitigations, criteria, detection, and rollback. Use before committing to medium or high-risk work; do not use to generate generic risk lists for trivial changes.
---

# Premortem

Assume the change has failed after release or handoff, then work backward from concrete consequences.

1. Read the active spec, behavior matrix, architecture, dependencies, authority, rollout, and reversibility.
2. Generate plausible failures across intent, domain, correctness, tests/oracles, compatibility, data, security/privacy, concurrency, operations, dependencies, and human process.
3. Write a causal chain for each material failure: trigger -> hidden condition -> propagation -> observable impact.
4. Rank likelihood, impact, detectability, reversibility, and evidence strength. Avoid precise probabilities without data.
5. Assign a proportional response: prevent, detect, contain, recover, accept, or investigate.
6. Propose stable criteria, tests, observability, rollout guards, rollback steps, or open decisions when justified. Edit the governing spec or another durable artifact only with explicit authority for that artifact; analysis alone grants no write authority.
7. Identify residual risk, owner, trigger, and authority required. Do not convert every recommendation into a blocking hook.

Return the highest-leverage failure modes first. Separate evidence-backed risks from speculative prompts and say what would reduce uncertainty.
