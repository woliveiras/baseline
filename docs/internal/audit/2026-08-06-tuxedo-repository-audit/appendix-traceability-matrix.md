# Apêndice — Matriz de rastreabilidade

> Esta matriz preserva o snapshot original. A situação de cada divergência no `HEAD` `b46f37643adfa83897427cb2be3c7f383f3b35d9` está em [09 — Reconciliação](09-reconciliation-2026-08-06.md); nenhuma das 29 divergências atende atualmente seu critério de aceitação.

`—` significa ausência observada, não “fora de escopo”. Classificação segue o contrato Tuxedo.

| Contrato/expectativa | Teste/eval/oracle | Implementação | Evidência atual | Classificação | Divergência/finding |
| --- | --- | --- | --- | --- | --- |
| Produto é toolkit portátil, sem runtime | validators, structure tests | skills + manifest + hooks | validators passam | `external` + `spec-derived` | Hook UV é runtime no consumidor: `002`; operação cross-client: `011`. |
| 17 skills distribuídas | manifest/catalog tests | `skills/*` | 17 validators passam | `external` | Conforme. |
| `SKILL.md` conciso, refs um nível | official validators + link check | 17 packages | todos passam | `external` | Conforme; canonical copies `028`. |
| Deep work explicit-only | routing configs | `agents/openai.yaml` | configs validam | `spec-derived` | Premortem/research default implicit: `013`. |
| Autoridade não se expande | security/routing behavior | skill texts + AGENTS | behavior histórico | misto | Premortem standalone ambíguo: `015`; rules partial `020`. |
| Mudança material tem spec e ACs | template/tests de structure | templates, não artefato real | — | `implementation-aware` | Catálogo sem spec: `001`. |
| AC → oracle → test → evidence | receipt unit tests | global fail/passing receipt | fixture trivial passa | `implementation-aware` | Sem mapping AC: `010`. |
| Três review phases | hook receipt tests | review templates + guard | unit tests passam | `spec-derived` | test/code contexts incompletos: `018`. |
| Spec/matrix/evidence separados | hashes/path presence | guard roles | alias probe passa | `diagnostic-probe` | Roles podem aliasar: `017`. |
| Risk tier pelo maior boundary | template/skill guidance | spec template | default `small` | guidance | Viés de default: `016`. |
| Hook ausente de policy é no-op | hook fixture missing | `uv run` → guard | unit passa no cwd errado | `implementation-aware` | `.venv`/lock criados: `002`. |
| Malformed policy fail-closed | malformed JSON fixture | exists/load_object | JSON malformado bloqueia | `spec-derived` | symlink/type/OSError não: `004`. |
| Tree exact/stale detection | scope/stale tests | glob + hashes | unit passa | `spec-derived` | Default overlap impossível: `019`; races residual. |
| Commit gate protege slice verificada | direct commit test | working-tree hashes | unit passa | `implementation-aware` | Index staged não lido: `003`. |
| Rules protegem external/destructive commands | `codex execpolicy check` | prefix rules | sete casos passam | `external` | wrappers/options não cobertos: `020`. |
| Routing cobre catálogo | 34 Promptfoo cases | routing assertion | reports históricos | `spec-derived` + heuristic | Só Codex explícito; nomes/clients `011`,`026`. |
| Behavior cobre tasks configuradas | 40 target + judges | AST/workspace assertions | historical aggregates | `spec-derived` | 7/17 apenas; docs é honesta. |
| Security frozen probes detectam ataque nomeado | 12 probes | security/trajectory assertion | 12/12 histórico | diagnostic | falsos negativos `006`. |
| Dedicated home rejeita content desconhecido | unit configs/known paths | `codex_auth.py` | tests passam | `spec-derived` | unknown/nested symlink aceita: `007`. |
| API keys não são fallback | env filtering tests/current runner | Promptfoo env | static review | `spec-derived` | Legacy execute herda env: `009`. |
| Raw prompts/output não persistem | sanitized report builder | current runner | samples sanitized | `implementation-aware` | Legacy grava raw: `009`; shape só suffix `021`. |
| Full cobre 34/40/12 | config range tests | aggregate sums rows | docs count confere | `spec-derived` | missing/duplicate passa: `008`. |
| Evidence corresponde ao snapshot | report fingerprint | AGENTS+skills hash | same hash across harness changes | `implementation-aware` | identidade incompleta: `005`. |
| Fresh evidence após upgrades | docs policy | manual evidence log | full verde pre-change | external historical | `005`. |
| Failed shard persiste checkpoint | runner unit/static review | sanitized checkpoint | result families presentes | `implementation-aware` | Conforme no caminho atual. |
| Git unchanged após full | before/after status | runner | históricos declaram | `diagnostic-probe` | Não identifica untracked/ignored evidence como product change por design. |
| Toolchain declarada | docs + version commands | package/UV imports | current env passa | external | Python mínimo ausente `023`; SDK mismatch `022`. |
| Dependências dev-only não distribuídas | grep/package manifest | package.json/lockfile | confirmado | `external` | advisories/licenças `025`. |
| MIT/proveniência clara | license text/manifest/readme | LICENSE | consistente | external/SPDX | Ledger ignorado `024`; paper metadata `027`. |
| Onboarding README suficiente | link/manual walk-through | README | não reproduzível | diagnostic | `012`. |
| Templates representam common/blocked/authorized | hook tests + manual scenarios | policy/receipts/reviews | normal/stale cobertos | `spec-derived` | co-location/context/alias gaps `017`–`019`. |
| Composição de skills termina | — | referências cruzadas informais | — | — | lifecycle/deadlock `014`. |
| Research atual é reproduzível | evidence map bibliography | technical-research skill | PDFs reconstruídos | external + diagnostic | metadata/method `027`; offline compatibility `029`. |

## Gaps em ambas as direções

### Promessa sem implementação suficiente

- “Commit gate” sem staged index.
- “Fail-closed” sem unknown surfaces, symlinks e filesystem errors.
- “34/40/12” sem expected-row set.
- “Steganographic exfiltration” com busca literal.
- “Portável” sem instalação/behavior cross-client.

### Implementação sem contrato canônico

- Algoritmos específicos de receipt/digest/glob não têm AC versionada.
- Sanitized report schema e aggregate shape não têm schema formal.
- Allowlist corrente do eval home não tem matriz de surfaces/version compatibility.
- Defaults de policy e Rules não têm cenário de suporte declarado.

### Teste sem requisito independente

- Igualdade byte a byte de templates preserva estado atual, mas não escolhe fonte canônica.
- Helpers de digest/receipt repetem implementação sem oracle independente.
- Range tests das shards não exigem que raw rows materializem o range.

### Requisito sem teste

- Staged commit candidate.
- Cwd real do hook/zero filesystem side effect.
- Unknown eval-home top-level/nested symlink.
- AC-by-AC receipt mapping.
- Composition state machine e fallback.
- Cross-client discovery/collision.
