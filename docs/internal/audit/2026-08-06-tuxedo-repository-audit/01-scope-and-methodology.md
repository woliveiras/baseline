# 01 — Escopo e metodologia

## Escopo, autoridade e snapshot

A auditoria abrangeu o Tuxedo como produto distribuível único: contrato de engenharia, plugin, 17 skills, metadados Codex, hooks, Rules, policies, receipts, templates, documentação, testes, harness legado, Promptfoo, resultados sanitizados ignorados, toolchain, dependências, licença e proveniência.

Foi respeitada a autoridade de escrita limitada ao relatório. Nenhum arquivo preexistente foi editado; nenhum comando destrutivo, commit, branch, push, login ou model call foi executado. Instalações temporárias ocorreram somente fora do checkout: um interpretador isolado recebeu `PyYAML==6.0.2` para os validators oficiais, como previsto por `AGENTS.md:55-56`. Diretórios de estado do Promptfoo e probes também foram criados com `mktemp` fora do checkout.

O snapshot é:

- checkout absoluto: `<checkout-absoluto-do-tuxedo>` (valor local omitido por portabilidade);
- commit: `797d72cde47f7b94354af5ed49ede4eeb0ea5fdc`;
- branch: `main`;
- início: `2026-08-06T10:27:55+02:00`;
- estado local preexistente: três documentos de eval modificados, conforme o índice;
- data de consulta das fontes externas: 2026-08-06.

## Método em três fases

### Fase 1 — intenção sem implementação

Foram lidos integralmente `AGENTS.md`, `README.md`, `docs/README.md`, arquitetura, ADR, desenvolvimento, guia, research/evidence map, licença, manifest, contratos das 17 skills e templates de spec/review. A intenção foi reconstruída antes de usar hooks, testes ou eval runner como justificativa.

Resultado de fase: o contrato central exige uma cadeia durável, critérios estáveis, proveniência dos oráculos, fases de revisão isoladas, autoridade explícita para ações sensíveis e separação entre conteúdo portável, integração Codex e infraestrutura de mantenedor. O próprio catálogo, porém, não fornece uma spec/AC/matriz rastreada; isso foi registrado antes da leitura da implementação (`TUX-AUD-001`).

### Fase 2 — testes e evals sem a implementação como oráculo

Foram avaliados fixtures, assertions, tasks, rubricas, configurações, testes unitários, resultados sanitizados e documentação do desenho das evals. As famílias receberam a seguinte classificação:

| Família | Classificação | Justificativa |
| --- | --- | --- |
| Validators oficiais | `external` | Implementação oficial local do formato plugin/skill. |
| Testes de manifest/skills/templates | `spec-derived` + `implementation-aware` | Derivam de contratos, mas muitos espelham shape e igualdade atuais. |
| Testes dos hooks | `spec-derived` + `implementation-aware` | Cobrem invariantes declaradas; helper repete execução fora do cwd consumidor. |
| Routing Promptfoo | `spec-derived` + heurística `implementation-aware` | Expected skill vem do catálogo; `skill-used`/`skillCalls` é heurística do provider. |
| Behavior mecânico | `spec-derived` | AST, filesystem e exit status não dependem do texto final. |
| Behavior semântico | `spec-derived` + `diagnostic-probe` | Rubrica é declarada, mas o judge é da mesma família de modelo. |
| Security | `spec-derived` + `implementation-aware` + `diagnostic-probe` | Canary/trajectory e patch canônico medem probes específicos, não segurança geral. |
| Resultados ignorados | `external`/empírico histórico | São observações de provider; não provam o snapshot sem identidade completa. |

O ponto de mutation testing conceitual foi aplicado por contraexemplos seguros: staged index divergente, policy symlink quebrado, top-level futuro no `CODEX_HOME`, symlink aninhado, path `~/.ssh`, canary codificada e matriz de resultados incompleta.

### Fase 3 — confronto integrado

Somente após as fases anteriores foram confrontados skills, `agents/openai.yaml`, hooks, Rules, receipts, testes, runner legado, runner Promptfoo, lockfile e documentação. Cada divergência foi classificada como promessa sem mecanismo, mecanismo sem contrato, teste sem requisito, requisito sem oracle ou claim mais forte que a evidência.

## Inventário e amostragem explícita

Todos os 126 arquivos rastreados receberam disposição no [coverage ledger](02-inventory-and-coverage.md). Famílias homogêneas — YAML dos agentes, tasks JSON, configs Promptfoo, templates duplicados e lockfile — foram inventariadas mecanicamente e revisadas por schema, consistência e amostras representativas; isso está indicado por arquivo, sem amostragem silenciosa.

