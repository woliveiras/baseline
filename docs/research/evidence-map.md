# Engineering evidence map

This maintainer-only map separates empirical results from engineering heuristics, product decisions, and community inspiration. The five supplied papers are preprints from 2026; their settings and limitations constrain every derived rule.

## Empirical results

| Claim | Source | Evidence type | Derived rule | Mechanism | Affected surface | Eval | Limitations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Existing regression suites can admit semantically wrong patches; mutation-guided augmentation changed top-agent resolved rates by 4.2-9.0% in the reported SWE-bench Verified study. | Li et al., *Are Benchmark Tests Strong Enough?*, arXiv:2604.01518v1 | Benchmark experiment, 211 augmented instances | Treat passing tests as evidence, require criterion traceability, and seek counterexamples for material changes. | guidance + detection | `spec`, `tdd`, `verify`; receipt presence only | `spec-inconsistent`, `post-hoc-contamination` | Benchmark-specific; mutation adequacy is not semantic completeness and executable mutation testing is deferred. |
| Tests generated after faulty code detected fewer faults than independently generated tests in the reported workflow (14% vs 25%). | Konstantinou, Tambon, Papadakis, *On the risk of coding before testing*, arXiv:2607.05139v1 | Controlled LLM generation experiment | Review the spec and derive behavior/oracle matrices before exposing reviewers to the new implementation. Classify implementation-aware tests. | guidance + detection | `spec`, `tdd`, `verify` | `post-hoc-contamination` | Model/task selection and generated-test setting limit generalization; independence reduces bias but does not guarantee correctness. |
| Prompt-induced volume of agent-written tests changed process cost more reliably than task outcomes; prints often dominated assertions. | Chen et al., *Rethinking the Value of Agent-Generated Tests*, arXiv:2602.07900v2 | Multi-model trajectory study plus prompt intervention | Prefer actionable oracles over test count; do not equate more agent-written tests with stronger evidence. | guidance | `tdd`, `bugfix`, `verify` | `bug-with-regression` | SWE-bench/light-scaffold setting; current models and other harnesses may differ. |
| Graph navigation improved hidden-dependency tasks in one 30-task benchmark, while tool adoption was inconsistent. | Paipuru, *CodeCompass / Navigation Paradox*, arXiv:2602.20048v1 | Controlled tool-augmentation benchmark, 258 completed trials | Trace dependency seams for multimodule work and use explicit navigation checklists; do not mandate an external graph service. | guidance | `design-deep-modules`, `improve-architecture`, `technical-research` | `multi-module-change` | Single codebase/tool/model family, incomplete planned trials, independent preprint; no universal impact-scan claim. |
| Cleaner variants did not change pass rate in the reported study but used 7-8% fewer tokens and 34% fewer file revisitations. | Trivedi and Schmitt, *Does Code Cleanliness Affect Coding Agents?*, arXiv:2605.20049v1 | Controlled minimal-pair study, 660 trials | Treat locality, names, and reduced complexity as maintainability and navigation heuristics, not correctness gates. | guidance | architecture skills, `docs` | `multi-module-change` | One agent/model, Python/Java, author-curated tasks; cost transfer and long-term compounding are unproven. |

## Engineering heuristics

| Heuristic | Basis | Use | Non-claim |
| --- | --- | --- | --- |
| Fail first on the smallest realistic seam. | TDD, debugging practice, Geremmyas experience | `tdd`, `bugfix` | A failing test can still encode the wrong behavior. |
| Prefer deep modules, information hiding, locality, and explicit seams. | *A Philosophy of Software Design* and established modular design practice | architecture skills | No single metric proves module depth or quality. |
| Preserve reversibility and use evidence before broad changes. | *The Pragmatic Programmer* and operational risk practice | architecture, decisions, premortem | Reversibility does not make a change safe by itself. |

## Product decisions

| Decision | Reason | Mechanism |
| --- | --- | --- |
| Specs remain active through review and maintenance. | Prevent silent drift between intent, tests, and code. | transversal `AGENTS.md`, templates, skill contracts, evals |
| Hooks enforce only mechanical facts. | Semantic judgments are not reliable lifecycle interlocks. | hashes, exact grants, narrow command patterns |
| Evals remain Codex-first and maintainer-only. | Codex is the initial evaluation client, not a conceptual dependency of portable skills. | `evals/`, excluded from plugin manifest |
| Stack-specific security and technology skills are deferred. | Avoid unsupported synthesis and keep v0.1 technology-neutral. | migration map and routing descriptions |

## Community inspiration

Community engineering skills, including Matt Pocock's catalog, informed coverage comparison and gap discovery. No names, phrases, or procedures were copied. Community practice is not represented as empirical evidence.

## Bibliography

- Chenglin Li et al. “Are Benchmark Tests Strong Enough? Mutation-Guided Diagnosis and Augmentation of Regression Suites.” arXiv:2604.01518v1, 2026.
- Michael Konstantinou, Florian Tambon, and Mike Papadakis. “On the risk of coding before testing.” arXiv:2607.05139v1, 2026.
- Zhi Chen et al. “Rethinking the Value of Agent-Generated Tests for LLM-Based Software Engineering Agents.” arXiv:2602.07900v2, 2026.
- Tarakanath Paipuru. “CodeCompass: Navigating the Navigation Paradox in Agentic Code Intelligence.” arXiv:2602.20048v1, 2026.
- Priyansh Trivedi and Olivier Schmitt. “Does Code Cleanliness Affect Coding Agents?” arXiv:2605.20049v1, 2026.
