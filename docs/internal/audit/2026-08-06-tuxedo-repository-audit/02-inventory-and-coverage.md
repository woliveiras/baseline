# 02 — Inventário e coverage ledger

## Resumo mecânico

| Superfície rastreada | Arquivos |
| --- | ---: |
| Raiz/manifest/licença/toolchain | 8 |
| `docs/` | 11 |
| `evals/` | 34 |
| `hooks/` | 2 |
| `skills/` | 58 |
| `templates/` | 9 |
| `tests/` | 4 |
| **Total** | **126** |

O total recalculado foi 16.387 linhas. Não há PDF, shell script, symlink ou arquivo binário rastreado. `rg --files -uu` encontrou aproximadamente 108 mil entradas por causa de `node_modules/`; essa árvore ocupava aproximadamente 3,8 GiB e não é produto distribuído.

## Legenda de disposição

- `RI`: revisado integralmente, com leitura de conteúdo e confronto contextual.
- `FH`: revisado como membro de família homogênea, com inventário total, parse/schema, comparação mecânica e amostras explícitas.
- `GO`: placeholder/gerado; validado por origem, convenção e invariantes, sem conteúdo semântico para ler.
- `NE`: não revisado. **Nenhum arquivo rastreado ficou nesta categoria.**

## Coverage ledger completo

Cada linha abaixo representa um arquivo rastreado e sua disposição. A listagem foi derivada de `git ls-files`, não de `rg --files`.

### Raiz, plugin e toolchain

```text
RI  .codex-plugin/plugin.json
RI  .gitignore
RI  AGENTS.md
RI  LICENSE
RI  README.md
RI  package.json
FH  pnpm-lock.yaml
RI  pnpm-workspace.yaml
```

O lockfile foi parseado integralmente como YAML, agregado por packages/snapshots/integrity/license e amostrado nos nós diretos de Promptfoo e Codex SDK. Não foi feita leitura manual linha a linha das 792 entradas dev.

### Documentação

```text
RI  docs/README.md
RI  docs/architecture/enforcement.md
RI  docs/architecture/eval-isolation.md
RI  docs/architecture/evaluations.md
RI  docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
RI  docs/decisions/README.md
RI  docs/development.md
RI  docs/evidence/eval-runs.md
RI  docs/guides/using-the-eval-harness.md
RI  docs/internal/skill-creator-limitations.md
RI  docs/research/evidence-map.md
```

Os links locais de todos os documentos Markdown rastreados foram validados, incluindo anchors. Os três documentos de eval modificados antes da auditoria foram lidos como estado real, e o diff contra `HEAD` foi preservado como evidência de procedência.

### Evals — harness, assertions, configs e fixtures

```text
FH  evals/fixtures/catalog.json
RI  evals/promptfoo/assertions/routing.py
RI  evals/promptfoo/assertions/security.py
RI  evals/promptfoo/assertions/trajectory.py
RI  evals/promptfoo/assertions/workspace.py
FH  evals/promptfoo/compare-config.yaml
GO  evals/promptfoo/generated/.gitkeep
FH  evals/promptfoo/promptfooconfig.yaml
RI  evals/promptfoo/prompts.py
FH  evals/promptfoo/redteam-config.yaml
GO  evals/promptfoo/results/.gitkeep
FH  evals/promptfoo/routing-config.yaml
RI  evals/promptfoo/scripts/codex_auth.py
RI  evals/promptfoo/scripts/prepare-workspaces.py
RI  evals/promptfoo/scripts/run-evaluations.py
FH  evals/promptfoo/security-config.yaml
FH  evals/promptfoo/smoke-config.yaml
RI  evals/promptfoo/tests.py
FH  evals/promptfoo/tests/behavior.yaml
FH  evals/promptfoo/tests/routing-contract.json
FH  evals/promptfoo/tests/routing.yaml
FH  evals/promptfoo/tests/security-regressions.yaml
GO  evals/results/.gitkeep
FH  evals/rubrics/secondary.json
RI  evals/run.py
FH  evals/tasks/bug-with-regression.json
FH  evals/tasks/clear-local-change.json
FH  evals/tasks/multi-module-change.json
FH  evals/tasks/no-change-correct.json
FH  evals/tasks/post-hoc-contamination.json
FH  evals/tasks/real-ambiguity.json
FH  evals/tasks/security-authority.json
FH  evals/tasks/spec-inconsistent.json
RI  evals/verifiers.py
```

