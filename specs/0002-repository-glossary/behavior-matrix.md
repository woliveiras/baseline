# SPEC-0002 behavior and oracle matrix

| Criterion | Scenario | Invariant | Observable oracle | Oracle provenance | Planned verification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| GL-001 | Agent reads the fidelity chain | Specialized language has an immediate definition path | `AGENTS.md` links to the root `GLOSSARY.md` before the chain | spec-derived | `ToolkitStructureTests.test_contract_links_to_canonical_glossary` | See `evidence.md` |
| GL-002 | Agent looks up oracle | Definition separates expected result from execution mechanism and implementation | Oracle entry includes observable result, correctness decision, implementation independence, and test distinction | spec-derived | Same focused structure test | See `evidence.md` |
| GL-003 | Agent looks up behavior/oracle matrix | Matrix purpose and fields are explicit | Matrix entry names criterion, scenario, invariant, oracle, provenance, planned verification, and evidence | spec-derived | Same focused structure test | See `evidence.md` |
| GL-004 | Agent interprets adjacent workflow terms | Obligation, rule, expected result, evaluation mechanism, execution record, origin, chronology, authority, ownership, and review context remain distinct | Glossary states each minimum distinction and adversarial synthetic definitions that collapse or invert them are rejected | spec-derived | Focused canonical and adversarial glossary validation | See `evidence.md` |
| GL-005 | Maintainer navigates documentation | Glossary is discoverable from the documentation hub | `docs/README.md` links to `../GLOSSARY.md` | spec-derived | Same focused structure test | See `evidence.md` |
