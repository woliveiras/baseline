# Scope tiers

Classify by the highest applicable condition. Risk promotes a change even when its diff is small.

| Tier | Boundary | Minimum evidence and review |
| --- | --- | --- |
| `trivial` | No observable behavior, contract, data, security, dependency, or runtime effect; examples are typo-only docs and proven mechanical formatting. | Focused validation; review may stay inline. |
| `small` | One localized behavior within one established boundary, easy rollback, no public contract or sensitive risk domain. | Criterion-linked oracle and one isolated reviewer across the three phases. |
| `medium` | Multiple modules, a public contract, schema/serialization, persistence, concurrency, compatibility, or a non-local dependency seam. | Explicit matrix, at least one spec-derived, independent, or external oracle, and separately reconstructed review contexts. |
| `large/high-risk` | Cross-context or broad architectural change, irreversible migration, unproven rollback, or security, privacy, authorization, data-loss, money, compliance, production, release, or publication exposure. | Independent phase reviewers when available, explicit rollback/residual risk, and the strongest relevant suite. |

When conditions disagree, use the higher tier. Line count never lowers the tier. A familiar implementation does not lower a sensitive risk domain.
