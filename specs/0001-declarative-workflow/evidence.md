# SPEC-0001 evidence

## Fail-first evidence

| Criteria | Command | Expected failure | Observed failure | Provenance |
| --- | --- | --- | --- | --- |
| DW-001–DW-006 | `uv run python -m unittest tests.test_toolkit.ToolkitStructureTests.test_distributed_product_has_no_lifecycle_runtime tests.test_toolkit.ToolkitStructureTests.test_contract_defines_declarative_task_flow tests.test_toolkit.ToolkitStructureTests.test_public_docs_do_not_claim_lifecycle_enforcement -v` | Current product still exposes hook runtime, lacks the declarative section, and claims lifecycle enforcement | 3/3 failed for exactly those boundaries before implementation | spec-derived |

## Passing evidence

| Criteria | Command | Result | Provenance |
| --- | --- | --- | --- |
| DW-001–DW-006 | Same focused command as fail-first evidence | 3/3 passed after implementation | spec-derived |
| DW-001–DW-006 | `uv run python -m unittest discover -s tests -v` | 63/63 passed after hook-specific tests were removed and three declarative invariants were added | implementation-aware regression suite |
| DW-001/DW-002 | Official plugin validator plus official skill validator for every skill, using temporary PyYAML through UV | Plugin valid; 17/17 skills valid | external |
| DW-002/DW-004 | `uv run python evals/run.py --dry-run` | 48 runs; current fingerprint `4268cf00971d61b58c59fb31b133f61c85525faa3742e48f8e331d7b9d72fd4a` | implementation-aware |
| DW-004 | `pnpm run promptfoo:validate` | Configuration valid | external |

Link checks and final Git checks remain pending until the audit reconciliation is complete.

## Documentation decision

- Decision: `required`
- Rationale: the installed product surface and public guarantee change.
- Updated artifacts: `AGENTS.md`, `README.md`, architecture, development guide, ADR index, trial log, audit reconciliation, affected skills.

## Residual limitations

- Declarative compliance can only be measured empirically; deterministic structure tests cannot prove that an agent follows the workflow.
- No provider run is authorized solely by this specification.
