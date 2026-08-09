# GitHub Actions

Load this reference only when GitHub Actions is the selected CI platform. Repository workflow conventions and current GitHub documentation take precedence.

## Workflow contract

- Define `on`, path filters, concurrency, cancellation, and permissions before job detail.
- Set top-level `permissions: {}` or the smallest read permissions, then grant job-specific access. A job that does not need write access must not inherit it.
- Pin third-party actions to a full-length commit SHA. A mutable tag may be readable, but it is not an immutable supply-chain reference. Record the release tag in a comment when useful for updates.
- Treat workflow expressions, event payloads, branch names, issue bodies, PR titles, and checked-out fork code as untrusted input. Do not interpolate them into shell scripts.
- Avoid privileged `pull_request_target` execution of untrusted PR code. If the event is necessary, separate metadata handling from any checkout or execution of contributor-controlled content.
- Keep secrets out of command arguments, logs, caches, artifacts, summaries, and fork-controlled jobs. Prefer OIDC with short-lived, audience-scoped cloud credentials when the target supports it and deploy authority is explicit.
- Give cache keys stable dependency inputs and bounded restore prefixes. Never cache credentials or attacker-controlled executable state into a trusted job.
- Upload only intentional artifacts, set retention explicitly, and include revision/test identity so evidence can be traced to the candidate.
- Put deployment behind a protected environment, required reviewers, and an explicit authority boundary. A workflow definition does not authorize a deploy.

## Verification

Validate YAML and repository scripts locally when possible. Inspect the resulting GitHub run, effective permissions, action SHAs, artifact contents, and revision before calling remote evidence complete.

Primary sources:

- Workflow syntax and permissions: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
- Security hardening: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
- OIDC: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect
- Artifact attestations: https://docs.github.com/en/actions/security-for-github-actions/using-artifact-attestations
