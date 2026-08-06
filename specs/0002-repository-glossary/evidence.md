# SPEC-0002 evidence

## Fail-first evidence

| Criteria | Command | Expected failure | Observed failure | Oracle provenance |
| --- | --- | --- | --- | --- |
| GL-001–GL-005 | `uv run python -m unittest tests.test_toolkit.ToolkitStructureTests.test_contract_links_to_canonical_glossary -v` | The canonical glossary is absent | 1/1 failed at `glossary_path.is_file()` before the glossary or links were implemented | spec-derived |

## Passing evidence

| Criteria | Command | Result | Oracle provenance |
| --- | --- | --- | --- |
| GL-001–GL-005 | Same focused command as fail-first evidence | 1/1 passed | spec-derived |
| GL-001–GL-005 | `uv run python -m unittest discover -s tests -v` | 64/64 passed | implementation-aware regression suite |
| GL-001–GL-005 | Official plugin validator and official skill validator for every skill, using temporary PyYAML through UV | Plugin valid; 17/17 skills valid | external |
| GL-001/GL-004 | `uv run python evals/run.py --dry-run` | 48 runs; current fingerprint `882e65944e807ffe5e193941eb6fda52189434cd924ad12ef1620dcd082c4723` | implementation-aware |
| GL-001/GL-005 | Repository Markdown local-link check | 82 Markdown files; 120 local links; 0 broken | independent |
| GL-001–GL-004 | Isolated spec review | Approved after clarifying medium risk and all required distinctions | independent |
| GL-001–GL-005 | Isolated test review | Approved after adversarial coverage was expanded to every required semantic boundary | independent |
| GL-001–GL-005 | Isolated code review | Approved after three correction rounds; no remaining Spec, Standards, or Risk findings | implementation-aware |
| GL-001–GL-005 | `git diff --check` | Passed before final review artifacts | implementation-aware |
| GL-001–GL-005 | Tracked shell inventory | 0 shell scripts; syntax check not applicable | diagnostic-probe |

## Documentation decision

- Decision: `required`.
- Rationale: this task establishes the canonical meaning of terms used by the repository contract.
- Updated artifacts: `GLOSSARY.md`, `AGENTS.md`, root and documentation-hub navigation, canonical spec/evidence templates and installed references/assets, SPEC-0002, and its semantic structural regression test.

## Residual limitations

- A structural test can prove the presence and organization of required concepts, but not that every reader will interpret prose identically.
- Domain-specific specifications may define a more specific oracle; the glossary explicitly preserves that precedence.
