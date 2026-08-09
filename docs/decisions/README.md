# Architecture decisions

| Number | Title | Status | Date | Summary |
| --- | --- | --- | --- | --- |
| [0001](./0001-use-promptfoo-as-evaluation-orchestrator.md) | Use Promptfoo as the evaluation orchestrator while retaining Tuxedo deterministic verifiers | accepted | 2026-08-05 | Promptfoo owns generic evaluation orchestration while Tuxedo retains domain-specific fixtures, snapshots, fingerprints, and deterministic oracles. |
| [0002](./0002-defer-lifecycle-hooks-pending-empirical-need.md) | Keep lifecycle enforcement out of the installed product | accepted | 2026-08-06 | Keep the consumer runtime-free; require a recurring, objectively observable failure before considering a narrow mechanical gate. |
| [0003](./0003-adopt-proportional-baseline-and-move-sdd.md) | Adopt the proportional baseline and move SDD ownership | accepted | 2026-08-09 | Replace distributed `spec` with ephemeral `measurer`; keep SDD independently installable from Storehouse without runtime coupling. |
