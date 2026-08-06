# 09 — Reconciliação com o `HEAD` atual

Data da reconciliação: 2026-08-06

Estado: **29 findings abertos; 0 parciais; 0 corrigidos**

Decisão geral: **Not ready**

> Este checkpoint foi sucedido pela [reconciliação após remoção do lifecycle enforcement](10-reconciliation-after-lifecycle-removal.md).

## Escopo e regra de classificação

A auditoria original avaliou o checkout em `797d72cde47f7b94354af5ed49ede4eeb0ea5fdc`, com três mudanças locais então preexistentes. Esta reconciliação compara cada critério de aceitação de `TUX-AUD-001` a `TUX-AUD-029` com o `HEAD` `b46f37643adfa83897427cb2be3c7f383f3b35d9`.

Um finding só seria **corrigido** se seu critério de aceitação estivesse implementado e provado. **Parcial** exigiria que uma parte separável desse próprio critério já estivesse satisfeita. Melhorias próximas, relatórios verdes e documentação nova não recebem crédito parcial quando o mecanismo encontrado pela auditoria permanece igual.

Entre os dois commits, apenas oito arquivos mudaram:

```text
docs/architecture/evaluations.md
docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
docs/evidence/eval-runs.md
evals/promptfoo/assertions/workspace.py
evals/tasks/real-ambiguity.json
skills/git-commit/SKILL.md
skills/git-commit/agents/openai.yaml
tests/test_toolkit.py
```

As mudanças corrigiram o routing de `git-commit`, tornaram determinístico um oráculo de ambiguidade e registraram nova evidência empírica. Elas não alteraram os launchers de hook, schema de receipts, staged-index binding, fingerprint do sistema de avaliação, cardinalidade do aggregate, isolamento do eval home, runner legado, oráculos de trajetória de segurança, defaults de spec ou supply chain citados nos findings.

## Evidência nova, sem extrapolação

Uma execução autorizada de `pnpm run eval:full` passou em 2026-08-06:

| Propriedade | Evidência |
| --- | --- |
| Routing | 34/34 |
| Behavior | 40/40 |
| Security | 12/12 |
| Aggregate | 86/86; 0 falhas; status `pass` |
| Duração | 3.376,701 s (56m16,701s) |
| Controles | approval `never`; dedicated home; network/web/cache remoto desativados; threads não persistidas |
| Privacidade | raw responses não salvas; sem compartilhamento; sem red-team remoto |
| Artefato | `evals/promptfoo/results/full-aggregate-1786013868505052000.json` |
| SHA-256 | `e6916e05766d7450c45a462b9b6e7a455672fb3595d8a32c1cc9211b4cc23827` |

Esse resultado prova que os 86 casos configurados passaram sob o harness corrente. Ele não corrige nem invalida os findings sobre identidade incompleta do snapshot, cardinalidade permissiva ou falsos negativos dos probes. Portanto, é evidência comportamental do catálogo configurado, não certificação de segurança nem prontidão de distribuição.

## Estado de cada finding

