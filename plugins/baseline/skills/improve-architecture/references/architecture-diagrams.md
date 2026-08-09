# Architecture diagrams

Use the smallest Mermaid view that adds verification value. Label every edge and distinguish current facts from inferred or proposed relationships.

```mermaid
flowchart LR
    caller["Caller"] -->|"domain intent"] boundary["Proposed boundary"]
    boundary -->|"adapter contract"] external["External mechanism"]
    test["Deterministic seam"] -.->|"substitutes mechanism"] boundary
```

For migrations, show current and target dependency direction plus ordered reversible slices. A diagram supplements paths, contracts, risk, and evidence; it never replaces them.
