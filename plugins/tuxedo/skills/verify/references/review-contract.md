# Three-phase fidelity review

## 1. Spec review

Input: objective, criteria, domain, invariants, reproduction, and complete spec. Exclude tests, diff, and implementation. Output the behavior/oracle matrix, context considered, and spec defects.

## 2. Test review

Input: approved spec, matrix, prior spec-review record, fail-first record, and tests. Exclude the new implementation. Verify criterion mapping, assertion strength, boundaries, negative paths, provenance, the recorded fail-first observation, and whether tests could pass a plausible wrong implementation. Record the context considered and findings.

## 3. Code review

Input: spec, matrix, prior test-review record, tests, diff, structured test evidence, evidence artifact, and documentation decision. Record the reviewed candidate, fresh commands, unavailable checks, and residual limitations. Report separately:

- `Spec`: intended behavior and explicit exclusions.
- `Standards`: repository rules, vocabulary, architecture, compatibility, and docs.
- `Risk`: correctness, security, privacy, data loss, concurrency, rollback, and missing evidence.

Use this finding schema: `severity`, `location`, `claim`, `evidence`, `impact`, and `remediation direction`. Do not let one passing axis cancel a finding in another.

Review records preserve the declared context and findings. They do not mechanically prove chronology, context isolation, or semantic sufficiency.
