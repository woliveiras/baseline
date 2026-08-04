---
name: spec
description: Create or reconcile an active software specification with routing metadata, stable acceptance criteria, invariants, behavior-oracle traceability, risk, authority, and review policy. Use for material features or behavior changes before implementation; do not use for trivial copy-only edits.
---

# Spec

Make the spec the active source of intended behavior across implementation, verification, review, maintenance, and resumption.

1. Read the complete governing objective, domain vocabulary, prior specs, contracts, and relevant observed behavior. Metadata never replaces reading the full spec.
2. Resolve or expose contradictions before implementation. Correct the spec explicitly when evidence invalidates an assumption; never let tests or code silently become the new intent.
3. Write compact routing metadata using [metadata](./references/metadata.md). Follow the project's artifact location; use [the bundled template](./assets/spec-template.md) only when no stronger convention exists.
4. Give acceptance criteria stable IDs. Record normal, edge, invalid, compatibility, and recovery behavior plus invariants and explicit exclusions.
5. Build the [behavior and oracle matrix](./references/behavior-matrix.md). Define observable oracles before the new implementation is shown to the reviewer.
6. Classify blast radius and risk as `trivial`, `small`, `medium`, or `large/high-risk`. Choose review separation and evidence proportional to risk, never line count.
7. Record authority granted and withheld, dependencies, change surfaces, contracts, reversibility, and unresolved decisions.
8. Keep the spec current while work proceeds. Every accepted correction must reconcile the matrix, tests, implementation, docs, and evidence.

A spec is ready when criteria are identifiable, contradictions are resolved or explicitly blocked, testable behavior has oracle candidates, risk and authority are routed, and exclusions prevent silent scope expansion.
