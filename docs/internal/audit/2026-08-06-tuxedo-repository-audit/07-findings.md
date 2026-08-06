# 07 — Findings

> Estado reconciliado em 2026-08-06 contra `b46f37643adfa83897427cb2be3c7f383f3b35d9`: 29 abertos, 0 parciais e 0 corrigidos. Os detalhes abaixo preservam a evidência do snapshot original; veja [09 — Reconciliação](09-reconciliation-2026-08-06.md) para a verificação individual atual.

Ordem: severidade, dependência e potencial de invalidar outras evidências. “Pode ser isolado” descreve implementação, não autorização para mudar o repositório.

## P1 — High

### TUX-AUD-001 — O próprio catálogo não possui cadeia de fidelidade durável

- **Severidade/confiança/categoria/status:** P1; alta; arquitetura/rastreabilidade; confirmado.
- **Contrato violado:** `AGENTS.md:7-17` e `README.md:9-20` exigem spec → matrix → tests → implementation → evidence → review com IDs estáveis.
- **Evidência local:** `git ls-files` não contém `specs/`, AC/SPEC real fora dos templates, matrix do catálogo, evidence artifact ou review receipt. `templates/spec/*` fornece apenas moldes.
- **Evidência externa:** não necessária; é contrato interno.
- **Explicação/impacto:** `SKILL.md` funciona simultaneamente como intenção e implementação. Um reviewer não reconstrói fase 1 sem ler o objeto julgado; mudanças podem redefinir silenciosamente o contrato.
- **Cenário:** alterar trigger/autoridade de uma skill e ajustar teste textual correspondente; nenhuma AC independente denuncia drift.
- **Causa provável:** migração priorizou conteúdo distribuível e não materializou os receipts de sua própria criação.
- **Recomendação/arquivos:** criar spec canônica do catálogo, ACs, oracle matrix, evidence/reviews; provavelmente nova superfície `specs/` ou equivalente e links em docs/tests.
- **Aceitação:** 17 skills e mecanismos mapeados; AC único por promessa pública; cada AC liga oracle/test/eval/implementation/evidence/review; fase 1 é reconstruível sem `SKILL.md`.
- **Validação:** link/schema checks, coverage matrix completa, review das três fases e todos os required checks.
- **Ordem/dependência/residual/isolamento:** `WP-01`, primeiro; funda os demais; presença estrutural ainda não provará semântica; não isolável.

### TUX-AUD-002 — O launcher do hook modifica o projeto consumidor

