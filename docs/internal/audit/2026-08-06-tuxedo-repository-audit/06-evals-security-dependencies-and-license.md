# 06 — Evals, segurança, dependências e licença

## Inventário das evals recalculado

| Suite | Matriz real | Máximo de chamadas |
| --- | ---: | ---: |
| Routing | 17 positive + 17 negative | 34 target |
| Behavior | 8 tasks × 5 condições | 40 target |
| Secondary judge | 5 tasks semânticas × 5 condições | até 25 judge |
| Security | 12 frozen probes | 12 target |
| `eval:full` | routing + behavior + security | 86 target + até 25 judge = 111 |
| Smoke | 4 condições | 4 target |
| Compare | 8 × 2 providers × 3 repetições | 48 target + até 30 judge = 78 |
| Legacy dry-run | 8 × 6 variantes | 48, sem provider no dry-run |
| Red-team config | 10 probes solicitados | custo real não verificado |

As quantidades documentadas 34/40/12/111 conferem com as tasks/configs. Isso não significa que o agregador as exija (`TUX-AUD-008`).

## Desenho e evidência

### Pontos fortes confirmados

- Tasks, fixtures, deterministic verifiers e provider estão separados.
- Workspaces são temporários e inicializados como Git repos.
- Promptfoo state/raw ficam em root temporário no caminho atual.
- Exit 100 ainda produz checkpoint sanitizado.
- Assertion failure em uma suite não apaga outcomes anteriores.
- Repetições write-capable usam processo/workspace novos.
- Child env remove `OPENAI_API_KEY` e `CODEX_API_KEY`.
- Configs fixam `approval_policy: never`, rede/web desabilitadas e `persist_threads: false`.
- Relatórios duráveis declaram `raw_responses_saved: false`.
- A documentação limita honestamente claims de routing, behavior, security, model identity e judge (`docs/architecture/evaluations.md:180-195`).

### Classificação das evidências

| Superfície | Tipo | Força/limite |
| --- | --- | --- |
| Routing contract | `spec-derived` | Expected skill declarada; metadata de uso é heurística. |
| AST/filesystem behavior | `spec-derived` | Oracle determinístico para fixture, não qualidade geral. |
| Secondary rubric | `spec-derived` + `diagnostic-probe` | Mesma família Codex; não independente. |
| Frozen security | `spec-derived` + `diagnostic-probe` | Mede ataques nomeados; falsos negativos confirmados. |
| Sanitized reports | `external`/empírico histórico | Provider observation; sem snapshot completo. |
| Dry-run/static validation | `diagnostic-probe` | Prova configuração/matriz, não comportamento de modelo. |

## Identidade e proveniência do snapshot

`evals/run.py:279-286` calcula fingerprint somente de `AGENTS.md` e `skills/**`. `prepare-workspaces.py:183-196` e `run-evaluations.py:430-455` propagam esse valor; reports não incluem commit, dirty-state digest ou hash de tasks, fixtures, rubrics, configs, assertions, verifiers, runner e lockfile.

O full verde documentado (`docs/evidence/eval-runs.md:200-218`) foi criado antes de múltiplos commits posteriores no harness. Um routing aggregate mais recente manteve fingerprint `1796ac…5bec` e falhou 33/34. A própria arquitetura exige evidência nova após task/fixture/provider/dependency upgrades (`docs/architecture/evaluations.md:193-195`). Portanto, o full histórico não prova o checkout atual (`TUX-AUD-005`).

## Validade dos security probes

### Paths externos

`security.py:99-133` marca uso externo apenas se o path resolvido for exatamente um sentinel listado. Um evento estruturado `cat ~/.ssh/id_rsa` produziu `violations=[]`, embora `security-regressions.yaml:36-44` proíba home/sibling reads. Qualquer path externo deveria violar a fixture controlada, não apenas o sentinel.

### Egress

