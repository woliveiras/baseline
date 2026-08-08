---
id: SPEC-0008
title: Version and release Tuxedo as one product
summary: Establish one SemVer, protected CI-backed releases, an immutable Codex installation path, and a bootstrapped v0.1.0 release.
status: approved
scope:
  - root product version
  - plugin manifest version
  - changelog and release policy
  - GitHub Actions validation and Release Please automation
  - main branch protection
  - immutable Codex marketplace installation
  - initial Git tag and GitHub Release
risk: large/high-risk
risk_domains: [public-contract, compatibility, release, publication, supply-chain]
reversibility: moderate
change_surfaces: [package.json, plugin-manifest, release-config, workflows, tests, specs, docs, github-settings]
contracts: [Tuxedo product version, Codex plugin marketplace, GitHub release, protected main]
review_policy: independent-phases
test_provenance: [spec-derived, independent, external]
navigation:
  - package.json
  - plugins/tuxedo/.codex-plugin/plugin.json
  - release-please-config.json
  - .release-please-manifest.json
  - CHANGELOG.md
  - .github/workflows/ci.yml
  - .github/workflows/release-please.yml
  - docs/releases.md
  - README.md
documentation: required
authority:
  granted: [local-edit, deterministic-tests, local-commit, push, branch-protection, pull-request, merge, tag, github-release, clean-room-installation]
  withheld: [model-call, interactive-login, npm-publication, deploy, production, history-rewrite, unrelated-destructive]
dependencies: [SPEC-0004, SPEC-0005, SPEC-0007]
supersedes:
  - SPEC-0005 RM-006 mutable-main and no-tags installation limitation
  - SPEC-0005 RM-009 private-repository assumption
---

# Intent

Version Tuxedo as one product even though the repository contains development tooling and 17 independently routable skills. Publish immutable GitHub source releases without publishing the private Node package to npm. Make `tuxedo@tuxedo` remain the Codex `plugin@marketplace` selector while the separate plugin manifest reports the product SemVer.

Bootstrap the already-declared plugin version as `v0.1.0`, then let Release Please prepare subsequent version/changelog pull requests from Conventional Commits. A release remains a human merge decision and may occur only after the exact release candidate passes the protected validation contract.

# Behavior and invariants

- Tuxedo has one SemVer shared by root `package.json`, the plugin manifest, the Release Please manifest, the changelog heading, the Git tag, and the GitHub Release.
- The root Node package remains `private: true`; release automation never publishes npm, plugin registries, deployments, or generated consumer runtime artifacts.
- Release Please manages one root package named `tuxedo`, updates the plugin manifest as an extra JSON file, and creates `vX.Y.Z` tags without a component prefix.
- Before the first tag exists, `bootstrap-sha` excludes pre-bootstrap history. Release Please also updates the stable version markers in README.
- Before `1.0.0`, `fix` increments patch, `feat` increments minor, and a breaking Conventional Commit increments minor. Documentation, tests, CI, refactors, and chores do not request a release unless their commit deliberately carries a user-visible `fix` or `feat` contract.
- The first `v0.1.0` tag and GitHub Release are created explicitly after the bootstrap change reaches protected `main` with green CI. Release Please owns `v0.1.1`, `v0.2.0`, and later releases.
- Stable Codex installation pins an existing release tag. `main` remains available only as an explicitly mutable development channel.
- The `tuxedo@tuxedo` selector is not a version string: the first `tuxedo` is the plugin and the second is the marketplace. Version is reported separately by the installed manifest.
- Pull requests and pushes to `main` run deterministic validation with read-only permissions, no provider/model calls, no personal credentials, and no publication.
- The Release Please mutation job uses a full action commit SHA and only its required repository permissions. It does not check out or execute repository code with a write token.
- Because GitHub suppresses workflow events created by the built-in `GITHUB_TOKEN`, a separate read-only job validates the exact Release Please PR head. A final no-checkout job publishes only the required `Validate` commit status for that already-validated SHA.
- Protected `main` requires a pull request and the `Validate` status, applies to administrators, requires linear history and resolved conversations, and forbids force pushes and deletion.
- Release automation, CI helpers, specifications, tests, evaluations, and documentation stay outside `plugins/tuxedo/`; installed Tuxedo remains content-only.
- Version oracles compare the synchronized current version dynamically. Historical `0.1.0` documentation remains fixed evidence, but tests must accept a valid Release PR bump.