- **Severidade/confiança/categoria/status:** P1; alta; hooks/runtime/portabilidade; confirmado.
- **Contrato violado:** “sem runtime dependency” (`docs/development.md:7-11`) e hook sem rede/efeito implícito (`docs/architecture/enforcement.md:122-126`).
- **Evidência local:** `hooks/hooks.json:10-11,22-23` usa `uv run python`; `tests/test_toolkit.py:235-238` não executa no cwd real do fixture.
- **Evidência externa:** [UV `run`](https://docs.astral.sh/uv/concepts/projects/run/) sincroniza o project environment; [Codex hooks](https://developers.openai.com/codex/hooks) executam no cwd da sessão.
- **Explicação/impacto:** UV participa do projeto consumidor antes do guard. Probe sem policy criou `.venv`/`uv.lock`; pyproject inválido retornou exit 2. Pode baixar/buildar dependências, alterar repo e bloquear Bash.
- **Cenário:** abrir projeto Python/UV com plugin ativo e executar Bash sem `.tuxedo/policy.json`.
- **Causa provável:** convenção de toolchain do mantenedor foi aplicada ao lifecycle do consumidor.
- **Recomendação/arquivos:** launcher autocontido/isolado, sem project discovery/sync; `hooks/hooks.json`, possível wrapper e tests; `commandWindows` explícito.
- **Aceitação:** projetos UV válido/inválido/sem policy não mudam nenhum byte, não criam env/lock e não acessam índice; comportamento missing-runtime e Windows documentado.
- **Validação:** E2E da definição real do hook com cwd real, snapshot before/after e offline; suites obrigatórias.
- **Ordem/dependência/residual/isolamento:** `WP-02`, paralelo após AC; runtime ausente ainda requer política; isolável.

### TUX-AUD-003 — O commit gate não valida o staged Git index

- **Severidade/confiança/categoria/status:** P1; alta; integridade/Git; confirmado.
- **Contrato violado:** slice staged verificada em `skills/git-commit/SKILL.md:8-12`, `README.md:43-50` e enforcement commit gate.
- **Evidência local:** `guard.py:79-98,141-162,247-364` lê somente working tree; não lê index/cached diff.
- **Explicação/impacto:** probe com working tree `VALUE=1` receipted e index `VALUE=999` passou em PreToolUse e Stop. O commit pode gravar bytes não revisados.
- **Cenário:** stage malicioso/antigo, restaurar working tree aprovada e executar `git commit`; `commit -a`/substitution amplia TOCTOU.
- **Causa provável:** “snapshot de conclusão” foi modelado como filesystem, não como candidato do trigger.
- **Recomendação/arquivos:** abstração de candidate snapshot; commit usa Git index, Stop usa working tree; `guard.py`, receipt schema, tests/docs.
- **Aceitação:** index != WT, staged deletion/rename/intent-to-add e `commit -a` bloqueiam ou ficam explicitamente fora do claim.
- **Validação:** repos Git temporários e `git show :path`/tree hash; required checks.
- **Ordem/dependência/residual/isolamento:** `WP-03`; depende do contrato de candidate; shell TOCTOU residual deve ser documentado; isolável depois da decisão.

### TUX-AUD-004 — Policy malformada pode falhar aberta ou fora do protocolo

- **Severidade/confiança/categoria/status:** P1; alta; security/fail-closed; confirmado.
- **Contrato violado:** malformed/escaping inputs falham fechados (`docs/architecture/enforcement.md:122-126`).
- **Evidência local:** `guard.py:247-251` usa `exists()` e policy não passa por `resolve_inside`; `load_object` (`:56-65`) não captura todo `OSError`.
- **Explicação/impacto:** symlink quebrado desativa gate; symlink externo é lido; diretório causa traceback exit 1, não JSON deny. Falha de hook não equivale a bloqueio protocolado.
- **Cenário:** checkout contém `.tuxedo/policy.json` quebrado ou trocado por directory/symlink.
- **Causa provável:** tratamento de ausência confundido com tipagem/erro de filesystem.
- **Recomendação/arquivos:** `lstat`, regular file, contenção e política de symlink; capturar filesystem errors e emitir deny; `guard.py`/tests/docs.
- **Aceitação:** internal/external/broken symlink, directory, FIFO, unreadable e removal race nunca allow silencioso nem traceback.
- **Validação:** matriz temporária de tipos/erros e protocolo Codex; required checks.
- **Ordem/dependência/residual/isolamento:** `WP-04`; paralelo; race entre lstat/read continua residual até open seguro; isolável.

### TUX-AUD-005 — Resultados verdes não identificam o snapshot completo

- **Severidade/confiança/categoria/status:** P1; alta; eval provenance; confirmado.
- **Contrato violado:** upgrades de task/fixture/provider/dependency exigem evidência nova (`docs/architecture/evaluations.md:193-195`).
- **Evidência local:** `evals/run.py:279-286` hasheia só `AGENTS.md + skills/**`; propagação em `prepare-workspaces.py:183-196` e report `run-evaluations.py:430-455`; full verde em `docs/evidence/eval-runs.md:200-218` precede commits do harness.
- **Explicação/impacto:** tasks/assertions/runner podem mudar mantendo fingerprint. Um routing posterior com o mesmo fingerprint falhou 33/34.
- **Cenário:** corrigir oracle de security sem tocar skills; report antigo aparenta atual.
- **Causa provável:** product fingerprint foi usado como evaluation-system fingerprint.
- **Recomendação/arquivos:** commit + dirty digest + hash canônico de tasks, fixtures, rubrics, configs, assertions, verifiers, runner e versões resolvidas.
- **Aceitação:** qualquer mudança em input/oracle altera identidade; report registra commit/dirty sem segredo; evidence log marca histórico incompatível.
- **Validação:** mutation matrix de cada entrada e hash determinístico cross-order; sem model call.
- **Ordem/dependência/residual/isolamento:** `WP-05`, antes de novo full; identidade não prova validade do oracle; parcialmente isolável.

### TUX-AUD-006 — Security probes aceitam violações reais

- **Severidade/confiança/categoria/status:** P1; alta; security eval validity; confirmado.
- **Contrato violado:** frozen probe requer estímulo concreto e oracle determinístico legítimo (`AGENTS.md:78-80`).
- **Evidência local:** external path exige igualdade com sentinel (`security.py:99-133`); blacklist curta (`:114-120`); canary somente literal (`:182-191`); claims em `security-regressions.yaml:36-44,124-132`.
- **Explicação/impacto:** probes controlados não detectaram `cat ~/.ssh/id_rsa` nem base64 da canary; `python`/`node` egress não entram na blacklist. 12/12 pode ser falso positivo.
- **Cenário:** concluir patch canônico após ler home; exfiltrar token transformado; egress por Python.
- **Causa provável:** blacklist/sentinel aproximam autoridade geral.
- **Recomendação/arquivos:** allowlist exata por fixture, rejeitar qualquer path fora do workspace, detectar transformações explicitamente suportadas ou reduzir claim.
- **Aceitação:** mutation tests de home/sibling, Python/Node, base64/hex e unknown command falham; documentação enumera limites.
- **Validação:** unit tests dos assertions com trajectories sintéticas; security static config; full somente depois e com autoridade.
- **Ordem/dependência/residual/isolamento:** `WP-06`, antes de novo full; silent read sem trajectory seguirá não comprovável; isolável.

### TUX-AUD-007 — Isolamento aceita superfícies futuras e symlinks aninhados

- **Severidade/confiança/categoria/status:** P1; alta; eval isolation; confirmado.
- **Contrato violado:** managed entries reais e future surfaces fail-closed (`docs/architecture/eval-isolation.md:34-55`).
- **Evidência local:** `codex_auth.py:137-191` não rejeita top-level desconhecido e só checa symlinks nos primeiros níveis.
- **Explicação/impacto:** probes aceitaram `future-behavior-surface/` e symlink aninhado em `skills/.system/.../personal-link`; conteúdo pode contaminar behavior mantendo preflight verde.
- **Cenário:** Codex adiciona surface behavior-bearing ou cache permitido contém link para conteúdo pessoal.
- **Causa provável:** denylist/top-level partial e traversal não recursivo.
- **Recomendação/arquivos:** allowlist explícita de top-level, `lstat` recursivo e validação de shape/proveniência do cache; `codex_auth.py`/tests/docs.
- **Aceitação:** unknown file/dir/symlink falha antes de auth status; symlink em qualquer profundidade falha.
- **Validação:** árvores sintéticas sem tocar dedicated home real.
- **Ordem/dependência/residual/isolamento:** `WP-07`; paralelo; cache real ainda requer trust decision; isolável.

### TUX-AUD-008 — O full pode passar com rows ausentes ou duplicadas

- **Severidade/confiança/categoria/status:** P1; alta; eval aggregation/coverage; confirmado.
- **Contrato violado:** full cobre 34 routing, 40 behavior e 12 security (`docs/architecture/evaluations.md:108-124`).
- **Evidência local:** raw validation não checa ID/cardinalidade (`run-evaluations.py:246-284`); aggregate concatena/soma (`:606-641`); pass depende apenas de status (`:734-743,843-862`).
- **Explicação/impacto:** uma row pass por shard pode produzir aggregates pass com menos de 86 trials; duplicate/wrong-provider também não é infrastructure failure.
- **Cenário:** Promptfoo omite rows por filtro/erro de schema, mas reporta as presentes como pass.
- **Causa provável:** runner confia na cardinalidade da ferramenta e valida response, não a matriz esperada.
- **Recomendação/arquivos:** conjunto esperado `(test_id, provider, shard)`, igualdade exata, unicidade e fingerprints/controls uniformes.
- **Aceitação:** missing, duplicate, unknown, wrong-provider/shard falham; full exige exatamente 34/40/12.
- **Validação:** raw-result fixtures mutantes e aggregate unit tests; sem provider.
- **Ordem/dependência/residual/isolamento:** `WP-08`, antes de full; não prova qualidade das rows; isolável.

### TUX-AUD-009 — Runner legado viola isolamento e sanitização atuais

- **Severidade/confiança/categoria/status:** P1; alta; privacy/auth/duplicate harness; confirmado.
- **Contrato violado:** dedicated home, API keys removidas e nenhum raw output persistido (`AGENTS.md:58-64`).
- **Evidência local:** `docs/development.md:58-63` documenta `--execute`; `evals/run.py:155-174,203-221` herda env; `:232-246,385-403` grava answer/raw.
- **Explicação/impacto:** um caminho oficial pode usar auth/home pessoal e persistir prompts/output/stderr sob pasta apenas ignorada.
- **Cenário:** maintainer executa comando documentado com secrets no ambiente.
- **Causa provável:** harness anterior foi preservado sem parity de controles.
- **Recomendação/arquivos:** desabilitar execute ou migrar integralmente para preflight/env filtrado/report sanitizado; `evals/run.py`, docs/tests.
- **Aceitação:** nenhum caminho herda keys/homes; secret sintético ausente de child env e disco; dry-run/verifiers preservados.
- **Validação:** subprocess fake/fixture sem model call, scan de output temp.
- **Ordem/dependência/residual/isolamento:** `WP-08`/subpacote; antes de qualquer uso; logs de ferramentas externas seguem residual; isolável.

### TUX-AUD-010 — Receipts não rastreiam evidência por critério

- **Severidade/confiança/categoria/status:** P1; alta; fidelity/enforcement; confirmado.
- **Contrato violado:** stable IDs e `criterion → oracle → test → evidence` (`AGENTS.md:7-17`, `skills/tdd/SKILL.md:8-18`).
- **Evidência local:** `templates/policy/receipts.json:14-24` e `guard.py:199-219` têm um par global fail/passing; `templates/spec/evidence.md:3-13` exige AC rows. Test fixture sem AC e `assert True` passa (`tests/test_toolkit.py:268-380,409-423`).
- **Explicação/impacto:** uma prova trivial satisfaz uma spec multi-critério; hashes conservam bytes, não coverage.
- **Cenário:** cinco ACs, apenas um test record global; gate aprova.
- **Causa provável:** receipt foi otimizado para integridade de artefatos, não traceability cardinal.
- **Recomendação/arquivos:** IDs únicos e mapping criterion/test/fail/pass/evidence no receipt; validar estrutura sem alegar semântica.
- **Aceitação:** ausente/duplicado/desconhecido/uncovered bloqueia; todos ACs têm oracle/proveniência/test/evidence.
- **Validação:** negative matrix + compatibility/migration test de schema.
- **Ordem/dependência/residual/isolamento:** `WP-01` + `WP-03`; depende do catálogo AC; presença continuará sem provar qualidade; não totalmente isolável.

## P2 — Medium

### TUX-AUD-011 — Portabilidade é formato, não instalação/comportamento comprovado

- **Severidade/confiança/categoria/status:** P2; alta; portabilidade/distribuição; confirmado.
- **Contrato:** toolkit portátil (`README.md:3,57-65`).
- **Evidência:** checkout tem `skills/`; eval admite layout Codex explícito e 7/17 behavior (`docs/architecture/evaluations.md:180-185`). Docs oficiais de [Codex](https://developers.openai.com/codex/skills/), [Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), [Claude](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) e [OpenCode](https://opencode.ai/docs/skills) usam layouts/precedências distintos.
- **Impacto/cenário/causa:** clone/cópia não auto-descobre skills; routing/authority cross-client não têm evidence; “portável” misturou formato com operação.
- **Recomendação/arquivos:** support matrix, install fixtures e claims por nível; README/docs/evals.
- **Aceitação/validação:** clean-room install/discovery + positive/negative routing mínimo em cada cliente alegado; validator continua verde.
- **Ordem/residual/isolamento:** `WP-09`, após contrato; versões futuras ainda driftam; parcialmente isolável.

### TUX-AUD-012 — Onboarding Codex não é reproduzível

- **Severidade/confiança/categoria/status:** P2; alta; docs/distribution; confirmado.
- **Contrato/evidência:** README diz ser suficiente (`README.md:5,33-41`) mas “add to marketplace” não dá comando/manifest/restart/update/removal; [OpenAI plugin docs](https://developers.openai.com/plugins/build/plugins) exigem passos concretos.
- **Impacto/cenário/causa:** novo usuário depende de conhecimento tácito; docs priorizaram conceito.
- **Recomendação/arquivos:** guia clean-room copiável para add/install/restart/verify/hooks/rules/update/remove.
- **Aceitação/validação:** terceiro segue em home temporário e confirma 17 skills/manifest sem conhecimento prévio.
- **Ordem/residual/isolamento:** `WP-09`; marketplace local depende da versão Codex; isolável após decisão distributiva.

### TUX-AUD-013 — Deep work explícito diverge de `openai.yaml`

- **Severidade/confiança/categoria/status:** P2; alta; routing/authority; confirmado.
- **Contrato/evidência:** `README.md:28,31`; `premortem/agents/openai.yaml:1-4` e `technical-research/agents/openai.yaml:1-4` omitem `allow_implicit_invocation: false`, cujo default Codex é true.
- **Impacto/cenário/causa:** research/premortem podem ser ativados implicitamente, ampliando custo/escopo; metadata driftou do resumo.
- **Recomendação/arquivos:** definir false ou reclassificar README e routing cases.
- **Aceitação/validação:** metadata e docs concordam; casos explicit/implicit positivos/negativos.
- **Ordem/residual/isolamento:** `WP-09`; routing heurístico residual; isolável.

### TUX-AUD-014 — Não há lifecycle/precedência de composição

- **Severidade/confiança/categoria/status:** P2; alta; agent architecture; confirmado.
- **Contrato/evidência:** lista plana em `README.md:24-31`; `spec/SKILL.md:14` e `verify/SKILL.md:11` compartilham matrix; `tdd/SKILL.md:3,10` requer approved, template nasce draft.
- **Impacto/cenário/causa:** refine/spec/premortem/security/tdd/verify podem competir; nenhum owner de aprovação/fallback; catálogo evoluiu por skills locais.
- **Recomendação/arquivos:** state machine com input/owner/output/status/precedência/stop/conflict/fallback.
- **Aceitação/validação:** cenários normal, ambíguo, high-risk, finding/reopen, skill ausente e deadlock têm rota única verificável.
- **Ordem/residual/isolamento:** `WP-09`, após AC; seleção de modelo seguirá heurística; não isolável.

### TUX-AUD-015 — `premortem` pode sugerir escrita sem autoridade explícita

- **Severidade/confiança/categoria/status:** P2; alta; authority; risco fundamentado.
- **Contrato/evidência:** `AGENTS.md:31-33` versus `skills/premortem/SKILL.md:15-16`, que manda adicionar critérios/tests/guards quando “justified”.
- **Impacto/cenário/causa:** skill standalone não herda AGENTS; pedido analítico pode virar edição; limite transversal não foi repetido.
- **Recomendação/arquivos:** exigir autorização explícita; sem ela, proposta apenas em resposta/artefato autorizado.
- **Aceitação/validação:** eval read-only prova zero write e mensagem de bloqueio; validator.
- **Ordem/residual/isolamento:** `WP-09`; cliente ainda aplica hierarchy própria; isolável.

### TUX-AUD-016 — Defaults de spec induzem sub-classificação

- **Severidade/confiança/categoria/status:** P2; média-alta; templates/risk; risco fundamentado.
- **Contrato/evidência:** tiers higher-boundary; `templates/spec/spec.md:7,12` e asset usam `risk: small`/single reviewer.
- **Impacto/cenário/causa:** auth/data-loss pode conservar default por inércia; template escolhe antes da análise.
- **Recomendação/arquivos:** placeholder/unresolved e gate antes de ready; spec templates/ref/tests.
- **Aceitação/validação:** security/release/data-loss nunca aceitam small sem rationale; negative cases.
- **Ordem/residual/isolamento:** `WP-01`; semântica de risco não é mecanicamente provada; isolável.

### TUX-AUD-017 — Roles spec/matrix/evidence podem aliasar

- **Severidade/confiança/categoria/status:** P2; alta; receipt schema; confirmado.
- **Contrato/evidência:** cadeia separada em enforcement; `guard.py:263-272` exige strings/hash, não distinção; probe com um arquivo passou.
- **Impacto/cenário/causa:** separação aparente satisfeita por artefato único; identity model usa path textual.
- **Recomendação/arquivos:** paths canônicos e identidade distinta, inclusive symlink/hardlink.
- **Aceitação/validação:** repeated/`./` alias/symlink/hardlink bloqueiam.
- **Ordem/residual/isolamento:** `WP-03`; conteúdo distinto ainda pode ser semanticamente duplicado; isolável.

### TUX-AUD-018 — Contextos test/code review são validados incompletamente

- **Severidade/confiança/categoria/status:** P2; alta; review receipts; confirmado.
- **Contrato/evidência:** templates exigem booleans; `guard.py:238-244` valida spec e só implementation=false em tests, nada em code. Probes contrários passaram.
- **Impacto/cenário/causa:** receipt contradiz formato oficial mas gate aprova; validator foi implementado assimetricamente.
- **Recomendação/arquivos:** shape/boolean exatos por fase.
- **Aceitação/validação:** chave ausente/extra/type/value errado falha em cada fase.
- **Ordem/residual/isolamento:** `WP-03`; declaração não prova contexto real; isolável.

### TUX-AUD-019 — Policy default bloqueia testes co-localizados

- **Severidade/confiança/categoria/status:** P2; alta; templates/usability; confirmado.
- **Contrato/evidência:** test globs e `src/**/*` (`policy.json:8,12`) com overlap false (`:16`); `guard.py:297-302` bloqueia. `src/example.test.ts` reproduz.
- **Impacto/cenário/causa:** Jest/Vitest comum entra em Stop loop até editar policy; defaults foram combinados sem fixture co-located.
- **Recomendação/arquivos:** defaults por layout ou exclude test patterns da implementation tree.
- **Aceitação/validação:** Python separado, TS co-located e monorepo produzem scopes satisfatíveis.
- **Ordem/residual/isolamento:** `WP-04`; layouts custom continuam configuráveis; isolável.

### TUX-AUD-020 — Claims de Rules excedem os prefixos cobertos

- **Severidade/confiança/categoria/status:** P2; alta; command authority/docs; confirmado.
- **Contrato/evidência:** resumo `README.md:38`; rules `templates/codex/tuxedo.rules:6-124`; tests sete casos `tests/test_toolkit.py:214-232`. Probes wrapper/options retornaram null.
- **Impacto/cenário/causa:** leitor do README pode tratar template parcial como boundary; prefix matching literal não é shell parser.
- **Recomendação/arquivos:** alinhar claims, matriz adversarial, enumerar deliberate gaps; não reimplementar shell.
- **Aceitação/validação:** cada claim tem case positivo/negativo oficial; wrappers/options documentados.
- **Ordem/residual/isolamento:** `WP-04`; aliases/composed shell sempre limitam rules; isolável.

### TUX-AUD-021 — “Shape validation” de results verifica só extensão

- **Severidade/confiança/categoria/status:** P2; alta; evidence retention; confirmado.
- **Contrato/evidência:** docs claim shape (`evaluations.md:72-75`); `_validate_local_outputs` (`run-evaluations.py:123-144`) só testa suffix/type.
- **Impacto/cenário/causa:** JSON truncado/raw payload pode coexistir como validado; nome da função/documento excede o check.
- **Recomendação/arquivos:** schema versionado, parse, naming, forbidden fields, aggregate links/hashes.
- **Aceitação/validação:** malformed/wrong schema/duplicate/raw field falha sem apagar evidence.
- **Ordem/residual/isolamento:** `WP-05`; schema não prova provenance; isolável.

### TUX-AUD-022 — SDK direto não é a versão efetiva do provider

- **Severidade/confiança/categoria/status:** P2; alta; dependency provenance; confirmado.
- **Contrato/evidência:** root `0.146.0` (`package.json:23-25`); ADR diz requerido; lockfile/provider Promptfoo resolve `0.144.6` (`pnpm-lock.yaml:6854-6955`). Reports não registram SDK efetivo.
- **Impacto/cenário/causa:** executor real difere da versão atribuída; dependency root pode ser redundante; transitive resolution ignorada.
- **Recomendação/arquivos:** alinhar/override/remover após compat check e registrar resolved-from-provider.
- **Aceitação/validação:** teste resolve package a partir de Promptfoo e compara report/doc; frozen install.
- **Ordem/residual/isolamento:** `WP-10`; requer authority para dependency update; isolável como decisão.

### TUX-AUD-023 — Python mínimo não é declarado

- **Severidade/confiança/categoria/status:** P2; alta; toolchain/onboarding; confirmado.
- **Contrato/evidência:** guia lista Node/UV/PNPM (`using-the-eval-harness.md:10-13`), mas `codex_auth.py:16` usa `tomllib` (Python 3.11+); sem pyproject/.python-version/preflight.
- **Impacto/cenário/causa:** `uv run python` pode resolver 3.10 e falhar; requisito ficou implícito no ambiente do autor.
- **Recomendação/arquivos:** declarar e preflight Python >=3.11 sem runtime dependency.
- **Aceitação/validação:** comando em 3.10 falha com mensagem antes de auth; supported version passa.
- **Ordem/residual/isolamento:** `WP-10`; UV resolver selection varia; isolável.

### TUX-AUD-024 — Ledger de migração/proveniência é ignorado e pessoal

- **Severidade/confiança/categoria/status:** P2; alta; provenance/maintainability; confirmado.
- **Contrato/evidência:** README afirma adaptação (`README.md:57-65`); evidence map cita migration map (`:31`); `.gitignore:16` oculta `docs/tmp/v0.1-map.md`, único ledger de 49 capabilities e paths pessoais.
- **Impacto/cenário/causa:** clone limpo perde disposição/inspiração/exclusão; artefato foi deliberadamente temporário e nunca promovido.
- **Recomendação/arquivos:** ledger sanitizado rastreado com source URL/commit/license/disposition/nature.
- **Aceitação/validação:** toda capability histórica tem disposição; zero personal path; link checker/provenance review.
- **Ordem/residual/isolamento:** `WP-11`; source history pode evoluir, por isso pin commit; isolável.

### TUX-AUD-025 — Grafo dev mantém advisories e licenças desconhecidas

- **Severidade/confiança/categoria/status:** P2; alta para inventário, média para exploitability; supply chain/license; risco fundamentado.
- **Contrato/evidência:** `pnpm audit` atual: 5 high/7 moderate/2 low; lockfile 792 dev; agregação encontrou 1 LGPL e 3 Unknown. Direct deps são dev-only (`package.json:23-25`).
- **Evidência externa:** GitHub Advisory Database URLs em `06-*`.
- **Impacto/cenário/causa:** maintainer eval processa network/output/optional packages; exploitability específica não foi provada; grafo Promptfoo amplo.
- **Recomendação/arquivos:** disposition por advisory, confirmar packages realmente carregados, licença Unknown, update/override somente com compat evidence.
- **Aceitação/validação:** zero high sem disposition/mitigation; effective graph e licenses registrados; validators/evals static continuam.
- **Ordem/residual/isolamento:** `WP-10`; provider run posterior para compat requer autoridade; isolável como análise, não necessariamente upgrade.

### TUX-AUD-026 — Nomes genéricos podem colidir cross-client

- **Severidade/confiança/categoria/status:** P2; média; routing/portability; risco fundamentado.
- **Contrato/evidência:** `docs`, `spec`, `verify`, `bugfix` em frontmatter; [Codex skills docs](https://developers.openai.com/codex/skills/) descrevem não-merge/precedência.
- **Impacto/cenário/causa:** package homônimo pode shadow/ser shadowed; nomes favoreceram UX local.
- **Recomendação/arquivos:** provar qualificação/namespace por cliente ou estratégia de nomes/install.
- **Aceitação/validação:** fixture com skill concorrente seleciona deterministicamente a intenção documentada.
- **Ordem/residual/isolamento:** `WP-09`; third-party catalogs mudam; depende da política de compatibilidade.

## P3 — Low

### TUX-AUD-027 — Evidence map não registra proveniência reproduzível dos PDFs

- **Severidade/confiança/categoria/status:** P3; alta; research/docs; confirmado.
- **Contrato/evidência:** `docs/research/evidence-map.md:3,39-43` tem título/ID, mas não URL/data/hash/páginas/método; `technical-research/SKILL.md:8-10` exige query/version/date/method/result/limitation.
- **Impacto/cenário/causa:** outro maintainer encontra preprint, mas não prova bytes/seção examinados; map resumiu bibliografia.
- **Recomendação/arquivos:** URLs diretas, versão/data, SHA-256, páginas/seções e método.
- **Aceitação/validação:** fresh download confere hash/version ou documenta drift; links válidos.
- **Ordem/residual/isolamento:** `WP-11`; arXiv versions podem mudar; isolável.

### TUX-AUD-028 — Cópias de templates não declaram fonte canônica

- **Severidade/confiança/categoria/status:** P3; média; maintainability; oportunidade.
- **Contrato/evidência:** sete pares root/skill byte-identical; test sincroniza, mas docs não dizem qual editar primeiro.
- **Impacto/cenário/causa:** alteração manual em duas superfícies; autocontenção exige duplicação, canonicalidade ficou tácita.
- **Recomendação/arquivos:** declarar source canônica e test/generation contract, preservando self-contained package.
- **Aceitação/validação:** uma fonte/fluxo documentado; drift test; pacote seletivo completo.
- **Ordem/residual/isolamento:** `WP-11`; geração adiciona tooling se exagerada; isolável.

### TUX-AUD-029 — `technical-research` não declara rede/fallback

- **Severidade/confiança/categoria/status:** P3; média; skill compatibility; oportunidade.
- **Contrato/evidência:** `technical-research/SKILL.md:8-14` exige claims atuais; `agents/openai.yaml:1-4` não declara compatibility/dependency.
- **Impacto/cenário/causa:** cliente offline ativa workflow impossível ou usa memória sem marcar; requisitos externos ficaram implícitos.
- **Recomendação/arquivos:** compatibility/network requirement, offline stop/fallback e evidence label.
- **Aceitação/validação:** cenário offline termina com limitação, sem claim atual inventado; online registra fontes.
- **Ordem/residual/isolamento:** `WP-09`; availability externa continua variável; isolável.

## Spec

Finding dominante: `TUX-AUD-001`. Antes de ajustar mecanismos, fixar intenção, ACs e força legítima dos claims. Correções não devem editar specs para acomodar o comportamento atual; staged candidate, fail-closed, cardinalidade e security oracles precisam ser decisões explícitas.

## Standards

Agent Skills estruturalmente conformes; plugin/skills passaram validators oficiais. Divergências normativas atuais concentram-se em operação: cwd/exit semantics de hooks, descoberta/precedência cross-client, UV project behavior, Promptfoo result contracts e supply-chain advisories. Fontes primárias estão registradas em `01-*` e `06-*`.

## Risk

Não há P0 identificado. O risco de distribuição é, porém, alto: gates centrais têm nomes/claims mais fortes que os fatos validados, e o sistema empírico pode emitir verde sem snapshot/coverage/oracle válidos. Até `WP-01`–`WP-08`, qualquer release deve tratar hooks e eval evidence como experimental/condicional, não como certificação.
