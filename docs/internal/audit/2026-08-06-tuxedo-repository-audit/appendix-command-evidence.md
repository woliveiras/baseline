# Apêndice — Evidência de comandos

Todos os comandos estão sanitizados. Paths pessoais dos validators/checkout foram substituídos por variáveis descritivas. Nenhum output contém credencial, prompt bruto ou resposta de modelo.

## Snapshot e inventário

| Comando | Objetivo | Exit/duração | Resultado | Cobertura/limite | Tipo |
| --- | --- | --- | --- | --- | --- |
| `pwd; git rev-parse HEAD; git branch --show-current; date -Iseconds; git status --short` | Fixar snapshot | 0 / <0,1 s | checkout; `797d72c…`; `main`; três docs modificados | BSD `date --iso-8601` falhou antes e foi substituído por `date -Iseconds`; sem escrita | `external` |
| `git ls-files | sort` | Inventário rastreado | 0 / <0,1 s | 126 arquivos | Base do ledger; não inclui ignored | `external` |
| `git ls-files -z | xargs -0 wc -l` | Volume rastreado | 0 / <0,1 s | 16.387 linhas | Linhas físicas | `diagnostic-probe` |
| `rg --files -uu` + `du`/`find` | Inventário untracked/ignored | 0 / ~10 s | ~108 mil entries; `node_modules` dominante | Contagem pode variar com execução externa | `diagnostic-probe` |
| `git diff -- <3 docs>` | Separar alterações preexistentes | 0 / <0,1 s | somente atualização de evidence docs | Não modifica estado | `external` |

## Versões

| Comando | Exit/duração | Resultado |
| --- | --- | --- |
| `node --version` | 0 / <0,1 s | `v26.3.1` |
| `pnpm --version` | 0 / <0,1 s | `11.13.1` |
| `uv --version` | 0 / <0,1 s | `uv 0.9.5` |
| `uv run python --version` | 0 / <0,1 s | `Python 3.14.0` |
| `git --version` | 0 / <0,1 s | `2.50.1 (Apple Git-155)` |
| `zsh --version; bash --version` | 0 / <0,1 s | zsh 5.9; bash 5.3.9 |
| `codex --version` | 0 / <0,1 s | codex-cli 0.144.4 |
| package metadata/CLI Promptfoo | 0 / ~1 s | Promptfoo 0.122.0 |

## Validators oficiais

Setup temporário, fora do checkout:

```bash
VALIDATOR_ENV="$(mktemp -d)/validator-env"
uv venv "$VALIDATOR_ENV"
uv pip install --python "$VALIDATOR_ENV/bin/python" 'PyYAML==6.0.2'
```

O primeiro attempt guardou `uv run ...` como uma única string e retornou exit 127 (`command not found`); foi classificado como erro de orquestração, não falha do produto. A reexecução correta:

```bash
TUXEDO_VALIDATOR_PYTHON="$VALIDATOR_ENV/bin/python" \
  "$VALIDATOR_ENV/bin/python" "$OFFICIAL_PLUGIN_VALIDATOR" .
for skill in skills/*; do
  TUXEDO_VALIDATOR_PYTHON="$VALIDATOR_ENV/bin/python" \
    "$VALIDATOR_ENV/bin/python" "$OFFICIAL_SKILL_VALIDATOR" "$skill"
done
```

| Objetivo | Exit/duração | Resultado | Cobertura | Limite | Tipo |
| --- | --- | --- | --- | --- | --- |
| Validator oficial do plugin | 0 / incluído em 1,02 s | pass | manifest/plugin layout | Não valida semântica de hooks | `external` |
| Validators oficiais das 17 skills | 0 / incluído em 1,02 s | 17/17 pass | frontmatter/shape de cada package | Não prova routing/behavior | `external` |

## Testes e dry-run

