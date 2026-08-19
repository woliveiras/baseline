# Baseline

Baseline is the portable minimum for disciplined software engineering. It is a
set of Agent Skills that helps coding agents measure work by risk, clarify real
ambiguity, test behavior first, review changes proportionally, and keep Git
authority explicit.

Baseline is loaded by your agent on demand. It does not add a CLI, runtime, or
project dependency.

Baseline follows the open [Agent Skills](https://agentskills.io) and
[Agent Plugins](https://agent-plugins.org) specifications. Agent Skills defines
the canonical content, Agent Plugins defines the open package, and thin native
adapters add lifecycle integration only where a client requires it.

## How it works

Baseline routes a task through the smallest workflow it needs:

```text
request -> measure -> clarify when needed -> test -> implement -> review
```

Ask your agent normally for a matching workflow, or invoke one directly with
`$skill-name` when you need a specific path. The skills are independent, so you
can use Baseline without installing Storehouse or a specification methodology.

## Install

Choose the route for your agent. The evidence column records deterministic
validation already completed; it is not a behavioral support claim.

| Agent | Recommended route | Current evidence |
| --- | --- | --- |
| Codex | GitHub marketplace plugin | Lifecycle and discovery validated |
| GitHub Copilot | Repository marketplace plugin | Lifecycle and discovery validated; no immutable source pin |
| Claude Code | Claude marketplace plugin | Default-branch lifecycle and discovery validated; immutable-tag association not validated |
| Cursor | Standalone `.agents/skills` links | Static format validation only |
| OpenCode | Standalone `.agents/skills` links | Project discovery validated |
| Pi | Local package registration | Local package lifecycle and discovery validated |

No model-backed behavioral certification has been completed for these client
routes. Discovery proves that a client can see the skills, not that its model
will route to or follow them correctly.

### Codex

Install the latest published version from the GitHub marketplace:

<!-- x-release-please-start-version -->
```bash
codex plugin marketplace add woliveiras/baseline --ref v0.5.0
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

This short route follows the repository default branch and is therefore
mutable. Use the tag-qualified route and limitations in the
[installation guide](docs/guides/installation.md) when reproducibility matters.

### Cursor and OpenCode

Run this block as-is. It downloads the published Baseline tag, creates
`$HOME/.agents/skills`, and links every distributed skill:

<!-- x-release-please-start-version -->
```bash
BASELINE_VERSION="v0.5.0"
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

BASELINE_VERSION="v0.5.0"
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

The canonical skill name is `setup-baseline`. A plugin-capable client may show
a namespace in discovery; Codex currently reports `baseline:setup-baseline`.
Use the name shown by the active client when its picker or skill list differs
from the canonical name used in these examples.

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
An immutable Codex installation must replace its pinned marketplace ref before
reinstallation; a marketplace refresh alone does not select a newer tag.

## Develop Baseline

The complete package lives under [`plugins/baseline/`](plugins/baseline/). To
work on the repository, its tests, release process, and architecture, start with
the [development documentation](docs/README.md).

Baseline is the horizontal engineering foundation. [Storehouse](https://github.com/woliveiras/storehouse)
provides optional technology-specific skills and the independent SDD workflow.

## License

Baseline is released under the [MIT License](LICENSE).
