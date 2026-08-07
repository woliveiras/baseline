---
id: SPEC-0005
title: Install Tuxedo from the GitHub marketplace without a local checkout
summary: Document and mechanically validate the supported remote marketplace lifecycle while preserving the maintainer clone flow.
status: approved
scope:
  - GitHub repository marketplace installation
  - optional sparse marketplace checkout
  - SSH access for private repositories
  - marketplace update and plugin lifecycle documentation
  - Codex and GitHub credential boundaries
  - deterministic documentation tests
risk: medium
risk_domains: [public-contract, compatibility, credential-safety]
reversibility: easy
change_surfaces: [README.md, docs/development.md, tests, specs]
contracts: [Codex plugin marketplace, GitHub Git transport, Tuxedo package boundary]
review_policy: separated-contexts
test_provenance: [spec-derived, external]
navigation:
  - README.md
  - docs/development.md
  - .agents/plugins/marketplace.json
  - plugins/tuxedo/.codex-plugin/plugin.json
  - tests/test_toolkit.py
documentation: required
authority:
  granted: [local-edit, deterministic-tests, local-commit]
  withheld: [plugin-installation, model-call, tag, release, publish, push, deploy, production, destructive]
dependencies: [SPEC-0004]
---

# Intent

Make the supported remote installation of Tuxedo explicit for a machine that
does not keep a local Tuxedo checkout. The GitHub repository is added as a
Codex marketplace snapshot, and the package named by that marketplace is then
installed with the normal plugin selector. Keep the local marketplace flow as
the maintainer's development path.

# Behavior and invariants

- The canonical remote flow is exactly `codex plugin marketplace add woliveiras/tuxedo --ref main` followed by `codex plugin add tuxedo@tuxedo-local`.
- The remote marketplace resolves the committed marketplace manifest, whose plugin source remains `./plugins/tuxedo`; a consumer does not need a Tuxedo checkout.
- Optional sparse checkout includes both `.agents/plugins/marketplace.json` and `plugins/tuxedo`; omitting either path is not a supported sparse recipe.
- A private repository may use an SSH Git URL such as `git@github.com:woliveiras/tuxedo.git`; GitHub access is configured through the machine's Git/SSH setup, not embedded in the command or repository.
- Updating the configured Git marketplace uses `codex plugin marketplace upgrade tuxedo-local`; refreshing the installed plugin uses the documented remove/add cycle.
- Reinstallation removes and adds `tuxedo@tuxedo-local`; complete removal removes the plugin before removing the `tuxedo-local` marketplace.
- Codex account authentication and GitHub repository authentication are separate concerns. Installing a public marketplace does not require a GitHub credential, and a private marketplace requires Git access independently of Codex account login.
- `main` is mutable and is the only documented ref because no Git tags are published yet. The flow does not claim immutable or reproducible source selection.
- The documented remote route never presents `codex plugin add <URL>` as a supported command. A marketplace source is added first, then a plugin selector is installed.
- No credential, token, private key, or credential-bearing URL belongs in commands committed to documentation or in the repository.

# Acceptance criteria

- **RM-001** README contains the exact remote marketplace command sequence and explains that it works without retaining a local Tuxedo checkout.
- **RM-002** README documents an optional sparse command containing both required paths: `.agents/plugins/marketplace.json` and `plugins/tuxedo`.
- **RM-003** README documents an SSH Git URL alternative for a private repository and states that GitHub access is configured outside the repository.
- **RM-004** README documents marketplace upgrade, plugin reinstallation, plugin removal, and marketplace removal in an executable order.
- **RM-005** README separates Codex account authentication from GitHub Git authentication and forbids credentials in URLs and repository content.
- **RM-006** README states that `main` is mutable, that Git tags are not published yet, and that direct `codex plugin add <URL>` is not the supported route.
- **RM-007** README and the development guide preserve the local clone flow as maintainer development workflow rather than presenting it as the remote installation requirement.
- **RM-008** Deterministic tests assert the exact commands, both sparse paths, lifecycle order, credential limitations, mutable-ref limitation, and absence of the unsupported direct-URL claim without installing the plugin, using the network, or calling a model.

# Explicit exclusions

- Installing or reinstalling Tuxedo in this change.
- Publishing a Git tag, GitHub release, marketplace publication, or any push.
- Running Codex models or claiming remote clean-room installation evidence.
- Adding a CLI, package manager, runtime dependency, authentication helper, or credential material.
- Claiming that `codex plugin add <URL>` installs a plugin directly.
- Claiming that `main` is immutable or that an unpublished tag exists.

# Edge and failure scenarios

- A consumer with a public repository can use the canonical shorthand without GitHub credentials; a private repository must use an authenticated Git transport such as SSH configured on that machine.
- A sparse checkout that omits either the marketplace manifest or the package directory cannot resolve the committed plugin source and is not documented as valid.
- After `marketplace upgrade`, an installed plugin cache may still need the remove/add cycle to refresh the package contents; the documentation keeps these operations distinct.
- Removing the marketplace before its installed plugin is an invalid lifecycle order; the documented removal sequence handles the plugin first.
- The absence of tags is a current repository limitation. A future immutable ref may be documented only after a tag is actually published and verified.

# Open decisions and assumptions

- The marketplace name remains `tuxedo-local` because that is the committed manifest name and selector used by the supported Codex flow, even when its snapshot was fetched from GitHub.
- The exact remote command is governed by the user request and cross-checked against the installed Codex CLI help; no remote install is authorized for this task.

# Evidence and review

- Behavior matrix: `behavior-matrix.md`
- Fail-first and passing evidence: `evidence.md`
- Documentation decision: required
- Spec review: `reviews/spec.md`
- Test review: `reviews/tests.md`
- Code review: `reviews/code.md`
