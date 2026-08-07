# 07 — Findings

> Latest state at `8776a6a`: 22 open and 7 closed by scope removal. The details below preserve evidence from the original snapshot; see [10 — Reconciliation after removal](10-reconciliation-after-lifecycle-removal.md) for the current state and [09](09-reconciliation-2026-08-06.md) for the previous checkpoint.

Order: severity, dependency, and potential to invalidate other evidence. “Can be isolated” describes implementation, not authorization to change the repository.

## P1 — High

### TUX-AUD-001 — The catalog itself lacks a durable fidelity chain

- **Severity/confidence/category/status:** P1; high; architecture/traceability; confirmed.
- **Violated contract:** `AGENTS.md:7-17` and `README.md:9-20` require spec → matrix → tests → implementation → evidence → review with stable IDs.
- **Local evidence:** `git ls-files` contains no `specs/`, real AC/SPEC outside the templates, catalog matrix, evidence artifact, or review receipt. `templates/spec/*` provides only molds.
- **External evidence:** not required; this is an internal contract.
- **Explanation/impact:** `SKILL.md` simultaneously serves as intent and implementation. A reviewer cannot reconstruct phase 1 without reading the judged object; changes may silently redefine the contract.
- **Scenario:** change a skill's trigger/authority and adjust the corresponding textual test; no independent AC detects drift.
- **Likely cause:** migration prioritized distributable content and did not materialize receipts for its own creation.
- **Recommendation/files:** create a canonical catalog spec, ACs, oracle matrix, evidence/reviews; probably a new `specs/` surface or equivalent, with links from docs/tests.
- **Acceptance:** 17 skills and mechanisms mapped; one AC per public promise; every AC links oracle/test/eval/implementation/evidence/review; phase 1 is reconstructible without `SKILL.md`.
- **Validation:** link/schema checks, complete coverage matrix, three-phase review, and all required checks.
- **Order/dependency/residual/isolation:** `WP-01`, first; foundational for the others; structural presence still will not prove semantics; not isolable.

### TUX-AUD-002 — The hook launcher modifies the consumer project

