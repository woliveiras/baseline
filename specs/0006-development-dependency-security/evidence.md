# SPEC-0006 evidence

Date: 2026-08-07

## Fail-first evidence

Before the remediation, `pnpm audit --json` exited nonzero and reported 14
advisories: five high, seven moderate, two low, and zero critical. Twelve
affected the mandatory `@ai-sdk/provider-utils -> undici@5.29.0` path; the two
remaining findings affected the optional
`@huggingface/transformers -> onnxruntime-node -> adm-zip@0.5.18` and
`@huggingface/transformers -> sharp@0.34.5` paths.

The new deterministic test was then executed before adding overrides:

```text
python3 -m unittest tests.test_toolkit.ToolkitStructureTests.test_maintainer_dependency_security_resolution -v
FAIL: expected three reviewed overrides, observed {}
```

This establishes failures from both the registry advisory source and the
spec-derived repository policy before implementation.

## Effective resolution and provenance

The direct versions and `package.json` digest remained unchanged:

| Package/file | Version or SHA-256 | Declared license | Recorded upstream |
| --- | --- | --- | --- |
| `promptfoo` | `0.122.0` | MIT | `promptfoo/promptfoo` |
| `@openai/codex-sdk` | `0.146.0` | Apache-2.0 | `openai/codex`, `sdk/typescript` |
| `package.json` | `d3ad191f2f14865a633025c8339ab6da269e330d0df9669b202fcd9fbb83ce39` | n/a | committed repository file |

Live npm metadata obtained through `pnpm view` records the changed nodes and
their parents as follows:

| Parent declaration | Effective child | Child license | Recorded upstream |
| --- | --- | --- | --- |
| `@ai-sdk/provider-utils@4.0.41`: `undici@^5.29.0` | `undici@6.28.0` | MIT | `nodejs/undici` |
| `@huggingface/transformers@4.2.0`: `sharp@^0.34.5` | `sharp@0.35.3` | Apache-2.0 | `lovell/sharp` |
| `onnxruntime-node@1.24.3`: `adm-zip@^0.5.16` | `adm-zip@0.6.0` | MIT | `cthackers/adm-zip` |

The parent packages declare Apache-2.0 for AI SDK provider utilities and
Transformers.js and MIT for ONNX Runtime Node. The committed lockfile retains
registry integrity hashes. Final file digests are:

```text
697ff95f927c87f2eec0fa2316411c42186154eceb1260b9112b0f59bbc1f657  pnpm-workspace.yaml
5c2e3c99d0f6776f74fc60619cc0d5a9b28c58723cb300bf9cd428a31506c810  pnpm-lock.yaml
```

## Verification results

| Criterion | Command or evidence | Result |
| --- | --- | --- |
| DS-001 | `pnpm audit --json` | pass; zero findings in 765 dev and 390 optional entries |
| DS-001 | `pnpm audit --prod --json` | pass; zero production dependencies and zero findings |
| DS-002–DS-004, DS-007–DS-008 | focused dependency policy test | pass |
| DS-005 | `pnpm install --frozen-lockfile --ignore-scripts` | pass; no lifecycle scripts authorized |
| DS-006 | official plugin validator with temporary `pyyaml==6.0.2` supplied by UV | pass |
| DS-006 | official skill validator for all 17 skills with the same temporary UV environment | pass |
| DS-006, DS-008 | `uv run python -m unittest discover -s tests -v` | pass; 91 tests including real clean-room install/remove/reinstall |
| DS-006 | `PYTHONDONTWRITEBYTECODE=1 uv run python evals/run.py --dry-run` | pass; 48 cases |
| DS-006 | `pnpm run promptfoo:validate` | pass; configuration valid |
| DS-006 | tracked shell syntax check | pass; no tracked shell scripts |
| DS-006 | `git diff --check` | pass |

The temporary `.DS_Store` in the local plugin directory was moved out only
while the clean-room unit suite ran and was restored afterward. The dependency
test evaluates the Git-tracked package boundary, so ignored local metadata is
not mistaken for distributed content.

## Residual limitations

- Every override crosses the range declared by its parent. Static loading,
  configuration validation, and deterministic tests do not prove every unused
  Promptfoo provider is compatible with those substitutions.
- Native lifecycle scripts were disabled. Sharp and ONNX native execution were
  not built or exercised and are not claimed as verified.
- No provider, model, paid evaluation, `eval:full`, push, release, or
  publication was executed.
- A zero registry advisory count is time-scoped evidence, not a permanent
  guarantee. Future audits and upstream range changes require a fresh review.

Reviews: [spec](reviews/spec.md), [tests](reviews/tests.md), and
[code](reviews/code.md).