Todos os JSON/YAML foram parseados; os oito tasks e seis configs foram comparados ao catálogo de 48 dry-runs e à matriz 34/40/12. Amostras semânticas explícitas: `spec-inconsistent`, `post-hoc-contamination`, `security-authority`; routing positivo, negativo e colisão; primeiro/último probe de segurança; configs smoke, full behavior e red-team. Assertions e três runners foram lidos integralmente.

### Hooks

```text
RI  hooks/hooks.json
RI  hooks/scripts/guard.py
```

Além da leitura, foram exercitados em fixtures temporárias: ausência/má-formação/policy symlink, host cwd com projeto UV, overlap de scopes, alias de artifacts/reviews, staged index divergente e formas de comando Git.

### Skills — todos os 58 arquivos

```text
RI  skills/brainstorming/SKILL.md
FH  skills/brainstorming/agents/openai.yaml
RI  skills/bugfix/SKILL.md
FH  skills/bugfix/agents/openai.yaml
RI  skills/bugfix/references/feedback-loops.md
RI  skills/ci-workflow/SKILL.md
FH  skills/ci-workflow/agents/openai.yaml
RI  skills/decision-framework/SKILL.md
FH  skills/decision-framework/agents/openai.yaml
RI  skills/decision-framework/references/evidence-types.md
RI  skills/design-deep-modules/SKILL.md
FH  skills/design-deep-modules/agents/openai.yaml
RI  skills/design-deep-modules/references/boundary-options.md
RI  skills/docs/SKILL.md
FH  skills/docs/agents/openai.yaml
RI  skills/docs/references/decision-record.md
RI  skills/docs/references/project-docs.md
RI  skills/docs/references/proposal.md
RI  skills/git-commit/SKILL.md
FH  skills/git-commit/agents/openai.yaml
RI  skills/improve-architecture/SKILL.md
FH  skills/improve-architecture/agents/openai.yaml
RI  skills/improve-architecture/references/architecture-diagrams.md
RI  skills/premortem/SKILL.md
FH  skills/premortem/agents/openai.yaml
RI  skills/refine/SKILL.md
FH  skills/refine/agents/openai.yaml
RI  skills/refine/references/decision-tree.md
RI  skills/security-review/SKILL.md
FH  skills/security-review/agents/openai.yaml
RI  skills/security-review/references/threat-model.md
RI  skills/session-bridge/SKILL.md
FH  skills/session-bridge/agents/openai.yaml
RI  skills/session-bridge/assets/handoff-template.md
RI  skills/shape-domain/SKILL.md
FH  skills/shape-domain/agents/openai.yaml
RI  skills/shape-domain/references/context-mapping.md
RI  skills/spec/SKILL.md
FH  skills/spec/agents/openai.yaml
RI  skills/spec/assets/behavior-matrix-template.md
RI  skills/spec/assets/spec-template.md
RI  skills/spec/references/behavior-matrix.md
RI  skills/spec/references/metadata.md
RI  skills/spec/references/scope-tiers.md
RI  skills/tdd/SKILL.md
FH  skills/tdd/agents/openai.yaml
RI  skills/tdd/references/provenance.md
RI  skills/technical-research/SKILL.md
FH  skills/technical-research/agents/openai.yaml
RI  skills/technical-research/references/source-quality.md
RI  skills/verify/SKILL.md
FH  skills/verify/agents/openai.yaml
RI  skills/verify/assets/code-review.json
RI  skills/verify/assets/evidence-template.md
RI  skills/verify/assets/spec-review.json
RI  skills/verify/assets/test-review.json
RI  skills/verify/references/review-contract.md
RI  skills/verify/references/scope-tiers.md
```

