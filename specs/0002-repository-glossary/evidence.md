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

## Identifier-prefix amendment evidence

| Criteria | Test-tree digest | Command | Result | Oracle provenance |
| --- | --- | --- | --- | --- |
| GL-006–GL-007 fail-first | `fc525638e95f2f1c700bb612d2274e4f9f4e9251` | `uv run python -m unittest -v tests.test_toolkit.ToolkitStructureTests.test_contract_links_to_canonical_glossary` before the glossary tables were added | 1/1 failed because `## Identifier and evidence prefixes` was absent | spec-derived |
| GL-006–GL-007 passing | `fc525638e95f2f1c700bb612d2274e4f9f4e9251` | Same focused command after implementation and whitespace-aware prose validation | 1/1 passed; namespace expansions, ownership, contextual `RM` collision, and documentation abbreviations were present | spec-derived |

The first post-implementation focused failure was a test-authoring issue: the
test required a prose sentence on one physical Markdown line. The final oracle
normalizes whitespace only for prose while retaining exact table-row checks.
It therefore permits ordinary Markdown wrapping without relaxing any required
prefix or expansion.
