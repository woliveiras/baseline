# Installing Baseline

This guide contains the complete installation and lifecycle details. For the
short path, see the [top-level README](../../README.md).

Baseline is distributed as static Agent Skills. Consumer projects receive no
Baseline runtime, CLI, Python, UV, PNPM, Node dependency, lifecycle hook, or
generated build output.

## Required project initialization

Client installation makes the skills discoverable but does not modify the
consumer repository. After completing one of the installation routes below,
start a new agent session at the target repository root and invoke the setup
skill once per project:

```text
Use $setup-baseline to create or safely reconcile this project's AGENTS.md.
```

This establishes the project-owned Baseline foundation from current repository
evidence. The skill creates the root file when absent, preserves stronger
existing instructions, reports an already conforming file without changing it,
and stops when a material conflict needs human resolution. It neither installs
a consumer runtime nor commits the resulting instructions. Request Claude Code
compatibility explicitly when the project also needs a minimal `CLAUDE.md`
import of `@AGENTS.md`.

## Codex

### Stable remote installation

The public GitHub marketplace route installs a published immutable release
without requiring a Baseline checkout on the consumer machine:

<!-- x-release-please-start-version -->
```bash
codex plugin marketplace add woliveiras/baseline --ref v0.3.0
codex plugin add baseline@baseline
```
The release tag `v0.3.0` is immutable; a later release uses a new tag.
<!-- x-release-please-end -->

The `woliveiras/baseline` shorthand uses HTTPS. The marketplace and plugin are
both named `baseline`; `baseline@baseline` is `plugin@marketplace`, not
`name@version`. The installed manifest reports its version separately. Start a
new Codex session after installation. Codex CLI and Codex desktop also expose
this flow through `/plugins` and the Plugins screen.

### Sparse checkout

Fetch only the marketplace manifest and the package when a sparse checkout is
useful:

<!-- x-release-please-start-version -->
```bash
codex plugin marketplace add woliveiras/baseline --ref v0.3.0 \
  --sparse .agents/plugins/marketplace.json \
  --sparse plugins/baseline
codex plugin add baseline@baseline
```
<!-- x-release-please-end -->

Do not omit either sparse path. The manifest selects the plugin and
`plugins/baseline/` contains the manifest and distributed skills.

### Private forks

For a private fork, use the same sparse paths with an SSH source after
configuring GitHub access on the machine:

<!-- x-release-please-start-version -->
```bash
codex plugin marketplace add git@github.com:OWNER/baseline.git --ref v0.3.0 \
  --sparse .agents/plugins/marketplace.json \
  --sparse plugins/baseline
codex plugin add baseline@baseline
```
<!-- x-release-please-end -->

The complete private-fork form is:

<!-- x-release-please-start-version -->
```bash
codex plugin marketplace add git@github.com:OWNER/baseline.git --ref v0.3.0
codex plugin add baseline@baseline
```
<!-- x-release-please-end -->

Codex account authentication and GitHub repository authentication are separate.
A public repository does not require a GitHub credential for this fetch. No credential, token, private key, or credential-bearing URL belongs in repository documentation.

### Update, reinstall, and remove

Tags are immutable. Replace the configured marketplace ref and reinstall to
update:

<!-- x-release-please-start-version -->
```bash
codex plugin remove baseline@baseline
codex plugin marketplace remove baseline
codex plugin marketplace add woliveiras/baseline --ref v0.3.0
codex plugin add baseline@baseline
```
<!-- x-release-please-end -->

To reinstall the same marketplace:

```bash
codex plugin remove baseline@baseline
codex plugin add baseline@baseline
```

To remove Baseline completely:

```bash
codex plugin remove baseline@baseline
codex plugin marketplace remove baseline
```

The supported remote route is marketplace-first. Do not use `codex plugin add <URL>`;
`codex plugin add` receives the `plugin@marketplace` selector after the marketplace
has been configured. `--ref main` is a mutable development channel for unreleased
testing, not a reproducible installation.

### Local development

For repository development, use the local marketplace flow:

```bash
git clone https://github.com/woliveiras/baseline.git
cd baseline
codex plugin marketplace add "$(pwd)"
codex plugin add baseline@baseline
```

This is a development convenience, not a prerequisite for users. The package
contains the plugin manifest and distributed skills; repository-only tests,
evaluations, documentation, and `node_modules/` stay outside it. No package-build or copy script is required.

## GitHub Copilot

Copilot direct repository installation is deprecated by the CLI. Register the
repository marketplace and install through the `plugin@marketplace` selector:

```bash
copilot plugin marketplace add woliveiras/baseline
copilot plugin install baseline@baseline
copilot skill list
```

Update the catalog before updating the plugin:

```bash
copilot plugin marketplace update baseline
copilot plugin update baseline
```

Reinstall or remove Baseline with:

