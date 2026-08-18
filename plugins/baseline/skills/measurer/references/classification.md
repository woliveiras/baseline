# Proportional classification

Classify by the highest applicable risk or boundary, never by line count or textual volume.

| Size | Typical boundary |
| --- | --- |
| `S` | Localized change in one unit or function; clear behavior; trivial rollback; no public contract, persistence, or sensitive risk. |
| `M` | Multiple files inside one established boundary; reversible behavior; nearby validation; no durable architectural decision. |
| `L` | Multiple modules or boundaries; public contract; schema, serialization, persistence, concurrency, integration, compatibility, durable architecture, security, or significant rollout. |
| `XL` | Cross-system or cross-context change; irreversible migration or unproven rollback; data loss; structural authentication or authorization; money, compliance, retention, production, release, publication, platform migration, or material vendor lock-in. |

## Difficult classifications

- A one-line authorization-default change can be `XL` because it changes a structural security boundary across production consumers.
- When that authorization behavior is already accepted, select an ADR before implementation rather than an RFC: rollback uncertainty raises risk but does not reopen the decision. Use an RFC only while materially different behaviors remain open.
- A mechanical rename spanning hundreds of lines can be `M` when it stays within one boundary, preserves behavior, has deterministic validation, and is easy to revert.
- Text size does not determine risk. Promote for blast radius, compatibility, sensitive data, rollout, rollback, or hard-to-observe failure even when the diff is tiny.
- A completely defined `L` or `XL` task can proceed without `refine`. A conflicting `S` or `M` request can require `refine`.

## Documentation timing

- Use an RFC before implementation while a material decision remains open.
- Use an ADR when an accepted hard-to-reverse decision must survive the task.
- Use C4 or architecture documentation when boundaries and responsibilities stabilize.
- Synchronize API or operations documentation during implementation as shipped behavior becomes authoritative.
- Use a postmortem after an incident with material user impact, data loss, security impact, manual recovery, unavailability, or a consequential detection failure.

Select only the smallest durable artifact that preserves knowledge unavailable from code, tests, or existing documentation.

## Examples

```json
{
  "size": "XL",
  "drivers": ["authorization", "production-blast-radius"],
  "refine": {
    "required": false
  },
  "documentation": [
    {
      "type": "adr",
      "timing": "before-implementation"
    }
  ],
  "review": "independent"
}
```

```json
{
  "size": "M",
  "drivers": ["mechanical-rename", "reversible"],
  "refine": {
    "required": true,
    "reason": "Two public naming contracts conflict."
  },
  "documentation": [],
  "review": "focused"
}
```
