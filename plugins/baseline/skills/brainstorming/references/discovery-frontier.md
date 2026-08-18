# Bounded discovery frontier

Load this only when the problem is too nebulous for one-pass alternatives or when unresolved dependencies require iterative questioning. Keep the frontier in conversation. Do not create a file, specification, ticket set, tracker entry, or prototype by default.

Classify each unresolved item before asking about it:

| Frontier item | Treatment |
| --- | --- |
| Researchable fact | Inspect repository evidence or route current external evidence to `technical-research`. Do not ask the user to discover a fact cheaply available elsewhere. |
| Owner decision | Ask one focused question that states the materially different consequences. Do not disguise a preference as research. |
| Testable uncertainty | Propose the cheapest discriminating experiment and the signal that would change the decision. A prototype is only one possible experiment and must be separately authorized. |
| Domain ambiguity | Route vocabulary, invariants, or ownership conflicts to `shape-domain`. |

Order the frontier by blocking dependency: resolve an item first only when its answer can eliminate downstream branches. Ask at most one focused question per round. Use a default budget of three question rounds; continue beyond it only when the user explicitly requests deeper discovery. At the budget boundary, stop and report the smallest unresolved decision plus the cheapest next evidence.

Stop earlier when outcomes and non-goals are clear, material facts are known or bounded, owner decisions are made or explicitly deferred, constraints and authority are sufficient, and a next verification seam exists. Feed one remaining incompatible interpretation to `refine`, established options to `decision-framework`, and approved behavior to the applicable implementation workflow.

If an experiment is useful, state its hypothesis, observable signal, time box, isolation, cleanup, and authority. Do not create a file or mutate code, Git, a tracker, or an external system unless that action is separately authorized.