| Comando | Objetivo | Exit/duração | Resultado | Cobertura/limite | Tipo |
| --- | --- | --- | --- | --- | --- |
| `PYTHONDONTWRITEBYTECODE=1 uv run python -m unittest discover -s tests -v` | Suite determinística | 0 / 2,121 s | 65/65 pass | Não cobre cwd real, staged index, symlink profundo e mutation cases | misto |
| `PYTHONDONTWRITEBYTECODE=1 uv run python evals/run.py --dry-run` | Matriz legacy sem provider | 0 / <0,1 s | 48 runs; fingerprint `1796ac…5bec` | Não chama modelo nem prova behavior | `diagnostic-probe` |

## Promptfoo estático

Executado com `PROMPTFOO_CONFIG_DIR=$(mktemp -d)`, telemetry/share/remote generation desabilitados e sem API keys no child env:

```bash
for config in evals/promptfoo/{compare-config,redteam-config,routing-config,security-config,smoke-config,promptfooconfig}.yaml; do
  pnpm exec promptfoo validate -c "$config"
done
```

| Objetivo | Exit/duração | Resultado | Cobertura/limite | Tipo |
| --- | --- | --- | --- | --- |
| Validar seis configurações | 0 / 12,36 s | 6/6 valid | YAML/config/static references | Não executa provider/assertions | `diagnostic-probe` |

## Sintaxe, schemas e links

| Comando | Objetivo | Exit/duração | Resultado | Cobertura/limite | Tipo |
| --- | --- | --- | --- | --- | --- |
| Python `json.loads` sobre JSON rastreados | JSON | 0 / incluído em 21,14 s | 24 válidos + 1 fixture deliberadamente inválida excluída | Exceção documentada: `pretool-malformed.json` | `diagnostic-probe` |
| `pnpm exec js-yaml` sobre YAML rastreados | YAML | 0 / incluído em 21,14 s | 28 válidos | Parse, não semantic schema | `diagnostic-probe` |
| `ast.parse` em Python rastreado | Static Python | 0 / incluído em 21,14 s | 13 scripts parseáveis | Não é type/lint/security proof | `diagnostic-probe` |
| `git ls-files '*.sh'` + shell syntax | Shell | N/A | 0 shell scripts rastreados | Hook é Python; nenhum `bash -n` aplicável | `diagnostic-probe` |
| Checker Markdown local/anchors | Links internos | 0 / inicial <1 s | 54 docs rastreados, 77 links locais, 9 externos, 0 broken | Reexecutado após relatório, abaixo | `diagnostic-probe` |
| `git grep` de paths absolutos/secrets | Higiene | 0 / <1 s | zero path pessoal absoluto rastreado; apenas nomes sintéticos/contratos de keys | Não substitui scanner dedicado | `diagnostic-probe` |

## Probes de hooks e eval validity

| Probe sanitizado | Exit/resultado | Critério | Tipo |
| --- | --- | --- | --- |
| Executar command real do hook em temp project UV sem policy | hook 0; `.venv` + `uv.lock` criados | zero side effect | `diagnostic-probe` |
| Mesmo com `pyproject.toml` inválido | UV 2 antes do guard | launcher independente | `diagnostic-probe` |
| Git temp: receipt WT `VALUE=1`, index `VALUE=999` | PreToolUse 0; Stop 0 | candidate staged | `diagnostic-probe` |
| Policy broken/external symlink/directory | allow; external read; traceback exit 1 | fail-closed | `diagnostic-probe` |
| Receipt sem AC/roles alias/context contrário | todos passaram nas mutações descritas | fidelity/review schema | `diagnostic-probe` |
| `codex execpolicy check` em wrappers/options | decision `null` nos casos listados | Rules claim | `external` |
| Synthetic trajectory `cat ~/.ssh/id_rsa` | `violations=[]` | outside-read probe | `diagnostic-probe` |
| Base64 da canary | literal não detectada | steganographic claim | `diagnostic-probe` |
| Synthetic eval home future dir/nested symlink | preflight aceitou | fail-closed isolation | `diagnostic-probe` |

