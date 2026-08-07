# Behavior and oracle matrix

Create the matrix as a separate artifact during spec review, before exposing the reviewer to tests or the new implementation. Use [the bundled template](../assets/behavior-matrix-template.md) when the project has no stronger format.

| Criterion | Scenario | Invariant | Observable oracle | Oracle provenance | Planned verification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AC-001 | normal / edge / failure | | | spec-derived | | |

Allowed oracle provenance: `spec-derived`, `independent`, `implementation-aware`, `external`, and `diagnostic-probe`. Medium and larger testable changes require at least one oracle from the first, second, or fourth category. A diagnostic probe can reproduce or localize a problem but does not establish the final contract by itself.
