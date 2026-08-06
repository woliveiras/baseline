# 03 — Produto, arquitetura e contratos

## Produto e escopo

### Fato observado

`README.md:3-20` e `docs/development.md:7-11` apresentam o Tuxedo como toolkit portátil, spec-driven, orientado a agentes e composto pelo repositório, sem CLI, daemon, package manager, sync, telemetry, generator ou runtime dependency. O manifest (`.codex-plugin/plugin.json:1-12`) distribui o plugin; `skills/` contém o core portável; `agents/openai.yaml`, `hooks/` e `templates/codex/` isolam comportamento Codex; `evals/`, testes e dependências são de mantenedor.

### Interpretação

O modelo mental é forte: conteúdo declarativo instalado, integração opcional por cliente e infraestrutura de validação fora do artefato consumido. Não foi encontrada maquinaria acidental de CLI/runtime na superfície distribuída. Promptfoo e Codex SDK aparecem apenas em dev tooling.

### Limite

“Portátil” é verdadeiro no sentido de formato e neutralidade textual; não está comprovado no sentido de instalação, descoberta, routing e composição nos clientes alegados (`TUX-AUD-011`). “Sem runtime dependency” é verdadeiro para o conteúdo das skills, mas falso para a operação atual dos hooks porque o launcher usa UV no projeto consumidor (`TUX-AUD-002`).

## Arquitetura atual

```mermaid
flowchart TB
    U["Usuário ou mantenedor"]
    P["Plugin Codex: manifest"]
    C["Core portável: 17 skills + references/assets"]
    O["Adapter Codex: agents/openai.yaml"]
    H["Lifecycle Codex: hooks + Rules opt-in"]
    T["Templates de spec/policy/review"]
    M["Manutenção: tests + evals + docs"]
    D["Promptfoo e Codex SDK, dev-only"]

    U --> P
    P --> C
    P --> O
    P --> H
    U --> T
    M --> C
    M --> O
    M --> H
    M --> T
    M --> D
```

### Boundaries confirmados

- O core das skills não referencia Promptfoo/Codex SDK.
- Integração OpenAI está em `agents/openai.yaml`; lifecycle está em `hooks/`.
- Rules e policy são templates de adoção, não mutações automáticas do projeto.
- `evals/` e `node_modules/` não fazem parte do conteúdo instalado.
- Assets necessários a `spec` e `verify` são autocontidos no pacote da skill.

### Acoplamentos problemáticos

- `hooks/hooks.json` acopla o lifecycle a UV e, por cwd, ao projeto consumidor.
- O receipt acopla implementação, testes, docs e reviews por hashes, mas não ao índice Git nem a IDs de critérios.
- O fingerprint de eval acopla identidade apenas a `AGENTS.md + skills/**`, enquanto o verdict depende também de tasks, fixtures, configs, assertions, runner, provider e lockfile.
- A mesma behavior matrix tem ownership simultâneo em `spec` e `verify`, sem state machine de transição.

## Cadeia de fidelidade declarada e real

```mermaid
flowchart LR
    S["Spec + AC IDs"] --> B["Behavior/oracle matrix"]
    B --> T["Tests/evals"]
    T --> I["Implementation"]
    I --> E["Evidence"]
    E --> R["3-phase review"]
    R --> G["Gate/commit"]

    X["Estado real do catálogo"] -.-> S
    X --> K["SKILL.md é intenção e implementação"]
    G -. "working tree, não staged index" .-> Z["Bytes do commit"]
```

`AGENTS.md:7-17` exige a sequência, IDs estáveis, classificação de evidência e três fases. Os templates representam o formato. Porém, `git ls-files` não contém spec ou AC real do catálogo, behavior matrix do produto, evidence artifact ou review receipt. A implementação (o texto da skill) é também a principal fonte de intenção. Isso impede reconstruir fase 1 sem contaminação e constitui `TUX-AUD-001`.

## Fluxo de enforcement

```mermaid
sequenceDiagram
    participant C as Codex session
    participant U as UV launcher
    participant G as guard.py
    participant P as .tuxedo/policy.json
    participant R as receipts/reviews/files
    participant I as Git index

    C->>U: PreToolUse ou Stop no cwd do projeto
    U->>U: Descobre/sincroniza projeto UV
    U->>G: python guard.py mode
    G->>P: exists + parse
    alt policy ausente
        G-->>C: allow
    else trigger requerido
        G->>R: resolve, glob, hash, digest
        G-->>C: allow ou JSON deny
    end
    Note over G,I: O índice staged não é lido
```

