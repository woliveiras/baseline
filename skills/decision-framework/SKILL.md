---
name: decision-framework
description: Make a material software decision with explicit options, evidence types, uncertainty, dependencies, reversibility, and validation. Use when several viable paths remain after refinement; do not use to add ceremony to routine reversible choices.
---

# Decision Framework

1. State the decision, deadline, owner, scope, non-goals, and upstream decisions it depends on.
2. Extract decision drivers from the active spec, domain invariants, constraints, risks, and authority. Weight only when the weights reflect a real preference.
3. Compare materially different options, including leave-as-is when credible. Keep behavior and constraints constant.
4. Classify each supporting claim using [evidence types](./references/evidence-types.md). Separate empirical result, engineering heuristic, product decision, and community inspiration.
5. Evaluate consequence, uncertainty, reversibility, lock-in, migration, rollback, verification, and the cost of delaying the decision.
6. Seek the cheapest discriminating evidence for high-uncertainty, high-impact claims. Do not average away a veto constraint such as security, law, data loss, or withheld authority.
7. Select only when the active authority permits it. Record rationale, rejected options, assumptions, expiration/revisit triggers, and evidence plan in the spec or decision artifact.

Return a transparent matrix plus a narrative recommendation. Numbers organize judgment; they do not manufacture objectivity.
