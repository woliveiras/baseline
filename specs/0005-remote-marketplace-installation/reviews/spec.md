# SPEC-0005 spec review

## Review boundary

Reviewed the user request, SPEC-0004's package and local-marketplace contract,
the committed marketplace manifest, the installed Codex CLI help, and
SPEC-0005 without using the new tests or documentation as justification.

## Spec

- The canonical sequence is marketplace-first: fetch `woliveiras/tuxedo` at
  `main`, then install `tuxedo@tuxedo-local` from the configured snapshot.
- Sparse checkout is optional and names both paths required by the repository
  contract: `.agents/plugins/marketplace.json` and `plugins/tuxedo`.
- Update, reinstall, and complete removal are distinct operations, with plugin
  removal preceding marketplace removal.
- Mutable `main`, the absence of published tags, and the prohibition on
  `codex plugin add <URL>` are explicit limitations rather than hidden
  assumptions.

## Standards

- The specification keeps Tuxedo's content-only package boundary and does not
  introduce a runtime, installer, credential helper, or new marketplace file.
- The local clone route remains a maintainer development workflow and is not
  presented as a prerequisite for consumers.

## Risk

- The credential boundary distinguishes Codex account authentication from Git
  transport authentication and forbids secrets in URLs or repository content.
- No unresolved specification finding remains. Remote installation and private
  SSH behavior are intentionally outside execution authority for this task and
  remain residual evidence limitations.