O guard usa apenas stdlib, canonical JSON e SHA-256; bloqueia traversal de artifacts e detecta hashes stale. Esses são pontos fortes reais. A força documental excede o mecanismo em quatro pontos: UV roda antes do guard; policy symlinks/tipos inesperados não falham pelo protocolo correto; roles podem aliasar; e o commit candidate não é o staged snapshot.

## Fluxo das evals

```mermaid
flowchart TD
    A["Autoridade humana explícita"] --> P["Preflight dedicated CODEX_HOME"]
    P --> V["Validators + static config + fixtures"]
    V --> R["Routing: 34"]
    V --> B["Behavior: 40 + até 25 judges"]
    V --> S["Security: 12"]
    R --> AR["Sanitized shard/aggregate"]
    B --> AB["Sanitized shard/aggregate"]
    S --> AS["Sanitized report"]
    AR --> F["Full aggregate"]
    AB --> F
    AS --> F
    F --> C{"status pass?"}
    C -->|sim| G["git status unchanged"]
    C -->|não| X["failure"]

    Q["Gaps"] -.-> P
    Q -. "unknown top-level + nested symlink" .-> P
    Q -. "no exact row matrix" .-> F
    Q -. "fingerprint omits harness" .-> AR
```

O desenho de isolamento, state temporário, checkpointing após exit 100, reports sanitizados e continuação de suites após assertion failure é sólido. Os findings `TUX-AUD-005` a `TUX-AUD-009` mostram que identidade, isolamento, cobertura e o caminho legado ainda não satisfazem o contrato.

## Enforcement determinístico versus julgamento

| Claim | Mecanismo real | Força legítima |
| --- | --- | --- |
| Artifact não mudou | SHA-256 sobre arquivo da working tree | Forte para bytes lidos naquele instante. |
| Tree está completa | glob + comparação exata de paths/hashes | Forte para policy e cwd atuais; sensível a overlap/symlink/race. |
| Critérios estão cobertos | Um par global fail-first/passing | Insuficiente; não há AC IDs. |
| Revisões foram independentes | Booleans declarados + hashes | Declaração de contexto, não independência real; validação incompleta. |
| Commit contém bytes revisados | Nenhuma leitura do índice | Não garantido. |
| Skill foi usada | metadata/`skill-used` | Heurística do provider. |
| Patch atende oracle | AST/filesystem checks | Forte para o fixture específico. |
| Segurança foi preservada | Frozen probes + canary/trajectory | Diagnóstico limitado; falsos negativos confirmados. |
| Full cobriu 86 trials | Soma de rows presentes | Não garantido sem matriz/cardinalidade. |

## Arquitetura recomendada

```mermaid
flowchart TB
    S["Canonical catalog spec + ACs"] --> M["Versioned oracle matrix"]
    M --> DT["Deterministic tests"]
    M --> EV["Behavior/security eval contracts"]
    DT --> IM["Skills, hooks, templates"]
    EV --> IM
    IM --> E["Evidence bound to full snapshot"]
    E --> RV["Independent phase receipts"]
    RV --> CI["Candidate snapshot abstraction"]
    CI --> WT["Stop gate: working tree"]
    CI --> IDX["Commit gate: staged Git tree"]

    AD["Client adapters"] --> CX["Codex"]
    AD --> CC["Claude/Copilot/OpenCode fixtures"]
    IM --> AD

    ISO["Self-contained hook launcher"] --> IM
    ISO -. "no project discovery or sync" .-> CX
```

Mudanças essenciais:

1. tornar spec/matriz do catálogo canônicas e versionadas;
2. separar `candidate snapshot` de working tree e staged index;
3. executar hooks em runtime autocontido/isolado do projeto consumidor;
4. tornar policy parsing fail-closed por protocolo;
5. dar identidade versionada a todas as entradas/oráculos das evals;
6. validar conjunto exato de rows e reduzir claims dos probes ao que o oracle detecta;
7. definir state machine de composição das skills e adapters/install fixtures por cliente.

## Sustentabilidade e reversibilidade

A base é pequena e reversível: skills são arquivos, hooks são opt-in e o toolchain é dev-only. Os maiores custos futuros vêm de duplicações manuais e da ausência de ownership explícito, não de volume de código. Os work packages mantêm correções independentes: hook launcher, staged binding, policy parsing e eval validity podem avançar paralelamente depois que o contrato canônico define os fatos que cada mecanismo deve provar.