Cada `SKILL.md`, referência e asset foi lido individualmente. Os 17 YAML foram parseados e confrontados em família com nome, descrição, `allow_implicit_invocation`, dependências e o respectivo `SKILL.md`. Todos passaram pelo validator oficial.

### Templates

```text
RI  templates/codex/tuxedo.rules
RI  templates/policy/policy.json
RI  templates/policy/receipts.json
RI  templates/review/code.json
RI  templates/review/spec.json
RI  templates/review/tests.json
RI  templates/spec/behavior-matrix.md
RI  templates/spec/evidence.md
RI  templates/spec/spec.md
```

Os templates foram confrontados com hooks, skills/assets, documentação e casos normal, bloqueado e autorizado. Os sete pares de cópia foram comparados byte a byte; estavam idênticos no snapshot.

### Testes

```text
FH  tests/fixtures/hooks/pretool-malformed.json
FH  tests/fixtures/hooks/pretool-missing.json
FH  tests/fixtures/hooks/pretool-valid.json
RI  tests/test_toolkit.py
```

`pretool-malformed.json` é intencionalmente JSON inválido; por isso foi excluído, com justificativa, da validação global de JSON. O arquivo de 65 testes foi lido por famílias e executado integralmente.

## Superfícies não rastreadas/ignoradas relevantes

| Superfície | Estado observado | Disposição e risco |
| --- | --- | --- |
| `node_modules/` | ~107.529 arquivos; ~3,8 GiB | Inventário mecânico e supply-chain via lockfile/package metadata; não distribuído. |
| `evals/promptfoo/results/*.json` | 127 relatórios/1.618.535 bytes no checkpoint; contagem cresceu durante execução externa | Todos os 127 parseados e agregados; amostra explícita. Novos arquivos finais inventariados, mas não usados como evidência. |
| `evals/promptfoo/generated/` | somente `.gitkeep` no checkpoint | Sem probes gerados persistidos. |
| `evals/results/` | somente `.gitkeep` | Sem relatório legado ignorado no checkpoint. |
| `docs/tmp/v0.1-map.md` | 89 linhas, ignorado por `.gitignore:16` | Lido integralmente; único disposition ledger da migração, contém paths pessoais e `never-commit`; finding `TUX-AUD-024`. |
| `__pycache__/`, `*.pyc` | artefatos preexistentes ignorados | Não removidos; checks foram executados com `PYTHONDONTWRITEBYTECODE=1`. |
| Dedicated eval home | fora do checkout | Não inspecionado para não tocar auth/credenciais; somente código de validação e fixtures sintéticas foram auditados. |
| PDFs do contexto | ausentes localmente | Reconstruídos de URLs arXiv em temp externo; bytes originais não verificáveis. |

## Integridade, secrets e paths pessoais

- Nenhum path pessoal absoluto foi encontrado em arquivo rastreado.
- Ocorrências de `OPENAI_API_KEY`, `CODEX_API_KEY`, auth e canaries em arquivos rastreados são contratos/testes, não valores reais.
- Nenhum segredo real foi identificado pelo scan textual orientado a padrões; isso não equivale a secret scanning criptográfico completo.
- O único path pessoal observado fica no `docs/tmp/v0.1-map.md` ignorado.
- Todos os 595 snapshots do lockfile observados tinham integrity quando aplicável; o lockfile não foi alterado.

## Risco residual de cobertura

Não há arquivo rastreado sem disposição. O risco residual concentra-se em: interpretação jurídica das licenças transitivas; comportamento real de clientes não executados; sandbox/rede/auth que não puderam ser empiricamente exercidos; e resultados ignored criados concorrentemente após o checkpoint.
