---
name: refine
description: Resolve material ambiguity in a software request with a proportional decision tree. Invoke from incompatible interpretations even without naming this skill; do not use because a task is large or when repository evidence already makes the path clear.
---

# Refine

Turn only material ambiguity into a decision-ready input and keep the normal result in conversation.

1. Read the request, nearest instructions, decisions, domain artifacts, code, and tests that can answer questions cheaply.
2. List only choices that change observable behavior, scope, constraints, compatibility, authority, or a hard-to-reverse boundary.
3. Use the [decision tree](./references/decision-tree.md) to order dependencies and resolve branches from evidence.
4. Ask one focused question only when at least two materially different paths remain; explain their consequences without inventing certainty.
5. Stop as soon as behavior, scope, constraints, authority, and the next verification seam are sufficient. Do not reopen accepted decisions or ask about reversible implementation details.

A fully defined `L/XL` task proceeds without `refine`. An `S/M` task can require `refine` when two behavioral interpretations conflict. Do not create a specification or persistent plan by default; update an existing authorized decision surface only when durability is independently required.

Return resolved choices, bounded assumptions, the smallest open decision if any, authority, and the ready next step in the conversation.
