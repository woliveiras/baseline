---
name: spec
description: Create or reconcile an active software specification with routing metadata, stable acceptance criteria, invariants, behavior-oracle traceability, risk, authority, and review policy. Use for material features or behavior changes before implementation; do not use for trivial copy-only edits.
---

# Spec

Make the spec the active source of intended behavior across implementation, verification, review, maintenance, and resumption.

1. Read the complete governing objective, domain vocabulary, prior specs, contracts, and relevant observed behavior. Metadata never replaces reading the full spec.
2. Resolve or expose contradictions before implementation. Correct the spec explicitly when evidence invalidates an assumption; never let tests or code silently become the new intent.
3. Write compact routing metadata using [metadata](./references/metadata.md). Follow the project's artifact location; use [the bundled spec template](./assets/spec-template.md) only when no stronger convention exists.
4. Give acceptance criteria stable IDs. Record normal, edge, invalid, compatibility, and recovery behavior plus invariants and explicit exclusions.
5. Build the [behavior and oracle matrix](./references/behavior-matrix.md) as a separate artifact, using [its template](./assets/behavior-matrix-template.md) when needed. Define observable oracles before the new implementation is shown to the reviewer.
6. Classify with [the scope tiers](./references/scope-tiers.md). Choose review separation and evidence proportional to the highest applicable risk, never line count.
7. Record whether documentation is required or not required, with a rationale and intended artifacts. Do not let `not-required` mean unexamined.
8. Record authority granted and withheld, dependencies, change surfaces, contracts, reversibility, and unresolved decisions.
9. Keep the spec current while work proceeds. Every accepted correction must reconcile the matrix, tests, implementation, docs, and evidence.

A spec is ready when criteria are identifiable, contradictions are resolved or explicitly blocked, testable behavior has oracle candidates, risk and authority are routed, and exclusions prevent silent scope expansion.
