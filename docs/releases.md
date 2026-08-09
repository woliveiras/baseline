# Releasing Tuxedo

Tuxedo has one product version for the complete plugin and all distributed
skills. Individual skills are independently routable and installable, but they
do not receive separate versions, changelogs, tags, or GitHub Releases.

The version is synchronized across `package.json`, `pyproject.toml`, the Tuxedo
entry in `uv.lock`, `plugins/tuxedo/.codex-plugin/plugin.json`,
`.release-please-manifest.json`, `CHANGELOG.md`, the `vX.Y.Z` Git tag, and its
GitHub Release. The private Node package is never published to npm, and the
non-package Python project is never published to PyPI; both exist only for
repository development tooling. `package.json` remains Release Please's root
version source.

## Version rules before 1.0.0

Use Conventional Commits to describe the user-visible effect:

| Change | Version result |
| --- | --- |
| `fix` | `0.1.0` -> `0.1.1` |
| `feat` | `0.1.0` -> `0.2.0` |
| Breaking change before `1.0.0` | `0.1.0` -> `0.2.0` |
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
   Release. No npm publish, deployment, or consumer runtime artifact follows.

The write-token job never checks out or executes repository content. The
validation job has read-only repository permission and does not receive a
publication credential. Branch protection requires the same `Validate` context
for ordinary and generated pull requests.

## Initial release

`v0.1.0` is bootstrapped explicitly because the plugin manifest already
declared `0.1.0` before Release Please existed. After the bootstrap PR passes CI
and reaches protected `main`, create tag `v0.1.0` and a GitHub Release targeting
that same merge commit. From then on, `.release-please-manifest.json` starts at
`0.1.0` and Release Please owns `0.1.1`, `0.2.0`, and later versions.

Until that initial tag exists, top-level `bootstrap-sha` in
`release-please-config.json` prevents pre-bootstrap Conventional Commits from
being interpreted as unreleased changes. Version tests compare the synchronized
sources dynamically; they must accept a legitimate Release PR version bump
instead of freezing the repository forever at `0.1.0`.

## Release verification

Before merging a Release PR, require:

- synchronized version files and changelog;
- the protected `Validate` status on the exact candidate SHA;
- a task-owned diff with no unexpected installed-plugin content;
- confirmation that the proposed tag and GitHub Release do not already exist.

After publication, verify that the tag and GitHub Release target the same commit.
Install the marketplace from the exact tag in disposable `HOME` and `CODEX_HOME`
directories, confirm `tuxedo@tuxedo` reports the released version, and confirm
all distributed skills are discovered. This check performs no login or model
call.

## Rollback

Published tags and GitHub Releases are immutable history and are not moved or
silently replaced. If a release is defective, revert the faulty change through
a protected pull request and publish a new patch or minor version according to
the table above. A mistaken unpublished Release PR may be corrected or closed;
deleting a published release or rewriting its tag requires separate explicit
human authority and is not the normal rollback path.
