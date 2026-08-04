# Behavior and oracle matrix

Create the matrix during spec review, before exposing the reviewer to the new implementation.

| Criterion | Scenario | Invariant | Observable oracle | Provenance | Planned test | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | normal / edge / failure | | | spec-derived | | |

Allowed provenance: `spec-derived`, `independent`, `implementation-aware`, `external`, and `diagnostic-probe`. Medium and larger testable changes require at least one oracle from the first, second, or fourth category. A diagnostic probe can reproduce or localize a problem but does not establish the final contract by itself.
