---
name: session-bridge
description: Create a truthful compact continuation that lets another software-engineering session resume from governing inputs, current artifacts, and real results. Use whenever the user explicitly asks to pause ongoing work or hand it to another session, even without naming this skill; do not claim to measure context-window health or replace project documentation.
---

# Session Bridge

1. Inspect the current objective, governing input, boundaries, decisions, diff, test outputs, Git state, and authority record.
2. Use [the handoff template](./assets/handoff-template.md). Link canonical artifacts rather than copying their full contents or narrating task history.
3. Preserve only the state required to resume: objective and exclusions, decisions and reasons, real test state, open hypotheses, blocking dependencies, decision frontier, granted and withheld authority, unrelated worktree state, and the next discriminating check.
4. Distinguish verified facts, reported facts, assumptions, and stale evidence. Include exact commands and results only when actually run.
5. Never describe the handoff as a replacement for governing inputs, tests, Git, or documentation. Do not infer how much context remains or claim that a future session will load the file automatically.

Return the compact structure in conversation by default. Write a file only when the user explicitly requests a durable handoff and chooses its location; a pause or handoff request alone is not file authority. Do not create session histories, task logs, or completed-work archives.
