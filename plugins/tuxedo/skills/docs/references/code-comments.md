# Durable code comments

Prefer, in order:

1. expressive names;
2. focused functions and modules;
3. intention-revealing types and interfaces;
4. a comment only for a reason, constraint, risk, or history that cannot be inferred safely.

Use `ENG-NOTE[kind][optional-id]: concise durable explanation`; the second bracket is an optional ID. Use one of:

- `bug`
- `invariant`
- `compat`
- `security`
- `decision`

The ID is optional but recommended for a stable issue, incident, or contract. Put the comment at the nearest seam that applies the rule and explain why, never what the line does. Do not store temporary status, plans, commands, or disposable context.

Examples:

```text
// ENG-NOTE[bug][GH-482]: An empty cursor previously restarted pagination and duplicated the first page.
// ENG-NOTE[invariant][session-expiry]: Refresh credentials must never outlive the owning session.
// ENG-NOTE[compat][wire-v2]: Keep this field optional until all v1 consumers have migrated.
```

Find notes portably with:

```bash
rg 'ENG-NOTE\['
```

Keep local information in code or its regression test. Put rules that cross modules, systems, or teams in architecture documentation; put accepted hard-to-reverse decisions in an ADR and open material decisions in an RFC. Do not add a parser, CLI, indexer, runtime, or complex schema for this convention.
