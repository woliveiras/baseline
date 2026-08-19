---
name: security-review
description: Review a software change or CI workflow for technology-neutral security, privacy, data-loss, and authority risks using verifiable evidence. Use for trust boundaries, untrusted or fork-controlled input, secrets, sensitive data, permissions, privileges, or destructive and external actions. This owns requests limited to security risks. When security is secondary to broader work, compose with the owning workflow; defer stack-specific remediation to dedicated skills.
---

# Security Review

Apply general security principles without inventing framework-specific advice.

1. Read the governing input, expected behavior, data flows, interfaces, deployment assumptions, diff, tests, and authority boundaries.
2. Build the smallest useful [threat model](./references/threat-model.md): assets, actors, trust boundaries, entry points, capabilities, abuse cases, and impact.
3. Verify input validation and canonicalization at trust boundaries, output handling, authentication versus authorization, least privilege, separation of duties, fail-safe defaults, complete mediation, and safe error behavior.
4. Trace sensitive data through collection, storage, transit, logs, caches, artifacts, backups, retention, deletion, and third parties. Minimize exposure and never print secrets as evidence.
5. Check state changes for replay, race, partial failure, idempotency, rollback, auditability, destructive scope, and explicit authority.
6. Map findings to identifiable expected behavior or propose an input correction. Require negative or abuse-case checks proportional to risk.
7. Report evidence-backed findings separately from hardening suggestions and unknowns. Do not claim a security guarantee from static review or passing tests.
8. When withheld authority blocks an external or destructive operation, state exactly which operation was not performed, the specific authority, destination and local evidence required to continue, and the safest authorized next step. Do not merely report that authority is absent.

Do not provide TypeScript, Go, Python, Android, API-framework, browser-framework, cloud, or database-specific recipes in this skill. Route those to project evidence or future dedicated skills.
