---
id: SPEC-0007
title: Use canonical Tuxedo vocabulary for identity and repository boundaries
summary: Keep the project name canonical while distinguishing development tooling, repository content, user authority, and the maintainer role.
status: approved
scope:
  - root Node package identity
  - repository and installed-product boundary vocabulary
  - user authorization terminology
  - active documentation, configuration, tests, and code comments
  - historical-record preservation
risk: medium
risk_domains: [public-contract, compatibility, authority-language]
reversibility: easy
change_surfaces: [package.json, AGENTS.md, GLOSSARY.md, README.md, docs, evals, specs, tests]
contracts: [Tuxedo identity, repository-only content, development-only tooling, user-authorized operations]
review_policy: separated-contexts
test_provenance: [spec-derived, independent]
navigation:
  - package.json
  - GLOSSARY.md
  - AGENTS.md
  - README.md
  - docs/development.md
  - tests/test_toolkit.py
documentation: required
authority:
  granted: [local-edit, deterministic-tests, local-commit]
  withheld: [provider-call, model-call, eval-full, push, release, publish, deploy, production, destructive]
dependencies: [SPEC-0004, SPEC-0005, SPEC-0006]
---

# Intent

Use `tuxedo` and **Tuxedo** as the project identity everywhere an identifier or
display name represents the product. Preserve the useful boundary between the
installed plugin and repository tooling without encoding a human role into
package names or generic development surfaces. State authority in terms of the
user who grants it, not a presumed developer or maintainer role.

# Context vocabulary

| Context | Canonical term | Meaning and translation boundary |
| --- | --- | --- |
| Product identity | `tuxedo` / **Tuxedo** | Stable machine and display identity for the repository, marketplace, and plugin |
| Development tooling | `development-only` | Tools and dependencies used to develop or evaluate Tuxedo; never a consumer runtime dependency |
| Repository content | `repository-only` | Specs, tests, docs, evals, and evidence retained in the checkout but excluded from the installed plugin |
| Task authority | `user-authorized` | An operation may run only after explicit permission from the user controlling the current task |
| Stewardship role | `maintainer` | A person responsible for ongoing project stewardship; not a product name, dependency class, or automatic source of authority |

# Behavior and invariants

- The root private Node package is named `tuxedo`; `private: true` and its
  development dependencies express the non-publishable tool boundary.
- `development-only` describes executable tooling or dependencies that are not
  shipped to plugin consumers.
- `repository-only` describes tracked project artifacts excluded from the
  installed plugin package.
- `user-authorized` means the current user explicitly granted the operation.
  Being a developer or maintainer does not implicitly grant task authority.
- `maintainer` remains valid only when ongoing stewardship is the actual actor
  being discussed or when it occurs in a historical record.
- Active product docs, configuration, source comments, and current specs use
  the canonical vocabulary. Historical evidence, completed reviews, and the
  frozen internal audit are not rewritten solely to modernize terminology.
- The plugin name, version, distributed content, direct dependencies, lockfile,
  evaluation behavior, and authorization requirements do not change.

# Acceptance criteria

- **TV-001** `package.json` names the private package `tuxedo`, describes its
  evaluation tooling as development-only, and keeps version, scripts, engines,
  and dependencies unchanged.
- **TV-002** `GLOSSARY.md` defines `development-only`, `repository-only`,
  `user-authorized`, and `maintainer` with the context boundaries above.
- **TV-003** Active repository contracts, product documentation, evaluation
  configuration, and source comments use the canonical boundary terms instead
  of role-branded compounds such as `maintainer-only`, `maintainer development`,
  or `maintainer checkout`.
- **TV-004** Operations that reach providers/models or otherwise require
  explicit permission are described as user-authorized; developer or maintainer
  status alone is not presented as authority.
- **TV-005** Historical evidence, completed review records, and the frozen
  repository audit retain their original language unless another active claim
  must be reconciled.
- **TV-006** The installed plugin remains named `tuxedo`, contains only
  `.codex-plugin` and `skills`, and gains no Node dependency or repository-only
  content.

# Explicit exclusions

- Removing every occurrence of the word `maintainer` without regard to meaning.
- Rewriting historical command evidence, completed review claims, or the frozen
  repository audit to make a search count reach zero.
- Changing dependency versions, the PNPM lockfile, scripts, plugin content,
  evaluation behavior, or provider configuration beyond descriptive labels.
- Running provider/model evaluations, publishing the Node package, pushing,
  releasing, or deploying.

# Edge and failure scenarios

- A global replacement can turn a real stewardship role into inaccurate
  language or falsify a historical record; those locations must remain intact.
- `developer-authorized` is invalid when the person granting authority is not a
  developer. `user-authorized` follows the task-control relationship instead.
- `development-only` does not itself grant permission to run expensive or
  external operations; those still require explicit user authorization.
- The private root package may share the `tuxedo` name with the plugin because
  they are distinct manifests and the Node package is not published.

# Evidence and review

- Behavior matrix: [behavior-matrix.md](behavior-matrix.md)
- Evidence: [evidence.md](evidence.md)
- Spec review: [reviews/spec.md](reviews/spec.md)
- Test review: [reviews/tests.md](reviews/tests.md)
- Code review: [reviews/code.md](reviews/code.md)
