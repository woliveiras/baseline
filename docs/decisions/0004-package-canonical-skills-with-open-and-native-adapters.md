---
status: accepted
date: 2026-08-10
decision-makers:
  - William Oliveira
---

# Package canonical skills with an open manifest and thin native adapters

## Context and problem statement

Baseline's 17 Agent Skills already form a client-neutral behavior corpus, but
the installed package exposed only a Codex manifest and lifecycle. Cursor and
GitHub Copilot implement the open Agent Plugins format, while Claude Code and
Pi require different declarative package contracts. OpenCode can discover
Agent Skills without a runtime plugin.

A multiclient package must preserve the `baseline` identity, one product
version, the existing Codex route, one canonical skill tree, and the absence of
a consumer CLI, generator, synchronizer, daemon, dependency, or runtime.
Recognizing `SKILL.md` must not be presented as proof of native lifecycle,
invocation semantics, composition, or behavior.

## Decision drivers

- Implement Agent Skills and Agent Plugins as open contracts where clients
  support them.
- Keep all workflow behavior, references, assets, and scripts in one canonical
  `plugins/baseline/skills/` tree.
- Add native metadata only when a client cannot use the common package contract.
- Preserve the Codex manifest, marketplace, namespace, and standalone symlink.
- Update identity and version atomically without generating client packages.
- Keep repository-only tests and evaluation tooling outside installed content.

## Decision outcome

Keep `plugins/baseline/` as the client-neutral product package boundary:

- `plugin.json` is the Agent Plugins 1.0.0 manifest shared by Cursor and
  GitHub Copilot;
- `.codex-plugin/plugin.json` remains the Codex adapter;
- `.claude-plugin/plugin.json` is a minimal Claude Code adapter;
- `package.json` is a private, script-free, dependency-free Pi descriptor with
  an exact `./skills/*/SKILL.md` allowlist;
- `skills/` is the sole behavior corpus.

Keep client-owned lifecycle catalogs outside the installed package. The Codex
catalog remains at `.agents/plugins/marketplace.json`; the Copilot catalog at
`.github/plugin/marketplace.json` points to the same `./plugins/baseline`
directory. The Copilot catalog is necessary because direct repository installs
are deprecated by the current CLI. The Claude catalog at
`.claude-plugin/marketplace.json` adds its persistent native lifecycle while
selecting the same package.

Do not add a `.cursor-plugin` adapter until Baseline has a necessary
Cursor-only component. Do not add an OpenCode executable plugin: `.agents/skills`
already supplies its static capability. Cursor and Claude marketplace
submission remain external, explicitly authorized operations. Cursor does not
need a repository catalog for a single Agent Plugin; its public listing is a
reviewed submission. Claude's repository marketplace is locally lifecycle
validated before any optional submission to Anthropic's official catalog.

Release Please updates all four package manifests, both Copilot catalog version
fields, and the Claude catalog plugin version from the root product version.
Deterministic tests reject copied
skill trees, package scripts or dependencies, executable Claude components,
unknown open-manifest fields, missing adapters, divergent catalog paths, and
version drift.

## Invocation-policy boundary

The canonical skill frontmatter stays within the strict Agent Skills contract.
Codex-specific explicit-only behavior remains in `agents/openai.yaml`.
Baseline does not add an unstandardized field and describe it as portable
enforcement. Until another host mapping is validated, its discovery result is
not evidence that Baseline's explicit-only policy is preserved.

The six explicit-only workflows remain a product policy and must be invoked
deliberately on clients without a validated mapping. A future change to
canonical invocation metadata, the minimum OpenCode contract, or a host adapter
requires a separate RFC because it changes observable routing semantics.

## Consequences

- Cursor and Copilot receive one open package manifest rather than divergent
  behavior adapters; Copilot adds only its client-owned catalog.
- Codex keeps its existing native package and marketplace compatibility.
- Claude and Pi can identify the same package without copied content or a
  consumer runtime; Claude also receives a persistent native marketplace
  lifecycle.
- OpenCode stays plugin-free and can consume the canonical Agent Skills.
- Agent Plugins does not replace client-owned marketplace, install, update, or
  removal contracts; the Copilot and Claude catalogs supply those native
  lifecycles.
- Copilot and Claude local marketplace lifecycles are clean-room validated.
  Claude's public HTTPS default-branch lifecycle is also validated on 2.0.29,
  which keeps a full private marketplace checkout while selecting only the
  consumer package. Cursor lifecycle, immutable-tag association for Copilot and
  Claude, and behavior under any model remain separate evidence gaps.
- The Pi local package intentionally references a trusted checkout; registry
  publication or a derived artifact needs a separate product and publication
  decision.

## Confirmation and rollback

Confirm the decision with the Agent Plugins 1.0.0 schema, official Codex and
Claude validators, all official skill validators, exact package-boundary and
version tests, and isolated lifecycle/discovery checks available without login
or model calls. Record unavailable client checks as limitations rather than
passing results.

Rollback of the Copilot or Claude lifecycle removes its repository marketplace
and corresponding version, test, and documentation contracts; direct or
standalone skill discovery can remain as a temporary fallback. Rolling back the
broader multiclient package
removes the open, Claude, and Pi descriptors while the unchanged canonical skill
tree, Codex adapter, Codex marketplace, and root compatibility symlink continue
to operate.