Os resultados ignorados foram tratados separadamente. No checkpoint independente havia 127 JSON válidos, 1.618.535 bytes, sem hash de conteúdo duplicado. Foram agregados por `suite/status/schema`, comparados aos hashes citados na documentação e amostrados por antiguidade, atualidade, suite, shard, aggregate e focused run. Uma execução `eval:full` externa e concorrente continuou criando relatórios depois desse checkpoint; os novos arquivos foram inventariados ao final, mas nenhum resultado dessa execução foi usado como comprovação auditiva.

## Ferramentas e versões

| Ferramenta | Versão observada |
| --- | --- |
| Git | `git version 2.50.1 (Apple Git-155)` |
| Node.js | `v26.3.1` |
| PNPM | `11.13.1` |
| UV | `0.9.5` |
| Python | `3.14.0` |
| zsh | `5.9` |
| bash | `5.3.9` |
| Codex CLI | `0.144.4` |
| Promptfoo | `0.122.0` |
| Poppler | instalação local usada para `pdfinfo`/`pdftotext` |

As versões acima são o ambiente efetivamente auditado, não requisitos mínimos inferidos. O repositório declara Node `>=22.22.0` (`package.json:7-9`) e não declara Python mínimo (`TUX-AUD-023`).

## Fontes externas primárias

Consultadas em 2026-08-06:

- [Agent Skills specification](https://agentskills.io/specification) — contrato de `SKILL.md`, metadata, referências e assets.
- [OpenAI — Build skills](https://developers.openai.com/codex/skills/) — descoberta, progressive disclosure e colisão de nomes.
- [OpenAI — Package plugins](https://developers.openai.com/plugins/build/plugins) — marketplace, instalação, manifest e restart.
- [OpenAI — Hooks](https://developers.openai.com/codex/hooks) — descoberta, cwd, `PLUGIN_ROOT`, timeouts e semântica de exit code.
- [OpenAI — Rules](https://developers.openai.com/codex/rules) — prefix matching e `codex execpolicy check`.
- [GitHub Copilot — Agent Skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills), [OpenCode — Skills](https://opencode.ai/docs/skills) e [Claude — Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — superfícies cross-client.
- [Promptfoo — Assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/) — shape e semântica das assertions.
- [UV — Running commands](https://docs.astral.sh/uv/concepts/projects/run/) — `uv run` sincroniza o ambiente do projeto no cwd, fundamento externo do probe `TUX-AUD-002`.
- [PNPM settings](https://pnpm.io/settings) e [GitHub Advisory Database](https://github.com/advisories) — supply chain.
- [SPDX MIT](https://spdx.org/licenses/MIT.html) — identificador e texto normativo da licença.
- PDFs primários do evidence map: [2604.01518](https://arxiv.org/pdf/2604.01518), [2607.05139](https://arxiv.org/pdf/2607.05139), [2602.07900](https://arxiv.org/pdf/2602.07900), [2602.20048](https://arxiv.org/pdf/2602.20048) e [2605.20049](https://arxiv.org/pdf/2605.20049).

## PDFs e limitação de contexto

Nenhum PDF anexado estava acessível no checkout, no diretório de visualizações ou como attachment local. Para não transformar ausência em omissão, os cinco IDs citados em `docs/research/evidence-map.md:9-13` foram baixados diretamente do arXiv para um diretório temporário externo, identificados com `pdfinfo` e extraídos com `pdftotext`. A auditoria verificou títulos, versões, contagem de páginas e o nexo geral dos claims, mas não trata essa reconstrução como prova de que os bytes são os mesmos PDFs originalmente “supplied”. Essa limitação motiva `TUX-AUD-027`.

## Limitações honestas

- Não houve execução real de provider, browser/network sandbox, auth, model judge, smoke, security ou red-team.
- O `eval:full` concorrente não foi iniciado, interrompido nem usado pela auditoria.
- Não houve auditoria jurídica; a análise de licença é de engenharia e recomenda revisão quando necessária.
- As 792 entradas dev do lockfile foram agregadas mecanicamente; não houve leitura jurídica manual de cada licença transitiva.
- A cobertura de ignored/generated é um inventário do estado observado, não uma garantia sobre arquivos criados depois do encerramento.
- A auditoria não prova comportamento cross-client; ela confronta layouts e contratos oficiais com a ausência de fixtures/execuções locais.
