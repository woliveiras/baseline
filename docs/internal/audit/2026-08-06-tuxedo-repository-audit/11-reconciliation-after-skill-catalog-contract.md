# 11 — Reconciliation after the skill catalog contract

Date: 2026-08-06

SPEC-0003 responds to the catalog, documentation, routing, and onboarding findings without rewriting the original audit. The product still has 17 skills; no workflow was removed or merged before real-task evidence demonstrates harmful overlap.

## Decision

Tuxedo now uses a declarative transition model in `skills/catalog.md`. It is a table of ownership, input, output, precedence, stop, and fallback. It is not an executable state machine: there is no persisted lifecycle state, hook, launcher, CLI, daemon, or consumer dependency.

The principal overlap resolutions are:

- `spec` owns the canonical behavior/oracle matrix; `verify` reviews it and proposes corrections.
- `design-deep-modules` owns boundary options; `decision-framework` selects among established material options when authority permits.
- `refine` resolves ambiguity but cannot reopen approved sufficient work or act as approval owner.
- `premortem` proposes mitigations and edits a governing artifact only with explicit authority.
- `ci-workflow` owns CI mechanics; `security-review` owns threat analysis when the workflows compose.

## Finding disposition

| Finding | Reconciled state | Evidence or remaining limitation |
| --- | --- | --- |
| `TUX-AUD-001` | Addressed for catalog contract | SPEC-0003 links criteria, matrix, deterministic tests, implementation, evidence, and review for all 17 skill boundaries. Empirical effectiveness remains a separate trial question. |
| `TUX-AUD-011` | Open with progress | README now provides Codex plugin and standalone installation. Cross-client installation, discovery, routing, and composition remain unverified. |
| `TUX-AUD-012` | Addressed deterministically | A local marketplace manifest and reproducible Codex CLI/desktop instructions now distinguish clone, install, update, removal, and new-session discovery. Clean-room installation is still residual external evidence. |
| `TUX-AUD-013` | Addressed | `premortem` and `technical-research` join the explicit-only metadata set; `git-commit` metadata now matches its existing explicit authority contract. |
| `TUX-AUD-014` | Addressed declaratively | The installed catalog defines owner, transition, precedence, stop, fallback, and multi-skill composition without claiming mechanical enforcement. |
| `TUX-AUD-015` | Addressed | Premortem output defaults to proposals; durable edits require explicit artifact authority. |
| `TUX-AUD-016` | Addressed | Canonical spec templates start risk and review policy as `unresolved` rather than preselecting `small` and one reviewer. |
| `TUX-AUD-026` | Open | Generic-name collision and precedence behavior in non-Codex clients still need clean-room tests. |
| `TUX-AUD-028` | Addressed for docs assets | MADR, C4, npm RFC, Google SRE postmortem, and GitHub Actions assets identify primary sources and selection boundaries. |
| `TUX-AUD-029` | Open | This slice does not define a complete offline/network contract for technical research. |

## Documentation knowledge

The docs skill now routes to reusable output assets instead of only short command reminders:

- MADR-based decision records;
- C4-based project architecture documentation;
- a lightweight RFC derived from npm's public RFC process with Tuxedo authority and validation fields;
- a blameless postmortem derived from Google SRE guidance.

The CI skill loads GitHub Actions guidance only when GitHub Actions is the selected platform. The reference covers least privilege, immutable action SHAs, untrusted inputs, secrets, caches, artifacts, OIDC, and protected deployment authority.

## Routing evidence boundary

The routing suite grows from 34 to 40 cases: three indirect requests do not name the expected skill, and three requests require two legitimate skill calls. Historical 34-case reports remain historical and cannot prove the expanded contract. Deterministic generator/adapter evidence is recorded in SPEC-0003; focused provider evidence is recorded only if actually executed.

## Residual risk

- A local marketplace manifest and validator success do not equal a clean-room install on every Codex surface.
- Skill-call metadata remains a Codex SDK heuristic, not universal proof that every instruction affected behavior.
- Declarative composition can still be ignored by an agent; real-task trials and routing evaluations measure different parts of that risk.
- No evidence yet justifies removing or merging a skill.