```bash
copilot plugin uninstall baseline
copilot plugin install baseline@baseline

# Complete removal
copilot plugin uninstall baseline
copilot plugin marketplace remove baseline
```

The committed catalog points to `./plugins/baseline`. Copilot marketplace clean-room
checks cover add, browse, install, discovery of 18 skills, update, uninstall,
marketplace removal, and reinstall without login or model calls.
Copilot's current marketplace command follows the repository marketplace rather
than exposing Codex's explicit immutable `--ref` option.

## Claude Code

Install the repository marketplace and the Baseline plugin:

```bash
claude plugin marketplace add https://github.com/woliveiras/baseline.git
claude plugin install baseline@baseline
claude plugin marketplace list
```

The HTTPS source tracks the repository default branch and is a mutable
development channel. For a reproducible release, append `#vX.Y.Z` after
confirming that the tag contains `.claude-plugin/marketplace.json`.

Remove or temporarily disable the plugin with:

```bash
claude plugin uninstall baseline@baseline
claude plugin marketplace remove baseline

claude plugin disable baseline@baseline
claude plugin enable baseline@baseline
```

For local development, validate and load the trusted package directly:

```bash
claude plugin validate /absolute/path/to/baseline/plugins/baseline
claude --plugin-dir /absolute/path/to/baseline/plugins/baseline
```

The first command performs no model call. Claude Code 2.0.29 was validated for
marketplace lifecycle and discovery of all 18 skills. Its validator emits a
stale `metadata.description` warning for the current top-level field; the
current Claude documentation defines the top-level field, so Baseline keeps it.

## Cursor and OpenCode

Both clients can consume the standalone Agent Skills layout. Run the complete
copy-paste block in the [README](../../README.md). It downloads the published
tag to `$HOME/.baseline`, creates `$HOME/.agents/skills`, refuses to overwrite
an existing skill, and links every distributed skill.

The command uses symlinks intentionally. Updating the checkout updates the
skills without copying a second behavior tree.

OpenCode 1.16.2 was locally verified to discover all 18 Baseline skills through
a project `.agents/skills` link. Cursor remains at static format compatibility
until its native loader and lifecycle can be exercised locally.

## Pi

Run this block as-is. It downloads the published Baseline tag, registers the
local Pi package, and lists the installed package:

<!-- x-release-please-start-version -->
```bash
set -eu

BASELINE_VERSION="v0.3.0"
BASELINE_DIR="$HOME/.baseline"
BASELINE_PACKAGE="$BASELINE_DIR/plugins/baseline"

if [ -d "$BASELINE_DIR/.git" ]; then
  git -C "$BASELINE_DIR" fetch --depth 1 origin "$BASELINE_VERSION"
  git -C "$BASELINE_DIR" checkout --detach "$BASELINE_VERSION"
elif [ -e "$BASELINE_DIR" ]; then
  printf 'Cannot use %s: the path already exists and is not a Git checkout.\n' "$BASELINE_DIR" >&2
  exit 1
else
  git clone --depth 1 --branch "$BASELINE_VERSION" https://github.com/woliveiras/baseline.git "$BASELINE_DIR"
fi

pi install "$BASELINE_PACKAGE" -l --approve
pi list --approve
```
<!-- x-release-please-end -->

Remove and reinstall the same source with:

```bash
pi remove "$HOME/.baseline/plugins/baseline" -l --approve
pi install "$HOME/.baseline/plugins/baseline" -l --approve
```

The private, dependency-free Pi descriptor selects only `skills/*/SKILL.md`.

## Standalone skill removal

Remove only the links created by the installer and then remove its checkout:

```bash
BASELINE_DIR="$HOME/.baseline"
BASELINE_SKILLS="$BASELINE_DIR/plugins/baseline/skills"

for skill_dir in "$BASELINE_SKILLS"/*/; do
  skill_name="$(basename "$skill_dir")"
  skill_path="${skill_dir%/}"
  link_path="$HOME/.agents/skills/$skill_name"

  if [ -L "$link_path" ] && [ "$(readlink "$link_path")" = "$skill_path" ]; then
    rm "$link_path"
  fi
done

if [ -d "$BASELINE_DIR/.git" ]; then
  rm -rf "$BASELINE_DIR"
fi
```

The removal block leaves unrelated skills and files under `.agents/skills`
untouched. Start a new agent session after installing or removing the links.

## How skills are selected

**Implicit invocation:** Codex may select a skill when the request matches its
description.

**Explicit invocation:** use `$skill-name` when you need a deterministic choice.
The canonical skill files use only the strict Agent Skills frontmatter shared by
validators. Baseline does not invent a metadata field and call it portable
enforcement. Other clients may select skills differently; discovery is not proof
that an agent followed every instruction.

The package uses the open Agent Plugins 1.0.0 manifest where supported, plus
thin native adapters for clients with their own package contract. All adapters
point to one canonical `skills/` tree and contain no copied behavior, hooks,
dependencies, scripts, or runtime.
