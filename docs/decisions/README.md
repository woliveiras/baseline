# Architecture decisions

| Number | Title | Status | Date | Summary |
| --- | --- | --- | --- | --- |
| [0001](./0001-use-promptfoo-as-evaluation-orchestrator.md) | Use Promptfoo as the evaluation orchestrator while retaining Tuxedo deterministic verifiers | accepted | 2026-08-05 | Promptfoo owns generic evaluation orchestration while Tuxedo retains domain-specific fixtures, snapshots, fingerprints, and deterministic oracles. |
| [0002](./0002-defer-lifecycle-hooks-pending-empirical-need.md) | Defer lifecycle hooks pending empirical need | accepted | 2026-08-06 | Remove lifecycle runtime and receipts; validate the strict declarative workflow across real tasks before considering a narrow mechanical gate. |