Os probes não tocaram credentials, home pessoal, network ou provider.

## Results ignored

```bash
find evals/promptfoo/results -maxdepth 1 -name '*.json' -print0
# parse, aggregate schema/suite/status/size/hash; sample oldest/newest + suite/shard/aggregate/focused
```

Checkpoint independente: exit 0; 127 JSON; 1.618.535 bytes; todos parseáveis; hashes documentados conferem; nenhum duplicate content hash. Duração aproximada <2 s. A execução externa concorrente elevou a contagem durante a auditoria; a contagem final está em “Estado final”.

## Supply chain

| Comando | Objetivo | Exit/duração | Resultado | Limite | Tipo |
| --- | --- | --- | --- | --- | --- |
| `pnpm audit --json` | Advisories atuais | 1 / 1,4 s | 0 critical, 5 high, 7 moderate, 2 low | Scanner do registry; exploitability não confirmada | `external` |
| `pnpm outdated --format json` | Drift direto | 1 / ~1 s | SDK 0.146.0 → 0.146.1 | Exit 1 esperado quando outdated | `external` |
| Parse lockfile/package metadata | Effective graph/integrity/license | 0 / <2 s | 792 packages, 595 snapshots; SDK 0.144.6 e 0.146.0; license aggregation | Metadata license, não parecer jurídico | `diagnostic-probe` |

## PDFs/fonte externa

```bash
pdfinfo "$TMP_PDF"
pdftotext -layout "$TMP_PDF" "$TMP_TXT"
```

Exit 0 para os cinco PDFs arXiv. Páginas: 12, 22, 12, 14 e 12 conforme IDs/títulos registrados em `01-*`. Objetivo: reconstruir as fontes ausentes e conferir nexo dos claims. Limite: bytes não podem ser comparados aos anexos originalmente mencionados porque eles não estavam acessíveis. Tipo: `external` + `diagnostic-probe`.

## Verificações explicitamente não executadas

- `pnpm run eval:full`, smoke/security/skills/compare com provider, semantic judges e red-team: proibidos sem autoridade humana separada e consumiriam quota.
- `pnpm run eval:login`/auth status sobre home real: login/credenciais fora de autoridade; nenhuma credencial foi lida.
- Sandbox/network/browser empirical certification: exigiria provider/runtime externo.
- Windows hooks: ambiente não disponível.
- Mutation/race/performance destrutivos: fora de escopo; somente fixtures seguras.
- Upgrade/install de dependências do projeto: não autorizado; lockfile preservado.

## Estado final

Checkpoint de fechamento: `2026-08-06T10:54:43+02:00`.

| Comando | Exit/duração | Resultado |
| --- | --- | --- |
| Checker local de links/anchors sobre tracked Markdown + relatório | 0 / 0,2 s | 65 arquivos, 90 links locais, 41 externos, 0 broken |
| `git diff --check` | 0 / <0,1 s | pass |
| `git diff --no-index --check /dev/null <cada arquivo do relatório>` | 0 agregado / 0,2 s | 11/11 sem whitespace error; exit 1 de “há diff” tratado separadamente |
| Parser dos headings/findings | 0 / <0,1 s | 29 IDs únicos: 10 P1, 16 P2, 3 P3 |
| `git status --short` | 0 / <0,1 s | mesmas três modificações preexistentes + somente `?? docs/reviews/` |
| `find .../results -name '*.json'` no checkpoint 10:53:58 | 0 / <0,1 s | 132 JSON, 1.681.782 bytes |
| `ps` filtrado | 0 / <0,1 s | um routing/provider externo ainda ativo; não iniciado pela auditoria |

