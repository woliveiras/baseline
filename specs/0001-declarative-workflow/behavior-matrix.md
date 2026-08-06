# SPEC-0001 behavior and oracle matrix

| Criterion | Scenario | Invariant | Observable oracle | Provenance | Planned test | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| DW-001 | Installed inventory | No lifecycle runtime or receipt machinery is distributed | Repository inventory lacks hook/policy/receipt/review-JSON surfaces and manifest hook capability | spec-derived | `ToolkitStructureTests.test_distributed_product_has_no_lifecycle_runtime` | Focused fail-first and passing runs recorded in `evidence.md` |
| DW-002 | Material task workflow | Oracle precedes implementation; scope and reviews remain explicit | Contract contains the ordered workflow and affected skills preserve their responsibilities | spec-derived | `ToolkitStructureTests.test_contract_defines_declarative_task_flow` plus official skill validators | Focused passing run; full validators pending |
| DW-003 | Additional work discovered | Authority does not expand | Contract explicitly requires stopping and requesting authority | independent | `ToolkitStructureTests.test_contract_defines_declarative_task_flow` | Focused passing run |
| DW-004 | Public guarantee | Guidance is not called mechanical enforcement | Public docs and manifest omit lifecycle-enforcement claims; Rules remain scoped to commands | spec-derived | `ToolkitStructureTests.test_public_docs_do_not_claim_lifecycle_enforcement` | Focused passing run |
| DW-005 | Future hook proposal | Evidence and no-runtime constraints precede implementation | ADR records reintroduction criteria and no dormant implementation remains | independent | ADR/link/inventory checks | Focused passing run |
| DW-006 | Real-task experiment | Decision uses observed failures | Architecture guide defines 10–20 task observation ledger and six failure categories | spec-derived | Documentation/link inspection | Trial log created with zero post-decision tasks; experiment pending |
