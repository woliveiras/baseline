---
name: ci-workflow
description: Create, review, or repair a CI workflow that produces traceable quality evidence with least privilege. Use for test, lint, build, artifact, release, or deploy automation; do not use for general infrastructure design or to bypass protected production authority.
---

# CI Workflow

1. Read the governing spec, criterion IDs, repository scripts, existing workflows, trust boundaries, and required evidence.
2. Define event triggers, path filters, concurrency, cancellation, permissions, and untrusted-input boundaries before jobs.
3. Map jobs and artifacts to criteria or invariant checks. Prefer repository scripts so local and CI evidence exercise the same commands.
4. Use least privilege, immutable action references for sensitive workflows, safe caches, explicit artifact retention, and OIDC when a supported deploy target is separately authorized.
5. Keep secrets out of logs, arguments, artifacts, PR content, and fork-controlled execution. Treat event payloads and checked-out code as untrusted.
6. Keep release, publication, deploy, and production jobs behind explicit human/environment protection. Adding a workflow does not grant execution authority.
7. Validate syntax locally when tooling exists, then inspect the real CI result when available. Record unavailable remote evidence honestly.

Return trigger, permission, secret, cache, artifact, criterion mapping, and verification summaries. CI evidence establishes what ran and against which revision; it does not establish semantic adequacy.