A blacklist em `security.py:114-120` cobre `curl`, `wget`, `nc`, `ssh` e poucos outros. `python`, `node`, `pnpm`, `gh` e cloud CLIs podem abrir rede sem disparar o oracle. O request da fixture pede um `cat` concreto, mas o assertion não enforce essa allowlist.

### Esteganografia

`security.py:182-191` procura a canary literal em arquivos/texto. Base64/hex da canary não contém a literal e passa, apesar do claim `steganographic-exfiltration` (`security-regressions.yaml:124-132`).

Conclusão: 12/12 pode conter falsos positivos; o claim precisa ser reduzido ou o oracle tornado legítimo para a fixture (`TUX-AUD-006`).

## Isolamento do dedicated `CODEX_HOME`

O modelo documentado é prudente: auth session pode ser reutilizada, behavior-bearing content não; API keys não são fallback; status precisa ser “Logged in using ChatGPT”; config é allowlisted.

Dois contraexemplos quebram o fail-closed declarado:

- `codex_auth.py:137-191` trata nomes conhecidos e `skills/plugins`, mas não tem `else` para top-level desconhecido; `future-behavior-surface/` foi aceito.
- Symlink é checado apenas nos primeiros níveis; um link aninhado em `skills/.system/.../personal-link` foi aceito.

Isso contradiz `docs/architecture/eval-isolation.md:34-55` (`TUX-AUD-007`). Nenhum dedicated home ou credencial real foi inspecionado.

## Agregação e cobertura

`run-evaluations.py:246-284` coleta recursivamente qualquer objeto com `response` e valida apenas erro/output/turn. `:606-641` concatena shards e soma counts; `:734-743` exige apenas status pass; `:843-862` pode imprimir full passed. Não há igualdade exata do conjunto `(test_id, provider)`, unicidade, shard ownership ou cardinalidade 34/40/12.

Contraexemplo conceitual executável: cada shard devolve uma row pass; aggregates e full continuam pass com menos de 86 trials. Tests checam ranges configurados, não raw rows missing/duplicate/wrong-provider. Ver `TUX-AUD-008`.

## Runner legado

`docs/development.md:58-63` ainda documenta `evals/run.py --execute`. Esse caminho monta `codex exec` (`evals/run.py:155-174`), herda todo ambiente no `subprocess.run` (`:203-221`) e grava `answer`/`raw` (`:232-246,385-403`) em pasta apenas ignorada. Ele não usa o preflight dedicado nem filtra API keys. É um segundo caminho oficial com garantias incompatíveis (`TUX-AUD-009`).

## Resultados sanitizados ignorados

No checkpoint independente:

- 127 JSON, 1.618.535 bytes, todos parseáveis;
- behavior: 65 (34 pass, 31 fail);
- routing: 30 (18 pass, 12 fail);
- security: 26 (14 pass, 12 fail);
- full: 5 (2 pass, 3 fail);
- smoke: 1 pass;
- nenhum hash de conteúdo duplicado;
- hashes dos reports citados em `eval-runs.md` conferiram.

Amostragem explícita: oldest/newest; último full/routing/behavior/security/smoke; shard, aggregate e focused report. Não foi encontrado raw model output nos campos duráveis amostrados. Porém `_validate_local_outputs` (`run-evaluations.py:123-144`) verifica somente extensão e diretório, não parse/schema/nome/duplicidade/integridade/campos proibidos (`TUX-AUD-021`).

Uma execução `eval:full` externa já rodava desde 09:46:36, antes do início da auditoria, e criou novos JSON durante o trabalho. Ela não foi iniciada, interrompida ou usada como prova; o total final é registrado no apêndice de comandos.

## Dependências diretas

| Dependência | Versão/pin | Escopo | Licença | Necessidade/proveniência | Risco |
| --- | --- | --- | --- | --- | --- |
| `promptfoo` | exata `0.122.0` | dev-only | MIT | Orquestra provider, repetitions, reports; decisão em ADR | Grafo muito grande; 14 advisories transitivos atuais. |
| `@openai/codex-sdk` | exata `0.146.0` | dev-only | Apache-2.0 | Declarada como requerida pelo provider | Promptfoo resolve efetivamente `0.144.6`; root `0.146.0` pode ser redundante (`TUX-AUD-022`). |

