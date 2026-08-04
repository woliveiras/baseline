---
name: security-review
description: Review a software change for technology-neutral security, privacy, data-loss, and authority risks using verifiable evidence. Use when behavior crosses trust boundaries, handles untrusted input or sensitive data, changes privileges, or performs destructive/external actions; defer stack-specific remediation to dedicated future skills.
---

# Security Review

Apply general security principles without inventing framework-specific advice.

1. Read the full spec, behavior/oracle matrix, data flows, interfaces, deployment assumptions, diff, tests, and authority boundaries.
2. Build the smallest useful [threat model](./references/threat-model.md): assets, actors, trust boundaries, entry points, capabilities, abuse cases, and impact.
3. Verify input validation and canonicalization at trust boundaries, output handling, authentication versus authorization, least privilege, separation of duties, fail-safe defaults, complete mediation, and safe error behavior.
4. Trace sensitive data through collection, storage, transit, logs, caches, artifacts, backups, retention, deletion, and third parties. Minimize exposure and never print secrets as evidence.
5. Check state changes for replay, race, partial failure, idempotency, rollback, auditability, destructive scope, and explicit authority.
6. Map findings to identifiable spec criteria or propose a spec correction. Require negative or abuse-case oracles proportional to risk; classify their provenance.
7. Report evidence-backed findings separately from hardening suggestions and unknowns. Do not claim a security guarantee from static review or passing tests.

Do not provide TypeScript, Go, Python, Android, API-framework, browser-framework, cloud, or database-specific recipes in this skill. Route those to project evidence or future dedicated skills.
