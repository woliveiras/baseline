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