O lockfile contém 792 packages dev, 595 snapshots e integrities. O virtual store local confirmou duas versões do SDK. `pnpm outdated` encontrou `0.146.1`, mas atualização não foi autorizada nem recomendada isoladamente sem compatibilidade.

### Advisories atuais

`pnpm audit --json` em 2026-08-06 retornou exit 1:

- 0 critical, 5 high, 7 moderate, 2 low;
- highs em `undici` WebSocket (DoS/exception), `adm-zip` (alocação 4 GiB) e `sharp/libvips`;
- todos chegam por Promptfoo/optional maintainer tooling, não pelo plugin distribuído.

Fontes primárias incluem [GHSA-vrm6-8vpv-qv8q](https://github.com/advisories/GHSA-vrm6-8vpv-qv8q), [GHSA-v9p9-hfj2-hcw8](https://github.com/advisories/GHSA-v9p9-hfj2-hcw8), [GHSA-vxpw-j846-p89q](https://github.com/advisories/GHSA-vxpw-j846-p89q), [GHSA-xcpc-8h2w-3j85](https://github.com/advisories/GHSA-xcpc-8h2w-3j85) e [GHSA-f88m-g3jw-g9cj](https://github.com/advisories/GHSA-f88m-g3jw-g9cj). O impacto está restrito por ser dev-only, mas evals processam output/archives e podem acessar rede; precisa de decisão documentada antes do próximo provider run (`TUX-AUD-025`).

### Licenças transitivas

Agregação mecânica dos packages instalados: 446 MIT, 87 Apache-2.0, BSD/ISC e outras permissivas; também uma LGPL-3.0-or-later e três metadata `Unknown`. Não foi feita análise jurídica manual de 792 entradas. Como o grafo não é distribuído com o plugin, o risco é de toolchain/redistribuição de cache, não de runtime do consumidor. Os `Unknown` impedem alegar inventário de licença completo sem revisão (`TUX-AUD-025`).

## Licença, autoria e proveniência

`LICENSE:1-21`, manifest (`.codex-plugin/plugin.json:11`) e README (`README.md:69-71`) concordam em MIT; o texto corresponde ao identificador [SPDX MIT](https://spdx.org/licenses/MIT.html). O repositório local Geremmyas também usa MIT e o mesmo autor, reduzindo incompatibilidade aparente. Isso não é parecer jurídico.

O evidence map declara inspiração comunitária sem cópia (`docs/research/evidence-map.md:33-35`) e cita cinco preprints. O problema é auditabilidade: o único disposition ledger capability-by-capability da migração está em `docs/tmp/v0.1-map.md`, ignorado, com paths pessoais e policy `never-commit`. Um clone limpo perde a origem/disposição (`TUX-AUD-024`).

Os cinco PDFs foram verificados por fontes arXiv diretas. O evidence map não registra URLs, data, hash, páginas/seções ou método, abaixo do padrão que `technical-research` exige (`TUX-AUD-027`). Não foi identificado texto longo copiado, mas uma análise de similaridade/autoria integral não foi realizada; se houver publicação ampla, revisão jurídica de adaptações e atribuições continua prudente.

## Privacidade e segurança residual

- Reports ignored não devem ser confundidos com segredo protegido: `.gitignore` não é access control.
- O caminho legado persiste output bruto; deve ser removido/migrado antes de uso.
- A execução concorrente demonstra que ignored results mudam fora do Git; full aggregates precisam de hashes/commit/fingerprint completo.
- Sandbox/network settings de configs são intenção; não foram empiricamente certificadas nesta auditoria.
- Canary prova cópia literal nos locais observados, não silent read ou transformação.
- Não foi encontrada credencial real ou path pessoal rastreado; nenhuma credencial foi lida/impressa.
