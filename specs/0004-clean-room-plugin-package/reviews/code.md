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
