# Skill creator limitations log

This log records maintenance evidence before Tuxedo considers a catalog-governance skill.

## v0.1 observations

- The generic validator checks frontmatter shape and naming but does not detect overlap between 17 related engineering skills.
- It does not verify that `agents/openai.yaml` user-invocation policy matches the workflow's intended routing.
- It does not validate links, portability, cross-skill traceability, installed-content boundaries, or empirical claims.
- Generated scaffolds require domain-specific replacement and deterministic repository tests.

These are current observations, not yet evidence of recurring operational failure. Add a `govern-skill-catalog` capability only after real routing, overlap, distribution, traceability, or governance failures recur.
