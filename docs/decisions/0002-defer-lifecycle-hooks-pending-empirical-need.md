---
status: accepted
date: 2026-08-06
decision-makers:
  - William Oliveira
---

# Keep lifecycle enforcement out of the installed product

ADR 0003 supersedes this record's former SDD-specific workflow. The no-runtime
decision, optional Codex Rules boundary, and threshold for any future mechanical
gate remain active.

## Context

Lifecycle hooks previously invoked a Python guard through UV to check policies,
receipts, and hashes. That placed development tooling in the consumer execution
path, risked discovering or synchronizing consumer environments, and could make
mechanical receipts appear to prove semantic quality, chronology, or review.

Portable guidance, repository tests, CI, sandboxing, approvals, and human review
already own different parts of this problem. Baseline should not add a second
runtime policy system without a recurring, objectively observable failure.

## Decision

The installed Baseline product contains no lifecycle hooks, launcher, policy or
receipt format, review-file generator, or Python/UV runtime dependency.

- `AGENTS.md` and skills provide declarative engineering guidance.
- Tests and CI provide repository-specific executable checks.
- Optional Codex Rules cover a narrow set of direct command-authority forms.
- Sandbox, approval policy, repository policy, and humans remain authoritative.

Guidance cannot mechanically prove chronology, semantic adequacy, review
independence, scope fidelity, or staged ownership. Public documentation must not
claim otherwise.

## Reintroducing a gate

A future mechanical gate is acceptable only when all of these are true:

- a failure recurs in real work and has material impact;
- the protected invariant is objectively observable;
- false-positive and false-negative cases have deterministic coverage;
- the gate does not mutate or discover the consumer project unexpectedly;
- the installed product gains no consumer runtime dependency;
- the documentation states the gate's limits precisely.

Semantic judgment stays in governing inputs, skills, tests, review, and human
authority.

## Consequences

- Consumers need no UV, Python, or Baseline runtime.
- The workflow remains declarative rather than a technical gate.
- Baseline accepts that some process violations cannot be blocked mechanically.
- Superseded hook implementations, trials, receipts, and validation logs remain
  recoverable from Git history and do not occupy the current product tree.

See [workflow and command boundaries](../architecture/enforcement.md) for the
current responsibility model.
