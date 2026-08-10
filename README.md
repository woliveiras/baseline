# Baseline

Baseline is the portable minimum for disciplined software engineering. It is a
set of Agent Skills that helps coding agents measure work by risk, clarify real
ambiguity, test behavior first, review changes proportionally, and keep Git
authority explicit.

Baseline is loaded by your agent on demand. It does not add a CLI, runtime, or
project dependency.

## How it works

Baseline routes a task through the smallest workflow it needs:

```text
request -> measure -> clarify when needed -> test -> implement -> review
```

Ask your agent normally for a matching workflow, or invoke one directly with
`$skill-name` when you need a specific path. The skills are independent, so you
can use Baseline without installing Storehouse or a specification methodology.

## Install

Choose the route for your agent:

| Agent | Recommended route |
| --- | --- |
| Codex | GitHub marketplace plugin |
| GitHub Copilot | Repository marketplace plugin |
| Claude Code | Claude marketplace plugin |
| Cursor and OpenCode | Standalone `.agents/skills` links |
| Pi | Local package registration |

### Codex

Install the latest published version from the GitHub marketplace:

<!-- x-release-please-start-version -->
```bash
codex plugin marketplace add woliveiras/baseline --ref v0.2.0
codex plugin add baseline@baseline
```
<!-- x-release-please-end -->

Start a new session after installation. In Codex CLI or desktop, you can also
open `/plugins`, select the Baseline marketplace, and install Baseline.

### GitHub Copilot

```bash
copilot plugin marketplace add woliveiras/baseline
copilot plugin install baseline@baseline
```

### Claude Code

```bash
claude plugin marketplace add https://github.com/woliveiras/baseline.git
claude plugin install baseline@baseline
```

### Cursor and OpenCode

Run this block as-is. It downloads the published Baseline tag, creates
`$HOME/.agents/skills`, and links every distributed skill:

<!-- x-release-please-start-version -->
```bash
BASELINE_VERSION="v0.2.0"
BASELINE_DIR="$HOME/.baseline"
BASELINE_SKILLS="$BASELINE_DIR/plugins/baseline/skills"

if [ -d "$BASELINE_DIR/.git" ]; then
  git -C "$BASELINE_DIR" fetch --depth 1 origin "$BASELINE_VERSION"
  git -C "$BASELINE_DIR" checkout --detach "$BASELINE_VERSION"
elif [ -e "$BASELINE_DIR" ]; then
  printf 'Cannot use %s: the path already exists and is not a Git checkout.\n' "$BASELINE_DIR" >&2
  exit 1
else
  git clone --depth 1 --branch "$BASELINE_VERSION" https://github.com/woliveiras/baseline.git "$BASELINE_DIR"
fi

mkdir -p "$HOME/.agents/skills"
for skill_dir in "$BASELINE_SKILLS"/*/; do
  skill_name="$(basename "$skill_dir")"
  skill_path="${skill_dir%/}"
  link_path="$HOME/.agents/skills/$skill_name"

  if [ -L "$link_path" ] && [ "$(readlink "$link_path")" = "$skill_path" ]; then
    continue
  fi
  if [ -e "$link_path" ] || [ -L "$link_path" ]; then
    printf 'Cannot install %s: target already exists at %s\n' "$skill_name" "$link_path" >&2
    exit 1
  fi
  ln -s "$skill_path" "$link_path"
done
```
<!-- x-release-please-end -->

The command uses symlinks so one checkout can serve every skill and updates do
not copy files into your home directory. For a project-only installation, run
the same block with `BASELINE_DIR` and the destination changed to paths inside
that project; the [installation guide](docs/guides/installation.md) covers the
full lifecycle.

### Pi

Run this block as-is. It downloads the published Baseline tag, installs the
local Pi package, and lists the installed package:

<!-- x-release-please-start-version -->
```bash
set -eu

BASELINE_VERSION="v0.2.0"
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

## Initialize a project

Installing Baseline makes its skills discoverable but does not modify the
consumer repository. To adopt the complete Baseline engineering contract,
start a new agent session at the repository root and run this explicit skill
once per project before relying on the workflow:

```text
Use $setup-baseline to create or safely reconcile this project's AGENTS.md.
```

The skill inspects current project evidence, creates `AGENTS.md` when absent,
preserves stronger existing instructions, and stops for a material conflict
instead of overwriting it. Ask it explicitly for Claude Code compatibility when
you also want a minimal `CLAUDE.md` that imports `@AGENTS.md` without copying the
contract.

## Use Baseline

After installation, start a new agent session and ask for the work you need:

```text
Fix this bug using the bugfix workflow and add a regression test.
Review this change proportionally before I commit it.
Use the $tdd workflow for this approved behavior.
```

The main workflow groups are:

| Group | Skills |
| --- | --- |
| Project foundation | `setup-baseline` |
| Change workflow | `measurer`, `refine`, `tdd`, `bugfix`, `verify`, `git-commit`, `ci-workflow`, `docs` |
| Design and architecture | `shape-domain`, `design-deep-modules`, `improve-architecture`, `decision-framework` |
| Explicit deep work | `brainstorming`, `premortem`, `session-bridge`, `technical-research` |
| Safety | `security-review` |

## Update or remove

Remove a plugin and its marketplace entry from the same client:

```bash
# Codex
codex plugin remove baseline@baseline
codex plugin marketplace remove baseline

# GitHub Copilot
copilot plugin uninstall baseline
copilot plugin marketplace remove baseline

# Claude Code
claude plugin uninstall baseline@baseline
claude plugin marketplace remove baseline
```

For Pi, run `pi remove "$HOME/.baseline/plugins/baseline" -l --approve`.
For standalone `.agents/skills` links, delete only the Baseline symlinks you
created. See the [installation guide](docs/guides/installation.md) for update,
reinstall, sparse checkout, private fork, and local development instructions.

## Develop Baseline

The complete package lives under [`plugins/baseline/`](plugins/baseline/). To
work on the repository, its tests, release process, and architecture, start with
the [development documentation](docs/README.md).

Baseline is the horizontal engineering foundation. [Storehouse](https://github.com/woliveiras/storehouse)
provides optional technology-specific skills and the independent SDD workflow.

## License

Baseline is released under the [MIT License](LICENSE).
