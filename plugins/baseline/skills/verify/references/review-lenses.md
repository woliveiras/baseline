# Review lenses

Use two orthogonal questions without duplicating the workflow.

## Behavior lens

Does the candidate satisfy the governing input, expected behavior, explicit exclusions, domain invariants, and compatibility promises? Check whether tests express that behavior and whether a plausible wrong implementation could pass. A green test that encodes the wrong expectation is a behavior finding.

## Engineering lens

Even when behavior is correct, does the complete diff introduce avoidable architecture, security, privacy, data-loss, concurrency, operability, rollback, readability, or maintenance risk? Scope this lens to risks relevant to the change rather than applying a generic checklist mechanically.

The same reviewer applies both lenses by default. `inline` and `focused` review may combine them in concise findings. `expanded` review makes the lens behind each material finding explicit when that distinction improves actionability. `independent` means use an independent reviewer only when `measurer` selected that depth; the two lenses alone never require additional reviewers.

Order findings by severity and point to the tightest evidence. Do not duplicate one issue under both lenses or require a specification. Do not create a review file; return findings and residual risk in the final response as usual.

For a read-only review, state that the same reviewer applied both lenses, distinguish unavailable execution from fresh evidence, and end with the next valid behavior and engineering checks without claiming they ran or that files changed.
