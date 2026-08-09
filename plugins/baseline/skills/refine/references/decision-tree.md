# Decision tree

Use a compact tree or table. Do not create branches for every implementation choice.

| ID | Decision | Evidence | Depends on | Options and consequences | State |
| --- | --- | --- | --- | --- | --- |
| D-01 | Observable behavior | | none | A / B | resolved / open |

Order questions by dependency and information value:

1. Objective and actor outcome.
2. Conflicting behavior or invariant.
3. Scope and compatibility boundary.
4. Risk, reversibility, and evidence seam.
5. Authority that cannot be inferred.

Stop when every open branch is either immaterial to the current slice, safely reversible, or recorded as a bounded assumption. A question is justified only when its answer would select a materially different branch.
