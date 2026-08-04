---
name: design-deep-modules
description: Design or review high-leverage modules with small stable interfaces, hidden complexity, explicit seams, adapters, locality, and reversible migration. Use when module boundaries materially affect behavior or change cost; do not use for cosmetic restructuring.
---

# Design Deep Modules

Use depth, seams, adapters, leverage, locality, and the deletion test as diagnostics, not slogans.

1. Start from domain behavior, spec invariants, callers, state ownership, side effects, failure modes, change history, contracts, and tests.
2. Apply the deletion test: identify which caller concepts and coordination disappear if the module is removed. Pass-through indirection with no hidden decision has little depth.
3. For consequential boundaries, load [boundary options](./references/boundary-options.md) and compare at least two materially different interfaces under the same scenarios.
4. Prefer small interfaces that let callers express intent while the module owns relevant coordination, dependency lifecycle, translation, and failure handling.
5. Put external mechanisms behind adapters; keep domain policy out of translation layers. Hide dependencies whose choices belong inside the module, but expose obligations callers truly own.
6. Evaluate test coupling. Protect behavior at the boundary; retain internal tests only for complex invariants that are uneconomical to observe externally.
7. Plan reversible slices, compatibility, rollback, evidence seams, and authority before irreversible operations.
8. Use Mermaid only when three or more modules, dependencies, or migration steps are hard to understand in prose. Show dependency direction, seams, and proposed change; never generate HTML.

Record trade-offs in the active spec and an ADR only when the repository's decision threshold is met. Draw operational rules from recognized modular-design references; citations never substitute for repository evidence.