| Finding | Estado atual | Evidência de reconciliação |
| --- | --- | --- |
| `TUX-AUD-001` | Aberto | Nenhuma spec/AC/matriz/evidence/review canônica do catálogo foi adicionada. |
| `TUX-AUD-002` | Aberto | `hooks/hooks.json` ainda inicia o guard com `uv run` no cwd consumidor. |
| `TUX-AUD-003` | Aberto | O novo trigger de `git-commit` não faz o guard ler ou vincular os bytes do Git index. |
| `TUX-AUD-004` | Aberto | Policy ainda usa `exists()` sem contrato robusto de `lstat`, tipo e contenção. |
| `TUX-AUD-005` | Aberto | O fingerprint raiz continua limitado a `AGENTS.md` e `skills/**`; o full novo não altera essa identidade. |
| `TUX-AUD-006` | Aberto | A mudança em ambiguidade não cobre external paths arbitrários, egress por executáveis alternativos ou canary transformada. |
| `TUX-AUD-007` | Aberto | O eval home ainda aceita top-level desconhecido e não rejeita symlinks recursivamente. |
| `TUX-AUD-008` | Aberto | O aggregate ainda não compara conjunto exato de rows nem rejeita ausências/duplicatas. |
| `TUX-AUD-009` | Aberto | `evals/run.py --execute` permanece disponível, com herança/sanitização incompatível com o caminho atual. |
| `TUX-AUD-010` | Aberto | Receipts continuam globais, sem mapeamento de evidência por critério. |
| `TUX-AUD-011` | Aberto | Não foi adicionada prova de instalação e comportamento cross-client. |
| `TUX-AUD-012` | Aberto | O onboarding Codex continua sem procedimento reproduzível de instalação/materialização. |
| `TUX-AUD-013` | Aberto | `premortem` e `technical-research` continuam sem `allow_implicit_invocation: false`. |
| `TUX-AUD-014` | Aberto | Não há lifecycle, precedência e fallback canônicos para composição de skills. |
| `TUX-AUD-015` | Aberto | `premortem` ainda pode recomendar critérios/testes sem autoridade explícita de escrita. |
| `TUX-AUD-016` | Aberto | Templates de spec ainda induzem `risk: small` e `single-isolated-reviewer`. |
| `TUX-AUD-017` | Aberto | Roles spec/matrix/evidence ainda podem apontar para o mesmo artefato. |
| `TUX-AUD-018` | Aberto | Contextos dos receipts de test/code review ainda são validados incompletamente. |
| `TUX-AUD-019` | Aberto | A policy default ainda torna layouts com testes co-localizados insatisfatíveis. |
| `TUX-AUD-020` | Aberto | Rules e documentação continuam prometendo mais do que os prefixos literais provados. |
| `TUX-AUD-021` | Aberto | Validação de results continua sem schema/shape completo além da convenção de arquivo. |
| `TUX-AUD-022` | Aberto | Promptfoo resolve SDK 0.144.6 enquanto a dependência direta é 0.146.0. |
| `TUX-AUD-023` | Aberto | O requisito mínimo de Python ainda não está declarado como contrato executável. |
| `TUX-AUD-024` | Aberto | O ledger de migração/proveniência continua ignorado e ligado a caminho pessoal. |
| `TUX-AUD-025` | Aberto | `pnpm audit` ainda encontra 5 high, 7 moderate e 2 low; disposition/licenças seguem pendentes. |
| `TUX-AUD-026` | Aberto | Não foi criada estratégia de colisão para nomes genéricos cross-client. |
| `TUX-AUD-027` | Aberto | Evidence map ainda não registra proveniência reproduzível dos PDFs. |
| `TUX-AUD-028` | Aberto | Cópias de templates continuam sem fonte canônica e verificação de derivação. |
| `TUX-AUD-029` | Aberto | `technical-research` continua sem contrato de rede, modo offline e fallback. |

## Próximos passos

Os work packages permanecem pendentes. A ordem recomendada continua:

1. `WP-01` para tornar o contrato do catálogo independente da implementação.
2. `WP-02` a `WP-04` para corrigir launcher, staged candidate e fail-closed policy.
3. `WP-05` a `WP-08` para tornar identidade, oráculos, isolamento e aggregate de eval confiáveis.
4. `WP-09` a `WP-11` para portabilidade, supply chain e proveniência.
5. Repetir as verificações determinísticas após cada slice. Um novo full só agrega evidência útil depois de mudanças que afetem o catálogo/harness; não é necessário repetir 86 chamadas para esta reconciliação documental.

## Revisão em três fases

### Spec

A decisão `Not ready` decorre dos critérios e claims públicos da auditoria, não da implementação nem do resultado do full. Nenhum critério de aceitação foi reduzido para acomodar o estado atual. O full verde foi classificado apenas dentro do que mede.

### Standards

Os 29 estados foram comparados individualmente com os critérios originais. A classificação evita tanto falso fechamento quanto “parcial” sem unidade de aceitação independente. O relatório preserva o snapshot histórico e adiciona esta reconciliação como overlay atual.

### Risk

Os riscos dominantes permanecem staged-index não verificado, side effects do launcher, identidade/cardinalidade incompletas e falsos negativos de segurança/isolamento. O principal risco de comunicação é confundir 86/86 com certificação desses mecanismos; esta reconciliação torna essa limitação explícita.