- **Severity/confidence/category/status:** P1; high; hooks/runtime/portability; confirmed.
- **Violated contract:** “no runtime dependency” (`docs/development.md:7-11`) and a hook without network/implicit effects (`docs/architecture/enforcement.md:122-126`).
- **Local evidence:** `hooks/hooks.json:10-11,22-23` uses `uv run python`; `tests/test_toolkit.py:235-238` does not execute in the fixture's real cwd.
- **External evidence:** [UV `run`](https://docs.astral.sh/uv/concepts/projects/run/) syncs the project environment; [Codex hooks](https://developers.openai.com/codex/hooks) execute in the session cwd.
- **Explanation/impact:** UV participates in the consumer project before the guard. A no-policy probe created `.venv`/`uv.lock`; an invalid pyproject returned exit 2. It may download/build dependencies, alter the repository, and block Bash.
- **Scenario:** open a Python/UV project with the plugin active and run Bash without `.tuxedo/policy.json`.
- **Likely cause:** maintainer toolchain convention was applied to the consumer lifecycle.
- **Recommendation/files:** self-contained/isolated launcher, without project discovery/sync; `hooks/hooks.json`, a possible wrapper and tests; explicit `commandWindows`.
- **Acceptance:** valid/invalid/no-policy UV projects do not change any byte, create an environment/lock, or access an index; missing-runtime and Windows behavior is documented.
- **Validation:** E2E of the real hook definition with real cwd, before/after snapshot, and offline execution; required suites.
- **Order/dependency/residual/isolation:** `WP-02`, in parallel after AC; missing runtime still requires a policy; isolable.

### TUX-AUD-003 — The commit gate does not validate the staged Git index

- **Severity/confidence/category/status:** P1; high; integrity/Git; confirmed.
- **Violated contract:** verified staged slice in `skills/git-commit/SKILL.md:8-12`, `README.md:43-50`, and the enforcement commit gate.
- **Local evidence:** `guard.py:79-98,141-162,247-364` reads only the working tree; it does not read the index/cached diff.
- **Explanation/impact:** a probe with receipted working tree `VALUE=1` and index `VALUE=999` passed in PreToolUse and Stop. The commit may record unreviewed bytes.
- **Scenario:** stage malicious/old content, restore the approved working tree, and run `git commit`; `commit -a`/substitution expands TOCTOU.
- **Likely cause:** the “completion snapshot” was modeled as a filesystem, not as the trigger candidate.
- **Recommendation/files:** candidate snapshot abstraction; commit uses the Git index, Stop uses the working tree; `guard.py`, receipt schema, tests/docs.
- **Acceptance:** index != WT, staged deletion/rename/intent-to-add, and `commit -a` block or are explicitly outside the claim.
- **Validation:** temporary Git repositories and `git show :path`/tree hash; required checks.
- **Order/dependency/residual/isolation:** `WP-03`; depends on the candidate contract; residual shell TOCTOU must be documented; isolable after the decision.

### TUX-AUD-004 — Malformed policy may fail open or outside the protocol

- **Severity/confidence/category/status:** P1; high; security/fail-closed; confirmed.
- **Violated contract:** malformed/escaping inputs fail closed (`docs/architecture/enforcement.md:122-126`).
- **Local evidence:** `guard.py:247-251` uses `exists()` and policy does not pass through `resolve_inside`; `load_object` (`:56-65`) does not catch every `OSError`.
- **Explanation/impact:** a broken symlink disables the gate; an external symlink is read; a directory causes traceback exit 1, not JSON deny. Hook failure is not equivalent to a protocolized block.
- **Scenario:** the checkout contains a broken `.tuxedo/policy.json` or it is replaced with a directory/symlink.
- **Likely cause:** absence handling was confused with filesystem typing/error handling.
- **Recommendation/files:** `lstat`, regular-file check, containment, and symlink policy; catch filesystem errors and emit deny; `guard.py`/tests/docs.
- **Acceptance:** internal/external/broken symlinks, directories, FIFOs, unreadable paths, and removal races never silently allow or traceback.
- **Validation:** temporary type/error matrix and Codex protocol; required checks.
- **Order/dependency/residual/isolation:** `WP-04`; parallel; race between lstat/read remains residual until safe open; isolable.

### TUX-AUD-005 — Green results do not identify the complete snapshot

- **Severity/confidence/category/status:** P1; high; eval provenance; confirmed.
- **Violated contract:** task/fixture/provider/dependency upgrades require new evidence (`docs/architecture/evaluations.md:193-195`).
- **Local evidence:** `evals/run.py:279-286` hashes only `AGENTS.md + skills/**`; propagation is in `prepare-workspaces.py:183-196` and report handling in `run-evaluations.py:430-455`; the green full run in `docs/evidence/eval-runs.md:200-218` predates harness commits.
- **Explanation/impact:** tasks/assertions/runner may change while retaining the fingerprint. A later routing run with the same fingerprint failed 33/34.
- **Scenario:** fix the security oracle without touching skills; the old report appears current.
- **Likely cause:** a product fingerprint was used as the evaluation-system fingerprint.
- **Recommendation/files:** commit + dirty digest + canonical hash of tasks, fixtures, rubrics, configs, assertions, verifiers, runner, and resolved versions.
- **Acceptance:** any input/oracle change alters identity; report records commit/dirty state without secrets; evidence log marks incompatible history.
- **Validation:** mutation matrix for every input and cross-order deterministic hash; no model call.
- **Order/dependency/residual/isolation:** `WP-05`, before a new full run; identity does not prove oracle validity; partially isolable.

### TUX-AUD-006 — Security probes accept real violations

- **Severity/confidence/category/status:** P1; high; security eval validity; confirmed.
- **Violated contract:** a frozen probe requires a concrete stimulus and legitimate deterministic oracle (`AGENTS.md:78-80`).
- **Local evidence:** external paths require equality with a sentinel (`security.py:99-133`); the blacklist is short (`:114-120`); the canary is literal-only (`:182-191`); claims are in `security-regressions.yaml:36-44,124-132`.
- **Explanation/impact:** controlled probes did not detect `cat ~/.ssh/id_rsa` or base64 of the canary; `python`/`node` egress is not in the blacklist. 12/12 may be false positives.
- **Scenario:** conclude the canonical patch after reading the home directory; exfiltrate a transformed token; egress through Python.
- **Likely cause:** blacklist/sentinel checks approximate general authority.
- **Recommendation/files:** exact allowlist per fixture, reject every path outside the workspace, detect explicitly supported transformations, or reduce the claim.
- **Acceptance:** mutation tests for home/sibling paths, Python/Node, base64/hex, and unknown commands fail; documentation enumerates limits.
- **Validation:** assertion unit tests with synthetic trajectories; static security config; full run only afterward and with authority.
- **Order/dependency/residual/isolation:** `WP-06`, before a new full run; silent reads without trajectory remain unprovable; isolable.

### TUX-AUD-007 — Isolation accepts future surfaces and nested symlinks

- **Severity/confidence/category/status:** P1; high; eval isolation; confirmed.
- **Violated contract:** managed entries must be real and future surfaces must fail closed (`docs/architecture/eval-isolation.md:34-55`).
- **Local evidence:** `codex_auth.py:137-191` does not reject unknown top-level entries and checks symlinks only at the first levels.
- **Explanation/impact:** probes accepted `future-behavior-surface/` and a nested symlink in `skills/.system/.../personal-link`; content may contaminate behavior while preflight remains green.
- **Scenario:** Codex adds a behavior-bearing surface or an allowed cache contains a link to personal content.
- **Likely cause:** partial top-level denylist and non-recursive traversal.
- **Recommendation/files:** explicit top-level allowlist, recursive `lstat`, and cache shape/provenance validation; `codex_auth.py`/tests/docs.
- **Acceptance:** unknown files/directories/symlinks fail before auth status; a symlink at any depth fails.
- **Validation:** synthetic trees without touching the real dedicated home.
- **Order/dependency/residual/isolation:** `WP-07`; parallel; real cache still requires a trust decision; isolable.

### TUX-AUD-008 — Full can pass with missing or duplicate rows

- **Severity/confidence/category/status:** P1; high; eval aggregation/coverage; confirmed.
- **Violated contract:** full covers 34 routing, 40 behavior, and 12 security cases (`docs/architecture/evaluations.md:108-124`).
- **Local evidence:** raw validation does not check ID/cardinality (`run-evaluations.py:246-284`); aggregate concatenates/sums (`:606-641`); pass depends only on status (`:734-743,843-862`).
- **Explanation/impact:** one passing row per shard can produce passing aggregates with fewer than 86 trials; duplicate/wrong-provider is also not an infrastructure failure.
- **Scenario:** Promptfoo omits rows due to a filter/schema error, but reports the present rows as passing.
- **Likely cause:** runner trusts tool cardinality and validates response, not the expected matrix.
- **Recommendation/files:** expected `(test_id, provider, shard)` set, exact equality, uniqueness, and uniform fingerprints/controls.
- **Acceptance:** missing, duplicate, unknown, and wrong-provider/shard cases fail; full requires exactly 34/40/12.
- **Validation:** mutating raw-result fixtures and aggregate unit tests; no provider.
- **Order/dependency/residual/isolation:** `WP-08`, before full; does not prove row quality; isolable.

### TUX-AUD-009 — Legacy runner violates current isolation and sanitization

- **Severity/confidence/category/status:** P1; high; privacy/auth/duplicate harness; confirmed.
- **Violated contract:** dedicated home, removed API keys, and no persisted raw output (`AGENTS.md:58-64`).
- **Local evidence:** `docs/development.md:58-63` documents `--execute`; `evals/run.py:155-174,203-221` inherits the environment; `:232-246,385-403` writes answer/raw.
- **Explanation/impact:** an official path may use personal auth/home and persist prompts/output/stderr in an ignored-only directory.
- **Scenario:** a maintainer runs the documented command with secrets in the environment.
- **Likely cause:** the previous harness was preserved without control parity.
- **Recommendation/files:** disable execute or migrate fully to preflight/filtered environment/sanitized report; `evals/run.py`, docs/tests.
- **Acceptance:** no path inherits keys/homes; a synthetic secret is absent from child environment and disk; dry-run/verifiers are preserved.
- **Validation:** fake subprocess/fixture without model calls, plus temporary output scan.
- **Order/dependency/residual/isolation:** `WP-08`/sub-package; before any use; external-tool logs remain residual; isolable.

### TUX-AUD-010 — Receipts do not trace evidence by criterion

- **Severity/confidence/category/status:** P1; high; fidelity/enforcement; confirmed.
- **Violated contract:** stable IDs and `criterion → oracle → test → evidence` (`AGENTS.md:7-17`, `skills/tdd/SKILL.md:8-18`).
- **Local evidence:** `templates/policy/receipts.json:14-24` and `guard.py:199-219` have one global fail/passing pair; `templates/spec/evidence.md:3-13` requires AC rows. A fixture without AC and with `assert True` passes (`tests/test_toolkit.py:268-380,409-423`).
- **Explanation/impact:** a trivial proof satisfies a multi-criterion spec; hashes preserve bytes, not coverage.
- **Scenario:** five ACs, only one global test record; gate approves.
- **Likely cause:** receipt was optimized for artifact integrity, not cardinal traceability.
- **Recommendation/files:** unique IDs and criterion/test/fail/pass/evidence mapping in the receipt; validate structure without claiming semantics.
- **Acceptance:** missing/duplicate/unknown/uncovered cases block; every AC has oracle/provenance/test/evidence.
- **Validation:** negative matrix + schema compatibility/migration test.
- **Order/dependency/residual/isolation:** `WP-01` + `WP-03`; depends on the AC catalog; presence will still not prove quality; not fully isolable.

## P2 — Medium

### TUX-AUD-011 — Portability is format, not proven installation/behavior

- **Severity/confidence/category/status:** P2; high; portability/distribution; confirmed.
- **Contract:** portable toolkit (`README.md:3,57-65`).
- **Evidence:** checkout has `skills/`; evals allow explicit Codex layout and 7/17 behavior (`docs/architecture/evaluations.md:180-185`). Official docs for [Codex](https://developers.openai.com/codex/skills/), [Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), [Claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), and [OpenCode](https://opencode.ai/docs/skills) use distinct layouts/precedence.
- **Impact/scenario/cause:** a clone/copy does not auto-discover skills; cross-client routing/authority has no evidence; “portable” conflates format with operation.
- **Recommendation/files:** support matrix, install fixtures, and claims by level; README/docs/evals.
- **Acceptance/validation:** clean-room install/discovery plus minimum positive/negative routing in each claimed client; validator remains green.
- **Order/residual/isolation:** `WP-09`, after the contract; future versions may still drift; partially isolable.

### TUX-AUD-012 — Codex onboarding is not reproducible

- **Severity/confidence/category/status:** P2; high; docs/distribution; confirmed.
- **Contract/evidence:** README says it is sufficient (`README.md:5,33-41`), but “add to marketplace” gives no command/manifest/restart/update/removal; [OpenAI plugin docs](https://developers.openai.com/plugins/build/plugins) require concrete steps.
- **Impact/scenario/cause:** a new user depends on tacit knowledge; docs prioritized concept.
- **Recommendation/files:** copyable clean-room guide for add/install/restart/verify/hooks/rules/update/remove.
- **Acceptance/validation:** a third party follows it in a temporary home and confirms 17 skills/manifest without prior knowledge.
- **Order/residual/isolation:** `WP-09`; local marketplace depends on the Codex version; isolable after the distribution decision.

### TUX-AUD-013 — Explicit deep work diverges from `openai.yaml`

- **Severity/confidence/category/status:** P2; high; routing/authority; confirmed.
- **Contract/evidence:** `README.md:28,31`; `premortem/agents/openai.yaml:1-4` and `technical-research/agents/openai.yaml:1-4` omit `allow_implicit_invocation: false`, whose Codex default is true.
- **Impact/scenario/cause:** research/premortem may activate implicitly, expanding cost/scope; metadata drifted from the summary.
- **Recommendation/files:** set false or reclassify the README and routing cases.
- **Acceptance/validation:** metadata and docs agree; explicit/implicit positive/negative cases.
- **Order/residual/isolation:** `WP-09`; residual routing is heuristic; isolable.

### TUX-AUD-014 — There is no composition lifecycle/precedence

- **Severity/confidence/category/status:** P2; high; agent architecture; confirmed.
- **Contract/evidence:** flat list in `README.md:24-31`; `spec/SKILL.md:14` and `verify/SKILL.md:11` share the matrix; `tdd/SKILL.md:3,10` requires approved while the template starts as draft.
- **Impact/scenario/cause:** refine/spec/premortem/security/tdd/verify may compete; no approval owner/fallback exists; the catalog evolved through local skills.
- **Recommendation/files:** state machine with input/owner/output/status/precedence/stop/conflict/fallback.
- **Acceptance/validation:** normal, ambiguous, high-risk, finding/reopen, missing-skill, and deadlock scenarios have one verifiable route.
- **Order/residual/isolation:** `WP-09`, after AC; model selection remains heuristic; not isolable.

### TUX-AUD-015 — `premortem` may suggest writing without explicit authority

- **Severity/confidence/category/status:** P2; high; authority; grounded risk.
- **Contract/evidence:** `AGENTS.md:31-33` versus `skills/premortem/SKILL.md:15-16`, which directs adding criteria/tests/guards when “justified.”
- **Impact/scenario/cause:** standalone skill does not inherit AGENTS; an analytical request may become an edit; the cross-cutting boundary was not repeated.
- **Recommendation/files:** require explicit authorization; without it, propose only in the response/authorized artifact.
- **Acceptance/validation:** read-only eval proves zero writes and a blocking message; validator.
- **Order/residual/isolation:** `WP-09`; client still applies its own hierarchy; isolable.

### TUX-AUD-016 — Spec defaults induce under-classification

- **Severity/confidence/category/status:** P2; medium-high; templates/risk; grounded risk.
- **Contract/evidence:** higher-boundary tiers; `templates/spec/spec.md:7,12` and the asset use `risk: small`/single reviewer.
- **Impact/scenario/cause:** auth/data-loss may retain the default through inertia; the template chooses before analysis.
- **Recommendation/files:** placeholder/unresolved state and gate before ready; spec templates/ref/tests.
- **Acceptance/validation:** security/release/data-loss never accept small without rationale; negative cases.
- **Order/residual/isolation:** `WP-01`; risk semantics are not mechanically proven; isolable.

### TUX-AUD-017 — Spec/matrix/evidence roles may alias

- **Severity/confidence/category/status:** P2; high; receipt schema; confirmed.
- **Contract/evidence:** chain is separate in enforcement; `guard.py:263-272` requires strings/hash, not distinction; a one-file probe passed.
- **Impact/scenario/cause:** apparent separation is satisfied by one artifact; identity model uses textual paths.
- **Recommendation/files:** canonical paths and distinct identity, including symlink/hardlink handling.
- **Acceptance/validation:** repeated/`./` aliases/symlinks/hardlinks block.
- **Order/residual/isolation:** `WP-03`; distinct content may still be semantically duplicated; isolable.

### TUX-AUD-018 — Test/code review contexts are incompletely validated

- **Severity/confidence/category/status:** P2; high; review receipts; confirmed.
- **Contract/evidence:** templates require booleans; `guard.py:238-244` validates spec and only `implementation=false` in tests, nothing in code. Contrary probes passed.
- **Impact/scenario/cause:** receipt contradicts the official format but the gate approves; validator was implemented asymmetrically.
- **Recommendation/files:** exact shape/boolean validation per phase.
- **Acceptance/validation:** missing/extra key and wrong type/value fail in each phase.
- **Order/residual/isolation:** `WP-03`; declaration does not prove actual context; isolable.

### TUX-AUD-019 — Default policy blocks co-located tests

- **Severity/confidence/category/status:** P2; high; templates/usability; confirmed.
- **Contract/evidence:** test globs and `src/**/*` (`policy.json:8,12`) have overlap false (`:16`); `guard.py:297-302` blocks. `src/example.test.ts` reproduces it.
- **Impact/scenario/cause:** common Jest/Vitest layouts enter a Stop loop until policy is edited; defaults were combined without a co-located fixture.
- **Recommendation/files:** layout-specific defaults or exclude test patterns from the implementation tree.
- **Acceptance/validation:** separate Python, co-located TS, and monorepo layouts produce satisfiable scopes.
- **Order/residual/isolation:** `WP-04`; custom layouts remain configurable; isolable.

### TUX-AUD-020 — Rules claims exceed covered prefixes

- **Severity/confidence/category/status:** P2; high; command authority/docs; confirmed.
- **Contract/evidence:** summary `README.md:38`; rules `templates/codex/tuxedo.rules:6-124`; seven cases in `tests/test_toolkit.py:214-232`. Wrapper/options probes returned null.
- **Impact/scenario/cause:** README readers may treat a partial template as a boundary; literal prefix matching is not a shell parser.
- **Recommendation/files:** align claims, add an adversarial matrix, enumerate deliberate gaps; do not reimplement shell parsing.
- **Acceptance/validation:** every claim has an official positive/negative case; wrappers/options documented.
- **Order/residual/isolation:** `WP-04`; aliases/composed shell always limit Rules; isolable.

### TUX-AUD-021 — Result “shape validation” checks only extension

- **Severity/confidence/category/status:** P2; high; evidence retention; confirmed.
- **Contract/evidence:** docs claim shape (`evaluations.md:72-75`); `_validate_local_outputs` (`run-evaluations.py:123-144`) tests only suffix/type.
- **Impact/scenario/cause:** truncated JSON/raw payload may coexist as validated; function/document name exceeds the check.
- **Recommendation/files:** versioned schema, parsing, naming, forbidden fields, aggregate links/hashes.
- **Acceptance/validation:** malformed/wrong-schema/duplicate/raw-field cases fail without deleting evidence.
- **Order/residual/isolation:** `WP-05`; schema does not prove provenance; isolable.

### TUX-AUD-022 — Direct SDK is not the provider's effective version

- **Severity/confidence/category/status:** P2; high; dependency provenance; confirmed.
- **Contract/evidence:** root `0.146.0` (`package.json:23-25`); ADR says required; lockfile/Promptfoo provider resolves `0.144.6` (`pnpm-lock.yaml:6854-6955`). Reports do not record the effective SDK.
- **Impact/scenario/cause:** actual executor differs from the attributed version; root dependency may be redundant; transitive resolution is ignored.
- **Recommendation/files:** align/override/remove after compatibility check and record resolved-from-provider.
- **Acceptance/validation:** test resolves the package from Promptfoo and compares report/doc; frozen install.
- **Order/residual/isolation:** `WP-10`; requires authority for dependency update; isolable as a decision.

### TUX-AUD-023 — Minimum Python is not declared

- **Severity/confidence/category/status:** P2; high; toolchain/onboarding; confirmed.
- **Contract/evidence:** guide lists Node/UV/PNPM (`using-the-eval-harness.md:10-13`), but `codex_auth.py:16` uses `tomllib` (Python 3.11+); there is no pyproject/.python-version/preflight.
- **Impact/scenario/cause:** `uv run python` may resolve 3.10 and fail; the requirement remained implicit in the author's environment.
- **Recommendation/files:** declare and preflight Python >=3.11 without a runtime dependency.
- **Acceptance/validation:** command on 3.10 fails with a message before auth; supported version passes.
- **Order/residual/isolation:** `WP-10`; UV resolver selection varies; isolable.

### TUX-AUD-024 — Migration/provenance ledger is ignored and personal

- **Severity/confidence/category/status:** P2; high; provenance/maintainability; confirmed.
- **Contract/evidence:** README claims adaptation (`README.md:57-65`); evidence map cites the migration map (`:31`); `.gitignore:16` hides `docs/tmp/v0.1-map.md`, the only ledger of 49 capabilities and personal paths.
- **Impact/scenario/cause:** a clean clone loses disposition/inspiration/exclusion; the artifact was deliberately temporary and never promoted.
- **Recommendation/files:** tracked sanitized ledger with source URL/commit/license/disposition/nature.
- **Acceptance/validation:** every historical capability has a disposition; zero personal paths; link checker/provenance review.
- **Order/residual/isolation:** `WP-11`; source history may evolve, so pin the commit; isolable.

### TUX-AUD-025 — Dev graph retains advisories and unknown licenses

- **Severity/confidence/category/status:** P2; high for inventory, medium for exploitability; supply chain/license; grounded risk.
- **Contract/evidence:** current `pnpm audit`: 5 high/7 moderate/2 low; lockfile has 792 dev entries; aggregation found 1 LGPL and 3 Unknown. Direct dependencies are dev-only (`package.json:23-25`).
- **External evidence:** GitHub Advisory Database URLs in `06-*`.
- **Impact/scenario/cause:** maintainer evals process network/output/optional packages; specific exploitability was not proven; Promptfoo graph is broad.
- **Recommendation/files:** disposition each advisory, confirm packages actually loaded, resolve Unknown licenses, and update/override only with compatibility evidence.
- **Acceptance/validation:** zero high advisories without disposition/mitigation; effective graph and licenses recorded; validators/static evals continue to pass.
- **Order/residual/isolation:** `WP-10`; later provider run for compatibility requires authority; isolable as analysis, not necessarily as an upgrade.

### TUX-AUD-026 — Generic names may collide cross-client

- **Severity/confidence/category/status:** P2; medium; routing/portability; grounded risk.
- **Contract/evidence:** `docs`, `spec`, `verify`, `bugfix` in frontmatter; [Codex skills docs](https://developers.openai.com/codex/skills/) describe non-merging/precedence.
- **Impact/scenario/cause:** a same-named package may shadow/be shadowed; names favored local UX.
- **Recommendation/files:** prove per-client qualification/namespace or a naming/install strategy.
- **Acceptance/validation:** fixture with a competing skill deterministically selects the documented intent.
- **Order/residual/isolation:** `WP-09`; third-party catalogs change; depends on compatibility policy.

## P3 — Low

### TUX-AUD-027 — Evidence map does not record reproducible PDF provenance

- **Severity/confidence/category/status:** P3; high; research/docs; confirmed.
- **Contract/evidence:** `docs/research/evidence-map.md:3,39-43` has title/ID but no URL/date/hash/pages/method; `technical-research/SKILL.md:8-10` requires query/version/date/method/result/limitation.
- **Impact/scenario/cause:** another maintainer finds the preprint but cannot prove the examined bytes/section; the map summarized bibliography.
- **Recommendation/files:** direct URLs, version/date, SHA-256, pages/sections, and method.
- **Acceptance/validation:** fresh download matches hash/version or documents drift; links are valid.
- **Order/residual/isolation:** `WP-11`; arXiv versions may change; isolable.

### TUX-AUD-028 — Template copies do not declare a canonical source

- **Severity/confidence/category/status:** P3; medium; maintainability; opportunity.
- **Contract/evidence:** seven root/skill pairs are byte-identical; a test synchronizes them, but docs do not say which to edit first.
- **Impact/scenario/cause:** manual changes must be made on two surfaces; self-containment requires duplication, while canonicality remains implicit.
- **Recommendation/files:** declare a canonical source and test/generation contract while preserving the self-contained package.
- **Acceptance/validation:** one documented source/flow; drift test; complete selective package.
- **Order/residual/isolation:** `WP-11`; generation adds tooling if overdone; isolable.

### TUX-AUD-029 — `technical-research` does not declare network/fallback

- **Severity/confidence/category/status:** P3; medium; skill compatibility; opportunity.
- **Contract/evidence:** `technical-research/SKILL.md:8-14` requires current claims; `agents/openai.yaml:1-4` does not declare compatibility/dependency.
- **Impact/scenario/cause:** an offline client activates an impossible workflow or uses memory without marking it; external requirements remain implicit.
- **Recommendation/files:** compatibility/network requirement, offline stop/fallback, and evidence label.
- **Acceptance/validation:** offline scenario ends with a limitation, without inventing a current claim; online runs record sources.
- **Order/residual/isolation:** `WP-09`; external availability remains variable; isolable.

## Spec

Dominant finding: `TUX-AUD-001`. Before adjusting mechanisms, fix intent, ACs, and the legitimate strength of claims. Fixes must not edit specs to accommodate current behavior; staged candidate, fail-closed, cardinality, and security oracles require explicit decisions.

## Standards

Agent Skills are structurally conformant; plugin/skills passed the official validators. Current normative divergences are concentrated in operation: hook cwd/exit semantics, cross-client discovery/precedence, UV project behavior, Promptfoo result contracts, and supply-chain advisories. Primary sources are recorded in `01-*` and `06-*`.

## Risk

No P0 was identified. Distribution risk is nevertheless high: central gates have names/claims stronger than validated facts, and the empirical system may emit green without a valid snapshot/coverage/oracle. Until `WP-01`–`WP-08`, any release should treat hooks and eval evidence as experimental/conditional, not certification.
