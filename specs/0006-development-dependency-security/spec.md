---
id: SPEC-0006
title: Remediate vulnerable development-only dependency paths
summary: Remove the 14 audited dev/optional advisories with narrow PNPM overrides while preserving direct provider versions and documenting compatibility limits.
status: approved
scope:
  - development-only Node dependency graph
  - PNPM overrides and committed lockfile
  - dependency audit and effective-resolution tests
  - Promptfoo evaluation harness compatibility checks
  - supply-chain decision and residual risk documentation
risk: large/high-risk
risk_domains: [security, supply-chain, dependency-compatibility, evaluation-integrity]
reversibility: easy
change_surfaces: [pnpm-workspace.yaml, pnpm-lock.yaml, tests/test_toolkit.py, docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md, specs/0006-development-dependency-security]
contracts: [development evaluation toolchain, committed lockfile, no consumer runtime dependency]
review_policy: reconstructed-three-phase-review
test_provenance: [spec-derived, external, diagnostic-probe]
documentation: required
authority:
  granted: [local-edit, dependency-resolution, local-install-without-scripts, local-test, local-commit]
  withheld: [native-build-approval, provider-call, model-call, eval-full, push, release, publish, deploy, production, destructive]
dependencies: []
---

# Intent

Remove the 14 advisories reproduced in the development-only PNPM graph without
upgrading unrelated direct dependencies or changing the distributed Tuxedo
plugin. Use explicit parent-scoped overrides because the current upstream
Promptfoo graph still requests vulnerable versions. Treat those overrides as a
reviewed compatibility exception, not as proof that cross-range substitution is
universally safe.

# Behavior and invariants

- `promptfoo` remains pinned at `0.122.0` and `@openai/codex-sdk` remains pinned at `0.146.0`; neither direct version change is necessary to remove the reproduced advisories.
- PNPM overrides are parent-scoped to the three vulnerable paths: `@ai-sdk/provider-utils>undici`, `@huggingface/transformers>sharp`, and `onnxruntime-node>adm-zip`.
- Effective resolutions are at least `undici@6.28.0`, `sharp@0.35.3`, and `adm-zip@0.6.0`, and the vulnerable locked versions are absent.
- Full and production dependency audits report zero advisories for the committed graph.
- A frozen install succeeds with lifecycle scripts disabled. This task does not approve or claim native build execution.
- Deterministic Tuxedo tests, official validators, eval dry-run, and Promptfoo configuration validation remain green without provider or model calls.
- The overrides affect development tooling only. The installed plugin remains limited to `.codex-plugin` and `skills` and gains no Node dependency.
- The decision record states why overrides were selected, which declared parent ranges they cross, how to remove them, and what remains unverified.

# Acceptance criteria

- **DS-001** Before remediation, `pnpm audit --json` reproduces exactly 14 advisories with 5 high, 7 moderate, 2 low, and zero critical findings; after remediation, full and production audits report zero.
- **DS-002** `package.json` keeps exact `promptfoo@0.122.0` and `@openai/codex-sdk@0.146.0`; no unrelated direct dependency is upgraded.
- **DS-003** `pnpm-workspace.yaml` contains exactly the three parent-scoped overrides and no implicit or placeholder native-build approvals.
- **DS-004** The committed lockfile resolves the three overridden paths to fixed versions and contains none of `undici@5.29.0`, `adm-zip@0.5.18`, or `sharp@0.34.5`.
- **DS-005** `pnpm install --frozen-lockfile --ignore-scripts` succeeds; native builds remain explicitly unverified rather than silently approved.
- **DS-006** The official plugin validator, all official skill validators, full deterministic unit discovery, eval dry-run, Promptfoo configuration validation, shell checks, and diff checks pass without provider/model execution.
- **DS-007** The ADR amendment records advisory reachability, direct and effective versions, package licenses/provenance, cross-range compatibility risk, override-removal conditions, and the native-build/provider limitations.
- **DS-008** Installed-package boundary tests prove the dependency remediation adds no consumer runtime content.

# Explicit exclusions

- Upgrading `@openai/codex-sdk`, Promptfoo, or other direct dependencies without a separate compatibility objective.
- Enabling Vercel AI Gateway, Hugging Face, Transformers, or any new provider.
- Approving or executing native package lifecycle scripts.
- Running providers, models, smoke, `eval:full`, red-team generation, login, or paid evaluation calls.
- Claiming that static validation proves native addons or every unused Promptfoo provider work with the overrides.
- Resolving the separate complete-license-inventory and effective-SDK-reporting findings beyond the nodes changed here.

# Edge and failure scenarios

- An audit can become green while a parent package remains incompatible with an overridden child. Harness checks reduce that risk only for Tuxedo's configured Codex path.
- A future Promptfoo graph may adopt fixed child ranges. The corresponding override must then be removed and the lockfile/audit evidence regenerated.
- Optional Hugging Face packages remain installed in the development graph even though Tuxedo does not configure their providers. Their native behavior is outside this task because scripts are disabled.
- A PNPM install that writes placeholder `allowBuilds` entries is not acceptable evidence; those entries are neither approval nor a deliberate deny policy.

# Evidence and review

- Behavior matrix: [behavior-matrix.md](behavior-matrix.md)
- Evidence: [evidence.md](evidence.md)
- Spec review: [reviews/spec.md](reviews/spec.md)
- Test review: [reviews/tests.md](reviews/tests.md)
- Code review: [reviews/code.md](reviews/code.md)
