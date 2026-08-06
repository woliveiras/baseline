# Auditoria integral do repositório Tuxedo

Data da auditoria: 2026-08-06

Estado: **completa para o snapshot local auditado, com limitações empíricas explícitas**

Decisão geral: **Not ready**

Reconciliação mais recente: `HEAD` `8776a6a`; **22 findings abertos e 7 encerrados por remoção de escopo**. Consulte [a reconciliação após remoção do lifecycle enforcement](10-reconciliation-after-lifecycle-removal.md). A [reconciliação anterior](09-reconciliation-2026-08-06.md) e o snapshot abaixo permanecem como registros históricos.

## Índice

1. [Escopo e metodologia](01-scope-and-methodology.md)
2. [Inventário e coverage ledger](02-inventory-and-coverage.md)
3. [Produto, arquitetura e contratos](03-product-architecture-and-contracts.md)
4. [Skills, agentes e documentação](04-skills-agents-and-documentation.md)
5. [Hooks, Rules, templates e testes](05-hooks-rules-templates-and-tests.md)
6. [Evals, segurança, dependências e licença](06-evals-security-dependencies-and-license.md)
7. [Findings](07-findings.md)
8. [Work packages de remediação](08-remediation-work-packages.md)
9. [Matriz de rastreabilidade](appendix-traceability-matrix.md)
10. [Evidência de comandos](appendix-command-evidence.md)
11. [Reconciliação com o HEAD atual](09-reconciliation-2026-08-06.md)
12. [Reconciliação após remoção do lifecycle enforcement](10-reconciliation-after-lifecycle-removal.md)

## Snapshot auditado

| Campo | Valor |
| --- | --- |
| Checkout | `<checkout-absoluto-do-tuxedo>` (valor local omitido por portabilidade) |
| Commit | `797d72cde47f7b94354af5ed49ede4eeb0ea5fdc` |
| Branch | `main` |
| Início | `2026-08-06T10:27:55+02:00` |
| Arquivos rastreados | 126 arquivos, 16.387 linhas |
| Skills | 17 |
| Estado Git inicial | três modificações preexistentes, listadas abaixo |

Modificações preexistentes, preservadas e não atribuídas à auditoria:

```text
 M docs/architecture/evaluations.md
 M docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
 M docs/evidence/eval-runs.md
```

O objeto da auditoria foi o checkout real — commit mais essas modificações locais — e não uma abstração de `HEAD` limpo.

## Conclusão executiva

O Tuxedo tem uma proposta clara e uma base incomumente disciplinada: o conteúdo distribuído é pequeno, client-neutral, sem runtime acidental; as 17 skills são concisas; os limites de autoridade são explícitos; e os testes determinísticos, validators, dry-run e validações estáticas passam. A documentação também distingue corretamente evidência comportamental de certificação de runtime.

Entretanto, o sistema não está pronto para distribuição responsável sob as garantias atuais. A cadeia de fidelidade que o produto exige de terceiros não existe como artefato durável para o próprio catálogo. Dois gates críticos não vinculam o fato que seus nomes sugerem: o hook pode modificar o projeto consumidor ao iniciar e o receipt de commit valida a working tree, não os bytes staged. Além disso, a evidência verde histórica não identifica o harness completo; os probes de segurança têm falsos negativos determinísticos; o isolamento aceita superfícies desconhecidas; e o agregador pode aprovar uma matriz incompleta. Assim, “mecanicamente verificado” e “stack atual verde” são claims mais fortes do que a implementação sustenta.

## Contagem de findings

| Severidade | Quantidade |
| --- | ---: |
| P0 — Critical | 0 |
| P1 — High | 10 |
| P2 — Medium | 16 |
| P3 — Low | 3 |
| **Total** | **29** |

## Cinco riscos dominantes

1. Um receipt pode aprovar um conteúdo da working tree enquanto outro conteúdo já está staged para commit (`TUX-AUD-003`).
2. O launcher de hook executado no cwd da sessão pode criar `.venv` e `uv.lock` no repositório consumidor, contrariando o contrato “sem runtime dependency” (`TUX-AUD-002`).
3. Resultados de eval antigos mantêm o mesmo fingerprint após alterações em tasks, assertions, runner ou dependências (`TUX-AUD-005`).
4. Probes de segurança podem aceitar leitura de `~/.ssh`, egress por executáveis fora da blacklist e exfiltração codificada (`TUX-AUD-006`).
5. O catálogo não possui spec, critérios e matriz duráveis que permitam reconstruir a intenção sem ler a própria implementação (`TUX-AUD-001`).

## Prontidão por dimensão

| Dimensão | Decisão | Motivo principal |
| --- | --- | --- |
| Produto | Ready with conditions | Proposta e escopo claros; falta contrato rastreável do catálogo. |
| Distribuição | Not ready | Instalação não reproduzível e hook pode mutar o consumidor. |
| Documentação | Ready with conditions | Clara e honesta, mas onboarding, composição e proveniência têm lacunas. |
| Testes | Ready with conditions | 65/65 passam; oráculos não cobrem staged index, host cwd e vários bypasses. |
| Evals | Not ready | Fingerprint, isolamento, cardinalidade e probes invalidam o claim verde atual. |
| Segurança | Not ready | Falsos negativos confirmados e um caminho legado herda ambiente pessoal. |
| Manutenção | Not ready | Não há cadeia spec → critérios → evidência do próprio produto. |
| Portabilidade | Ready with conditions | Formato portável; instalação e comportamento cross-client não comprovados. |

## Checks em uma linha

Passaram: validator oficial do plugin; validators oficiais das 17 skills; 65 testes unitários; dry-run legado com 48 runs; seis configurações Promptfoo; JSON/YAML válidos, exceto a fixture deliberadamente malformada; AST dos 13 scripts Python; links/anchors de 65 documentos Markdown incluindo o relatório; `git diff --check` e whitespace check dos 11 arquivos novos. Não havia shell script rastreado. `pnpm audit` retornou 14 advisories (5 high, 7 moderate, 2 low) e `pnpm outdated` encontrou uma atualização patch do SDK. Detalhes, duração, limites e exit codes estão no [apêndice de comandos](appendix-command-evidence.md).

Não foram executados login, `eval:full`, provider/model calls, red-team real, deploy, publicação ou qualquer ação Git externa. Uma execução `eval:full` iniciada por outro processo antes desta auditoria foi observada e explicitamente excluída da evidência.

Posteriormente, uma execução autorizada passou 86/86 em 56m16,701s. Essa evidência está reconciliada sem extrapolação em [09](09-reconciliation-2026-08-06.md): ela prova os casos configurados, mas não fecha os findings sobre validade e completude do harness.

## Ordem recomendada

Começar por `WP-01` (contrato do catálogo), enquanto `WP-02` (hook launcher), `WP-03` (binding ao staged index) e `WP-04` (fail-closed de policy) avançam em paralelo. Em seguida, executar `WP-05` a `WP-08` para corrigir validade e isolamento das evals. Somente então produzir nova evidência empírica autorizada. A sequência completa está em [work packages](08-remediation-work-packages.md).

Nenhum código, skill, teste, template, configuração, spec ou documentação preexistente foi corrigido por esta auditoria. As únicas escritas autorizadas são os arquivos deste diretório de relatório.
