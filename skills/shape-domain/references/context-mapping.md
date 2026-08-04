# Context mapping

Use only when evidence shows multiple material domain contexts.

| Context | Owned behavior | Local terms | Upstream | Downstream | Contract | Translation | Open conflict |
| --- | --- | --- | --- | --- | --- | --- | --- |

For every cross-context operation, record direction, supplied fact/model/policy, consumer, compatibility, failure behavior, and where translation occurs. Direction can differ by operation. Sharing an identifier does not require sharing lifecycle or invariants. Keep translation at an explicit boundary and avoid leaking one context's internal model through ordinary callers.
