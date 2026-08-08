# SPEC-0005 test review

## Review boundary

Reviewed the approved specification, behavior/oracle matrix, fail-first record,
and the deterministic documentation test without using the new documentation
implementation as evidence that the test expectations were correct.

## Spec

- The test maps RM-001 through RM-008 to exact commands, both sparse paths,
  SSH transport, lifecycle order, authentication separation, mutable-ref and
  no-tag limitations, the unsupported direct-URL route, and the maintainer
  clone flow.
- The negative regex rejects URL-shaped arguments to `codex plugin add`, while
  the explicit prose assertion requires the documented prohibition for the
  placeholder `<URL>` form.

## Standards

- The oracle is static and deterministic: it reads repository documentation,
  does not fetch GitHub, does not invoke Codex installation, and does not call
  a model.
- The test reviews the public command contract rather than collaborator order
  or implementation details. The installed CLI help is recorded separately as
  an external protocol check.

## Risk

- The test cannot establish that GitHub accepts the remote source, that a
  private SSH key works, or that Codex installs the remote snapshot; those cases
  are explicitly prohibited or unexecuted and remain in residual limitations.
- No unresolved test finding remains after reconciling the capitalization
  expectation corrections and temporary sparse-command test literal observed
  during focused execution.

## Post-authorization amendment review

### Spec

- RM-009 adds a deterministic documentation oracle for the current private
  access policy and its HTTPS/SSH distinction.

### Standards

- The fail-first focused test rejected the prior README because it did not state
  that the repository is private or identify the verified transport.
- Remote probes stayed outside the static documentation test and used isolated
  homes with both API-key environment variables removed.

### Risk

- The SSH lifecycle is external evidence for one configured machine. It does
  not prove that another machine has valid GitHub SSH access or that Codex
  desktop exposes the same UI behavior.

## 2026-08-08 marketplace identity reconciliation

### Review boundary

Reviewed the reconciled specifications, RM-010 matrix row, fail-first record,
and test changes without using the changed manifest or documentation as
evidence.

### Spec

- No findings. Static assertions require marketplace identifier `tuxedo`,
  display name `Tuxedo`, exact `tuxedo@tuxedo` lifecycle commands, and absence
  of the retired branding from current installation documentation.
- The real clean-room lifecycle uses the installed Codex CLI and asserts the
  reinstalled plugin ID, so a documentation-only rename cannot pass CP-004
  through CP-006.

### Standards

- The two core identity tests failed before the manifest and documentation
  changed for the expected reasons. Their oracles are spec-derived.
- The explicit legacy-name absence checks were added after implementation
  inspection and are implementation-aware supplemental coverage; the
  fail-first manifest, selector, and lifecycle assertions remain the primary
  oracles.

### Risk

- A plausible partial rename fails either the parsed manifest assertions,
  exact command assertions, or real CLI lifecycle.
- The ignored `.DS_Store` independently triggers the package allowlist as
  designed; preserving it outside the package during the integration run does
  not weaken the naming assertions.
