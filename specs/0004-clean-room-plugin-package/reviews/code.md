# SPEC-0004 code review

## Review boundary

Reviewed the complete staged candidate with SPEC-0004, the matrix, tests, documentation, validator output, clean-room lifecycle, and Git rename evidence.

## Spec

- The marketplace now resolves `./plugins/tuxedo` and the manifest remains named and versioned `tuxedo` `0.1.0`.
- All 63 distributed files moved without content changes into the 260 KB package; Git reports 100% renames for the manifest and skill files.
- Root `skills` is a relative compatibility symlink; the installed package contains real files and no symlinks.
- Public standalone instructions use the canonical package path. Maintainer tools continue through the compatibility path, while the official plugin validator targets the actual package root.

## Standards

- The implementation adds no script, dependency, generated distribution, login, model call, or broader installed surface.
- Official plugin validation, 17 skill validations, 81 unit tests, Promptfoo config validation, 48-run dry-run, shell check, and diff check pass.

## Risk

- The layout depends on symlink support only inside the maintainer checkout, consistent with the stated macOS and Linux scope.
- Codex desktop UI and other clients remain untested. Actual skill effectiveness remains delegated to the user's upcoming real-task trials.
- No unresolved implementation finding remains.

## 2026-08-07 link-integrity amendment

### Review boundary

Reviewed the complete task diff with amended SPEC-0004, matrix, fail-first and passing evidence, fixture tests, installed-package traversal, validator results, dependency diff, and the preserved ignored-file limitation.

### Spec

- CP-008 is implemented by decoding and canonically resolving local paths before a `plugins/tuxedo/` containment check, then requiring the destination to be a file.
- CP-009 derives deterministic anchors from ATX and setext headings outside frontmatter and fenced code, including duplicate suffixes, and checks decoded fragments exactly.
- External schemes and protocol-relative URLs leave local validation before any destination read; the external fixture confirms the connection seam remains unused.
- The real installed corpus is scanned through the root `skills/` symlink while the resolved package root remains the authority boundary.

### Standards

- All implementation remains in maintainer tests and uses only the Python standard library. No distributed plugin file, runtime, dependency manifest, or lockfile changed.
- Official plugin validation and all 17 official skill validations pass. The focused link suite passes 9/9, the clean tracked unit candidate passes 89/89, and the legacy dry-run retains 48 configurations with its prior fingerprint.
- `git diff --check` passes and no tracked shell file exists, so shell syntax validation is not applicable.

### Risk

- Direct and percent-encoded traversal are covered; canonical resolution also rejects absolute paths and paths escaping through an existing symlink.
- External reachability is intentionally untested. The anchor parser is deterministic for the installed package's inline Markdown links and headings; it is not presented as a network or full Markdown-renderer conformance test.
- The ignored `plugins/tuxedo/.DS_Store` remains preserved outside the commit. Its presence makes the two existing package-boundary tests fail as designed; temporarily preserving it outside the package proved the tracked candidate passes 89/89, after which the file was restored unchanged.
- No unresolved in-scope finding remains.
