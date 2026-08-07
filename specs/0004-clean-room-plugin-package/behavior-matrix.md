# SPEC-0004 behavior and oracle matrix

| Criterion | Scenario | Invariant | Observable oracle | Oracle provenance | Planned verification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CP-001 | Marketplace resolution | Marketplace selects the dedicated plugin root | Parsed source equals `./plugins/tuxedo`; manifest name is `tuxedo` | spec-derived | unit test; CLI marketplace list | pass; structural and clean-room tests |
| CP-002 | Installed-content boundary | Only distributed content belongs to the package | Package top-level allowlist, recursive forbidden-path and symlink checks pass | independent | unit test | pass; 63 real files, 260 KB, no package symlinks |
| CP-003 | Single canonical skill tree | Root compatibility path does not duplicate skill content | `skills` is a relative symlink resolving to packaged `skills`; inventory is 17 | spec-derived | unit test | pass |
| CP-004 | Fresh installation | Installation requires neither personal state nor credentials | Isolated CLI marketplace-add and plugin-add return zero with keys removed | external | clean-room integration test | pass with Codex CLI 0.144.4 |
| CP-005 | Codex discovery | Installed package exposes exactly the intended catalog | App Server reports 17 enabled `tuxedo:*` skills, installed-cache paths, no errors | external | clean-room integration test | pass; 17/17 from installed cache |
| CP-006 | Repeatability | Removal and reinstallation are supported lifecycle operations | CLI remove empties installed list; second add succeeds | external | clean-room integration test | pass |
| CP-007 | Onboarding | Users can install without a package-generation step | README and development guide state package root and exact commands | spec-derived | documentation test | pass |
| CP-008 | Local link target | Installed Markdown cannot escape its package boundary or name an absent file | A valid in-package link passes; missing and `../` escape fixtures report deterministic errors | spec-derived | focused fixture tests; installed-package traversal | pass; fail-first detected escape, final direct and encoded traversal fixtures pass |
| CP-009 | Local fragment and external URL | Local fragments name destination headings; deterministic validation performs no network I/O | Valid anchor passes, absent anchor fails, and an external URL passes with the network seam asserted unused | independent | focused fixture tests; installed-package traversal | pass; fail-first detected absent anchor, final anchor and offline URL fixtures pass |