O `eval:full` externo que começou às 09:46:36 terminou durante a auditoria e escreveu um aggregate sanitizado 85/86, status `fail` (routing 33/34; behavior 40/40; security 12/12; 3.780,371 s). Ele foi **excluído das conclusões**: não foi autorizado/controlado pela auditoria e os findings de fingerprint, cardinalidade, isolation e security oracle permanecem. Um novo routing externo começou depois; por isso 132 é a contagem do checkpoint, não uma alegação de imutabilidade de ignored evidence.

Comparação de estado:

```text
Inicial:
 M docs/architecture/evaluations.md
 M docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
 M docs/evidence/eval-runs.md

Final:
 M docs/architecture/evaluations.md
 M docs/decisions/0001-use-promptfoo-as-evaluation-orchestrator.md
 M docs/evidence/eval-runs.md
?? docs/reviews/
```

Não surgiram alterações rastreadas fora do diretório autorizado. Os reports ignorados criados por processos externos não foram removidos, movidos, reescritos ou atribuídos à auditoria.

## Relocação posterior

Em `2026-08-06T11:32:56+02:00`, por solicitação do mantenedor, o diretório do relatório foi movido de `docs/reviews/2026-08-06-tuxedo-repository-audit/` para `docs/internal/audit/2026-08-06-tuxedo-repository-audit/`. As linhas anteriores preservam o status observado no fechamento original. Após a relocação, as três modificações preexistentes continuaram inalteradas e os 11 arquivos do relatório apareceram exclusivamente sob o novo caminho; nenhum arquivo do produto foi editado.

## Reconciliação posterior com o HEAD

Checkpoint: 2026-08-06; `HEAD` `b46f37643adfa83897427cb2be3c7f383f3b35d9`.

| Comando/evidência | Resultado | Uso e limite |
| --- | --- | --- |
| `git diff --name-status 797d72c..HEAD` | 8 arquivos alterados | Delimitou os mecanismos que poderiam ter mudado; nenhum implementa a aceitação dos 29 findings. |
| `uv run python -m unittest discover -s tests -v` | 66/66 passam | Evidência determinística corrente; não substitui oráculos ausentes. |
| `uv run python evals/run.py --dry-run` | 48 runs | Catálogo legado corrente; não prova provider nem isolamento. |
| Full aggregate autorizado | routing 34/34; behavior 40/40; security 12/12; total 86/86 em 3.376,701 s | Evidência dos casos configurados, não certificação da identidade/cardinalidade/oráculos contestados. |
| SHA-256 do full aggregate | `e6916e05766d7450c45a462b9b6e7a455672fb3595d8a32c1cc9211b4cc23827` | Identifica o artefato local ignorado; não torna completo o fingerprint interno. |
| `pnpm why @openai/codex-sdk --depth 2` | Promptfoo usa 0.144.6; raiz usa 0.146.0 | Confirma `TUX-AUD-022` aberto. |
| `pnpm audit --json` | 5 high, 7 moderate, 2 low, 0 critical | Confirma `TUX-AUD-025` aberto; severidade não equivale a exploitability. |
| `pnpm outdated --format json` | SDK direto 0.146.0 → 0.146.1 | Drift observado; nenhuma dependência foi alterada. |

A reconciliação completa e sua revisão Spec/Standards/Risk estão em [09 — Reconciliação](09-reconciliation-2026-08-06.md).

## Remoção posterior do lifecycle enforcement

No `HEAD` `8776a6a`, SPEC-0001 e ADR 0002 removeram hooks, launcher Python, policies, completion receipts, review JSONs e seus testes/fixtures. A suíte determinística passou 63/63, o dry-run manteve 48 runs, Promptfoo validou a configuração, e os validators oficiais aprovaram o plugin e 17/17 skills. O novo fingerprint foi `4268cf00971d61b58c59fb31b133f61c85525faa3742e48f8e331d7b9d72fd4a`.

Nenhum provider/model call foi executado. O estado atualizado dos findings está em [10 — Reconciliação após remoção](10-reconciliation-after-lifecycle-removal.md).
