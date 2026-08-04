# Three-phase fidelity review

## 1. Spec review

Input: objective, criteria, domain, invariants, reproduction, and complete spec. Exclude diff and implementation. Output the behavior/oracle matrix and spec defects.

## 2. Test review

Input: approved spec, matrix, and tests. Exclude the new implementation. Verify criterion mapping, assertion strength, boundaries, negative paths, provenance, and whether tests could pass a plausible wrong implementation.

## 3. Code review

Input: spec, matrix, tests, diff, and evidence. Report separately:

- `Spec`: intended behavior and explicit exclusions.
- `Standards`: repository rules, vocabulary, architecture, compatibility, and docs.
- `Risk`: correctness, security, privacy, data loss, concurrency, rollback, and missing evidence.

Use this finding schema: `severity`, `location`, `claim`, `evidence`, `impact`, and `remediation direction`. Do not let one passing axis cancel a finding in another.
