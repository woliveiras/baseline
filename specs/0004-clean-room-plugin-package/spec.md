---
id: SPEC-0004
title: Package Tuxedo as an isolated Codex plugin
summary: Make local plugin installation copy only the distributed Tuxedo surface and prove it in a clean Codex home.
status: approved
scope:
  - Codex plugin package layout
  - local marketplace installation
  - clean-room discovery
  - installed Markdown link integrity
  - installation documentation
risk: medium
risk_domains: [public-contract, compatibility, installation]
reversibility: easy
change_surfaces: [plugins/tuxedo, skills, marketplace, tests, specs, docs]
contracts: [Codex plugin, Agent Skills, Tuxedo installed-content boundary]
review_policy: separated-contexts
test_provenance: [spec-derived, independent, external]
navigation:
  - plugins/tuxedo/.codex-plugin/plugin.json
  - .agents/plugins/marketplace.json
  - README.md
  - tests/test_toolkit.py
documentation: required
authority:
  granted: [local-edit, deterministic-tests, clean-room-installation, local-commit]
  withheld: [model-call, interactive-login, push, release, publish, deploy, production, destructive]
dependencies: [SPEC-0003]
---

# Intent

Install the complete Tuxedo plugin from a trusted checkout without copying maintainer-only files or dependencies into the Codex plugin cache. Preserve the root compatibility path for maintainer tooling while directing public standalone installation to the canonical packaged skill tree.

## Behavior and invariants

- `plugins/tuxedo/` is the canonical plugin package and contains only the manifest and distributed skills.
- The repository marketplace points to `./plugins/tuxedo`, following the Codex repo-marketplace layout.
- The root `skills/` path is a compatibility link to the canonical packaged skills; it is not a second copy or a generated artifact.
- Local plugin installation must not copy `node_modules/`, `evals/`, `specs/`, tests, maintainer documentation, repository configuration, or authentication state.
- Clean-room verification uses isolated operating-system and Codex homes, removes API-key variables, performs no login, and makes no model call.
- Installation, discovery, removal, and reinstallation use the installed Codex CLI rather than a simulated copy routine.
- Tuxedo remains a content-only plugin with no consumer runtime dependency or package-generation command.
- Deterministic package checks treat every local Markdown destination as confined to the installed package, require the destination file and referenced heading anchor to exist, and never fetch external URLs.

## Acceptance criteria

- **CP-001** The marketplace source is exactly `./plugins/tuxedo`, and that directory is the manifest-bearing package named `tuxedo`.
- **CP-002** The package top level contains only `.codex-plugin/` and `skills/`; it contains no symlink escaping the package and no maintainer-only or runtime dependency path.
- **CP-003** The root `skills/` path resolves to `plugins/tuxedo/skills`, so existing maintainer tooling uses the same canonical files while public standalone instructions name the canonical path directly.
- **CP-004** In empty temporary `HOME` and `CODEX_HOME` directories, `codex plugin marketplace add` and `codex plugin add tuxedo@tuxedo-local` succeed without authentication or API keys.
- **CP-005** Codex App Server `skills/list` reports exactly the 17 `tuxedo:*` skills from the installed cache, enabled with no discovery errors.
- **CP-006** `codex plugin remove` removes the installation and a subsequent `codex plugin add` reinstalls it successfully in the same clean room.
- **CP-007** README and maintainer documentation explain the package boundary, direct CLI installation, standalone installation, updates, removal, and the absence of a package-build step.
- **CP-008** Every local Markdown link in the installed package resolves to a file within `plugins/tuxedo/`; a path that escapes that boundary or names a missing destination fails validation.
- **CP-009** A local Markdown fragment resolves only when it matches a deterministic heading anchor in the destination document; external URLs are excluded from local resolution and are never accessed by the deterministic test.

## Explicit exclusions

- Executing a model or claiming empirical skill effectiveness from installation evidence.
- Logging into Codex, copying credentials, or reusing the personal or evaluation Codex homes.
- Testing Codex desktop UI or clients other than the installed Codex CLI.
- Publishing a plugin, marketplace, release, or Git ref.
- Adding a build script, generated package directory, runtime, or dependency to consumer projects.
- Establishing the availability, content, or fragment validity of an external URL.

## Edge and failure scenarios

- A missing Codex CLI skips only the CLI integration oracle; structural package tests remain mandatory.
- A clean-room subprocess timeout is a test failure, not permission to weaken package assertions or increase the installed-content allowlist.
- Codex-managed system skills may appear in `skills/list`; the Tuxedo assertion filters by the `tuxedo:` namespace and still requires exactly 17 entries.
- The clean room may create operational Codex databases and bundled system skills. They are outside the installed Tuxedo package and are not treated as contamination.
- A local checkout may contain ignored dependencies and evaluation results; none may enter the installed package.
- Fragment-only links target the current Markdown document. Percent-encoded local paths and fragments are decoded before filesystem and heading comparison.
- The compatibility `skills/` symlink may be used as the scan entry point, but containment is evaluated against its canonical `plugins/tuxedo/` package target.

## Open decisions and assumptions

- Symlinks are acceptable for the root compatibility path on the maintainer's supported macOS and Linux environments. The installed package itself contains real files.
- The plugin version remains `0.1.0`; this source-layout repair does not publish a release.

## Evidence and review

- Behavior matrix: `behavior-matrix.md`
- Fail-first evidence: `evidence.md#fail-first-evidence`
- Documentation decision: required
- Spec review: `reviews/spec.md`
- Test review: `reviews/tests.md`
- Code review: `reviews/code.md`