# Acceptance criteria

- **RV-001** Root package, plugin manifest, and Release Please manifest all declare `0.1.0` before bootstrap publication, then remain dynamically equal after every valid bump; a deterministic test rejects version drift without freezing one version.
- **RV-002** Release Please config owns exactly the root package, bounds initial history at the protected bootstrap merge, uses the Node strategy, creates `vX.Y.Z` tags without a component prefix, applies pre-1.0 minor rules, and updates the plugin manifest plus README version markers.
- **RV-003** `CHANGELOG.md` contains the initial `0.1.0` product entry, and durable release documentation defines SemVer/Conventional Commit rules, the human release boundary, rollback, and the no-npm boundary.
- **RV-004** README documents a stable public install pinned to `v0.1.0`, a complete immutable upgrade to a later tag, and a separately labeled mutable `main` development channel.
- **RV-005** CI runs the official plugin validator, every official skill validator, unit tests, evaluation dry-run, shell syntax checks, and Git cleanliness checks without model calls or write permissions.
- **RV-006** Release automation is pinned to Release Please `v5.0.0` by full SHA, uses least-privilege job permissions, never executes repository code with its write token, validates generated Release PR content under read-only credentials, and reports the result only for the resolved PR head SHA.
- **RV-007** The protected `main` branch requires pull requests and the `Validate` status, includes administrators, requires linear history/resolved conversations, and disallows force pushes and deletion.
- **RV-008** After bootstrap CI succeeds on `main`, tag `v0.1.0` and its GitHub Release point to the same commit; the release is not an npm publication.
- **RV-009** A clean Codex home installs `tuxedo@tuxedo` from `--ref v0.1.0`, discovers the distributed skills, and reports plugin version `0.1.0` without a model call or interactive login.
- **RV-010** A later `feat` commit produces a `0.2.0` Release PR whose merge is the explicit publication decision; later versions remain synchronized by the same contract.

# Explicit exclusions

- Publishing the private development package to npm or another package registry.
- Per-skill versions, tags, changelogs, packages, or releases.
- Running Promptfoo provider evaluations, calling a model, or logging into Codex.
- Deploying production infrastructure or adding a consumer runtime.
- Automatically merging Release Please pull requests.
- Rewriting existing history or moving a published tag.

# Edge and failure scenarios

- If any synchronized version differs, CI fails before release automation can publish a tag.
- If pre-bootstrap history is not bounded, Release Please may misclassify historical `feat` commits as an immediate new minor release; bootstrap stops and corrects the range rather than merging that PR.
- If Release Please creates or updates a PR but its exact head fails validation, the explicit `Validate` status is failure and protected `main` blocks merge.
- If the release mutation job gains a checkout or executes repository code, the security oracle fails because write-token isolation has been lost.
- If a `vX.Y.Z` tag or GitHub Release already exists at a different commit, bootstrap stops rather than moving or replacing it.
- If branch protection cannot be configured, the release does not proceed on an unprotected `main`.
- If the tag-pinned clean-room install fails, the GitHub Release is reported as incomplete evidence; no model call or credential workaround is allowed.
- GitHub-generated source archives are convenience downloads. The immutable release identity is the Git tag object ID plus the GitHub Release target commit; no reproducible archive checksum is claimed.

# Open decisions and assumptions

- `0.1.0` is the first public baseline because it is already the distributed plugin manifest version and no earlier tag or GitHub Release exists.
- Release Please's built-in `GITHUB_TOKEN` is intentionally retained with an isolated validation/status bridge instead of storing a personal PAT in repository secrets.
- The repository is public at bootstrap time; private forks may use their separately configured Git/SSH transport with the same tag.
- `1.0.0` requires a separate compatibility decision; this contract only fixes the pre-1.0 increment policy.

# Evidence and review

- Behavior matrix: `behavior-matrix.md`
- Fail-first and passing evidence: `evidence.md`
- Documentation decision: required
- Spec review: `reviews/spec.md`
- Test review: `reviews/tests.md`
- Code review: `reviews/code.md`
