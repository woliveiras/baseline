# Three-phase fidelity review

## 1. Spec review

Input: objective, criteria, domain, invariants, reproduction, and complete spec. Exclude tests, diff, and implementation. Output the behavior/oracle matrix and spec defects. When receipts are enabled, record the spec input hash and matrix output hash.

## 2. Test review

Input: approved spec, matrix, prior spec-review receipt, fail-first record, and tests. Exclude the new implementation. Verify criterion mapping, assertion strength, boundaries, negative paths, provenance, the recorded fail-first observation, and whether tests could pass a plausible wrong implementation. Record the test-tree, fail-first, and upstream hashes.

## 3. Code review

Input: spec, matrix, prior test-review receipt, tests, diff, structured test evidence, evidence artifact, and documentation decision. Record the test, implementation, test-evidence, evidence, documentation, and upstream review digests. Report separately:

- `Spec`: intended behavior and explicit exclusions.
- `Standards`: repository rules, vocabulary, architecture, compatibility, and docs.
- `Risk`: correctness, security, privacy, data loss, concurrency, rollback, and missing evidence.

Use this finding schema: `severity`, `location`, `claim`, `evidence`, `impact`, and `remediation direction`. Do not let one passing axis cancel a finding in another.

The receipt dependency chain makes stale or incomplete artifacts detectable at commit and completion gates. It cannot prove that a reviewer respected the declared context or that the artifacts are semantically sufficient.
