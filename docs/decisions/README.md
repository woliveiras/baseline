# Architecture decisions

| Number | Title | Status | Date | Summary |
| --- | --- | --- | --- | --- |
| [0001](./0001-use-promptfoo-as-evaluation-orchestrator.md) | Use Promptfoo as the evaluation orchestrator while retaining Baseline deterministic verifiers | accepted | 2026-08-05 | Promptfoo owns generic evaluation orchestration while Baseline retains domain-specific fixtures, snapshots, fingerprints, and deterministic oracles. |
| [0002](./0002-defer-lifecycle-hooks-pending-empirical-need.md) | Keep lifecycle enforcement out of the installed product | accepted | 2026-08-06 | Keep the consumer runtime-free; require a recurring, objectively observable failure before considering a narrow mechanical gate. |
| [0003](./0003-separate-foundation-and-optional-sdd.md) | Separate the engineering foundation from optional SDD | accepted | 2026-08-09 | Keep `measurer` in Baseline and SDD independently installable from Storehouse without runtime coupling. |
