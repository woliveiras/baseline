---
name: session-bridge
description: Create a truthful handoff that lets another software-engineering session resume from canonical artifacts and real evidence. Use only when the user explicitly requests a handoff, pause, or session bridge; do not claim to measure context-window health or replace specs.
---

# Session Bridge

1. Inspect the current objective, boundaries, active spec, behavior matrix, plan/tasks, diff, test outputs, Git state, and authority record.
2. Use [the handoff template](./assets/handoff-template.md). Link canonical artifacts rather than copying their full contents.
3. Preserve objective and exclusions, decisions and reasons, stable criterion IDs, real test state, open hypotheses, manual work, granted and withheld authority, unrelated worktree state, and the next recommended step.
4. Distinguish verified facts, reported facts, assumptions, and stale evidence. Include exact commands and results only when actually run.
5. Never describe the handoff as a replacement for specs, tests, Git, or documentation. Do not infer how much context remains or claim that a future session will load the file automatically.

Write the smallest durable handoff in the location chosen by the user or repository. If no file change is authorized, return the same structure in the response.
