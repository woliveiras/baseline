# Review depth

Classify by the highest applicable risk or boundary, never line count.

| Size | Review |
| --- | --- |
| `S` | `inline`: inspect the localized change and run focused checks. |
| `M` | `focused`: review the complete task diff and run the nearby suite. |
| `L` | `expanded`: include architecture, public compatibility, rollout, rollback, and durable documentation. |
| `XL` | `independent`: use an independent reviewer when available, applicable specialists, and the strongest relevant validation. |

Every depth reports findings and residual risk in the final response rather than creating review files by default.
