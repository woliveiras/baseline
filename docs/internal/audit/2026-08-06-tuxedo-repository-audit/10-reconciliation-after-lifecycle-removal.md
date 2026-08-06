# 10 — Reconciliação após remoção do lifecycle enforcement

Data: 2026-08-06

Estado no `HEAD` `8776a6a`: **22 findings abertos; 7 encerrados por remoção de escopo; 0 corrigidos por fortalecimento do mecanismo**

Decisão geral: **Not ready**

## Mudança de produto

O mantenedor decidiu validar primeiro o workflow declarativo em tarefas reais. `SPEC-0001`, ADR 0002 e o commit `8776a6a` removeram:

- `hooks/hooks.json` e o launcher Python `guard.py`;
- policy e completion-receipt templates;
- review-receipt JSONs da raiz e da skill `verify`;
- fixtures e testes específicos do hook;
- capabilities e claims públicos de lifecycle enforcement.

`AGENTS.md` agora exige declarativamente oráculo antes da implementação, escopo autorizado, três reviews reconstruídos, candidato staged pertencente à tarefa e autorização antes de trabalho adicional. Codex Rules continuam opcionais e limitadas à autoridade de comandos. O produto instalado não executa UV ou Python no checkout consumidor.

## Regra de status

“Encerrado por remoção de escopo” significa que a superfície e seu claim foram retirados. Não significa que o mecanismo anterior foi corrigido nem que a garantia passou a existir em outra camada. Findings restantes continuam abertos até satisfazerem seus critérios originais ou serem explicitamente substituídos por uma decisão de produto equivalente.

## Findings reconciliados

| Finding | Estado | Evidência atual |
| --- | --- | --- |
| `TUX-AUD-001` | Aberto, com progresso | `SPEC-0001` prova a cadeia para esta decisão; o catálogo completo de 17 skills ainda não foi mapeado. |
| `TUX-AUD-002` | Encerrado por remoção de escopo | Launcher UV/Python e todo o diretório `hooks/` foram removidos. |
| `TUX-AUD-003` | Encerrado por remoção de escopo | Não existe mais claim de commit gate; staged ownership é uma obrigação declarativa. |
| `TUX-AUD-004` | Encerrado por remoção de escopo | Policy e parser de policy foram removidos. |
| `TUX-AUD-005` | Aberto | Fingerprint do sistema de avaliação continua incompleto. |
| `TUX-AUD-006` | Aberto | Oráculos de security trajectory não foram alterados neste slice. |
| `TUX-AUD-007` | Aberto | Allowlist e symlinks do eval home não foram alterados. |
| `TUX-AUD-008` | Aberto | Aggregate ainda não prova o conjunto exato de rows. |
| `TUX-AUD-009` | Aberto | Runner legado continua disponível; apenas seu metadata de workflow foi atualizado. |
| `TUX-AUD-010` | Encerrado por remoção de escopo | Completion receipts foram removidos; SPEC-0001 liga seus próprios critérios diretamente à matriz/testes/evidência. |
| `TUX-AUD-011` | Aberto, com progresso | Runtime consumidor foi removido, mas instalação/comportamento cross-client ainda não foi provado. |
| `TUX-AUD-012` | Aberto | Onboarding Codex reproduzível não foi implementado. |
| `TUX-AUD-013` | Aberto | Invocation policy de deep work não mudou. |
| `TUX-AUD-014` | Aberto | Lifecycle e precedência de composição de skills não foram definidos. |
| `TUX-AUD-015` | Aberto | Autoridade standalone de `premortem` não foi alterada. |
| `TUX-AUD-016` | Aberto | Defaults de classificação/review dos templates não mudaram. |
| `TUX-AUD-017` | Encerrado por remoção de escopo | Roles e hashes do completion receipt foram removidos. |
| `TUX-AUD-018` | Encerrado por remoção de escopo | Validação mecânica de contextos foi removida; reviews agora declaram contexto sem claim de enforcement. |
| `TUX-AUD-019` | Encerrado por remoção de escopo | Policy e seus tree scopes default foram removidos. |
| `TUX-AUD-020` | Aberto | Limitações dos prefixos de Rules permanecem documentadas e não mudaram. |
| `TUX-AUD-021` | Aberto | Shape validation de results não mudou. |
| `TUX-AUD-022` | Aberto | Divergência entre SDK direto e efetivo não mudou. |
| `TUX-AUD-023` | Aberto | Python mínimo do toolchain mantenedor ainda não é um contrato executável. |
| `TUX-AUD-024` | Aberto | Ledger de migração/proveniência não mudou. |
| `TUX-AUD-025` | Aberto | Supply-chain disposition não foi executada. |
| `TUX-AUD-026` | Aberto | Estratégia de colisão cross-client não foi criada. |
| `TUX-AUD-027` | Aberto | Proveniência reproduzível dos PDFs não mudou. |
| `TUX-AUD-028` | Aberto | Templates remanescentes ainda precisam de fonte canônica explícita. |
| `TUX-AUD-029` | Aberto | Contrato offline/rede de `technical-research` não mudou. |

## Evidência determinística

| Evidência | Resultado |
| --- | --- |
| Testes fail-first de SPEC-0001 | 3/3 falharam pelos boundaries esperados antes da implementação |
| Testes focados após implementação | 3/3 passaram |
| Suíte unitária | 63/63 passaram; seis testes do hook removidos e três oráculos declarativos adicionados |
| Dry-run legado | 48 runs; fingerprint atual `4268cf00971d61b58c59fb31b133f61c85525faa3742e48f8e331d7b9d72fd4a` |
| Promptfoo config | válida |
| Validators oficiais | plugin válido; 17/17 skills válidas |
| Inventário instalado | nenhum `hooks/`, Python, projeto UV, policy, completion receipt ou review JSON |

## Evidência empírica

O full 86/86 anterior continua válido somente para o snapshot em que foi executado. `AGENTS.md`, `verify`, `git-commit`, `ci-workflow` e o fingerprint mudaram; nenhuma nova chamada de modelo foi autorizada por esta decisão. O ledger de tarefas reais está vazio e será preenchido em [declarative-workflow-trials.md](../../../evidence/declarative-workflow-trials.md).

## Próxima ordem racional

1. Executar 10–20 tarefas reais e registrar somente falhas observadas do workflow declarativo.
2. Continuar `WP-01` para cobrir o catálogo completo, sem recriar receipts.
3. Tratar `WP-05`–`WP-11` conforme prioridade; itens exclusivos do hook/policy/receipt foram retirados.
4. Só reconsiderar um hook se uma falha recorrente tiver oráculo mecânico estreito e solução sem runtime consumidor.

## Revisão

### Spec

SPEC-0001 preserva o objetivo do usuário: rigor de oráculo, escopo, review, commit e autoridade sem representar instruções como enforcement. Nenhum critério antigo foi enfraquecido para declarar um mecanismo verde; o mecanismo foi removido explicitamente.

### Standards

O slice usa UV/PNPM apenas como toolchain mantenedor, mantém Rules/testes/CI em suas responsabilidades e registra fail-first, passing evidence e três contextos reconstruídos. Histórico da auditoria permanece intacto; este documento é um overlay posterior.

### Risk

O risco aceito é a ausência de bloqueio mecânico durante o experimento. Permanecem ainda 22 findings não relacionados ou só parcialmente beneficiados. O full histórico não deve ser apresentado como evidência do novo contrato.
