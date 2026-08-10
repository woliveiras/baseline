# Releasing Baseline

Baseline has one product version for the complete plugin and all distributed
skills. Individual skills are independently routable and installable, but they
do not receive separate versions, changelogs, tags, or GitHub Releases.

The version is synchronized across `package.json`, `pyproject.toml`, the Baseline
entry in `uv.lock`, `plugins/baseline/plugin.json`,
`plugins/baseline/.codex-plugin/plugin.json`,
`plugins/baseline/.claude-plugin/plugin.json`,
`plugins/baseline/package.json`,
both version fields in `.github/plugin/marketplace.json`,
the plugin version in `.claude-plugin/marketplace.json`,
`.release-please-manifest.json`, `CHANGELOG.md`, the `vX.Y.Z` Git tag, and its
GitHub Release. The private Node package is never published to npm, and the
non-package Python project is never published to PyPI; both exist only for
repository development tooling. The private Pi descriptor inside the consumer
package is also never published to npm. Root `package.json` remains Release
Please's version source.

## Version rules before 1.0.0

Use Conventional Commits to describe the user-visible effect:

| Change | Version result |
| --- | --- |
| `fix` | increment the patch version |
| `feat` | increment the minor version |
| Breaking change before `1.0.0` | increment the minor version |
| `docs`, `test`, `ci`, `chore`, or `refactor` only | no release |

A documentation, test, CI, chore, or refactor commit that actually changes the
public product contract must use `fix` or `feat` deliberately. Do not add an
empty `fix`/`feat` merely to force a release. Reaching `1.0.0` requires a
separate compatibility decision.

## Automated flow

1. Every ordinary pull request runs the `Validate` check with read-only
   credentials.
2. After a merge to protected `main`, Release Please reads Conventional Commits
   since the latest release and creates or updates one Release PR.
3. GitHub suppresses ordinary workflow events for a PR created with the built-in
   `GITHUB_TOKEN`. The release workflow therefore resolves that PR's exact head
   SHA, validates it in a separate read-only job, and publishes only the
   resulting `Validate` commit status from a final no-checkout job.
4. The Release PR updates the shared versions and `CHANGELOG.md`. Review its
   complete diff and evidence. Release PR merge is the explicit publication
   decision; Release Please never auto-merges it.
5. After the protected merge, Release Please creates the `vX.Y.Z` tag and GitHub
   Release. That one immutable Git snapshot versions every manifest and the
   canonical skill tree atomically. No npm publish, deployment, generated
   client package, or consumer runtime artifact follows.

The committed Codex, Copilot, and Claude catalogs are product manifests that
select the same in-repository package. External marketplace submission,
enterprise catalog registration, package-registry publication, and support
claims remain distinct publication decisions. Creating the GitHub Release does
not perform or authorize any of them.

The write-token job never checks out or executes repository content. The
validation job has read-only repository permission and does not receive a
publication credential. Branch protection requires the same `Validate` context
for ordinary and generated pull requests.

## Release verification

Before merging a Release PR, require:

- synchronized version files and changelog;
- a schema-valid Agent Plugins manifest and native Codex and Claude manifests;
- synchronized Codex, Copilot, and Claude marketplace entries that resolve the canonical package;
- an exact Pi skill allowlist with no package scripts or dependencies;
- the protected `Validate` status on the exact candidate SHA;
- a task-owned diff with no unexpected installed-plugin content;
- confirmation that the proposed tag and GitHub Release do not already exist.

After publication, verify that the tag and GitHub Release target the same commit.
Install the Codex marketplace from the exact tag in disposable `HOME` and
`CODEX_HOME` directories, confirm `baseline@baseline` reports the released
version, and confirm all distributed skills are discovered. Validate the same
tagged package with the Agent Plugins schema and Claude validator, exercise the
Pi package allowlist and lifecycle, and exercise the Copilot and Claude
marketplaces after their configured sources resolve to the release commit.
Confirm marketplace add/list or browse, plugin install/update or reinstall,
disable/enable where supported, removal, installed version, and exact discovery.
Run Cursor lifecycle checks only when its client
is available. These checks perform no login or model call. If a client cannot
pin the exact tag or is not available, record that limitation instead of
promoting a static format result to lifecycle evidence.

## Rollback

Published tags and GitHub Releases are immutable history and are not moved or
silently replaced. If a release is defective, revert the faulty change through
a protected pull request and publish a new patch or minor version according to
the table above. A mistaken unpublished Release PR may be corrected or closed;
deleting a published release or rewriting its tag requires separate explicit
human authority and is not the normal rollback path.
