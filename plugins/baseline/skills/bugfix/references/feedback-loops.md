# Difficult feedback loops

Load this only when the normal focused test is unavailable, too slow, or intermittent. Choose the smallest loop that observes the actual symptom.

| Loop | Use when | Guard against |
| --- | --- | --- |
| Unit, integration, or E2E test | A stable seam exists | Testing a lower layer than the symptom |
| CLI fixture | Input/output or exit behavior is the contract | User profile and ambient config leakage |
| HTTP script | A request/response sequence reproduces the bug | Live production targets and nondeterministic data |
| Headless browser | Browser lifecycle or UI behavior matters | Locale, timing, and unstable selectors |
| Trace replay | A captured sequence can be sanitized and replayed | Secrets, obsolete schema, and partial causality |
| Property test or fuzzing | An invariant spans many inputs | Unbounded runtime and unreproducible seeds |
| `git bisect run` | A deterministic script distinguishes good/bad commits | Destructive worktree state and flaky exit codes |
| Differential comparison | A trusted reference implementation exists | Treating another buggy implementation as authority |
| Human-in-loop script | Automation cannot observe the physical or subjective boundary | Vague steps and unrecorded outcomes |

Require a clear setup, action, expected signal, timeout, cleanup, and stable exit interpretation. Make failures reproducible with captured seeds or fixtures. Never point an experimental loop at production without explicit authority.
