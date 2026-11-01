# AI HUB Protocol v0.4

Especificação mínima para que qualquer IA, de qualquer fornecedor, continue o trabalho de outra num projeto, usando só arquivos de texto e Git.

Status: MVP. Escopo congelado em 01/11/2026 pelo Product Owner.

## 1. Princípios

1. O conhecimento pertence ao projeto, não ao fornecedor da IA.
2. Tudo é texto: Markdown com metadados YAML no topo. Qualquer modelo que leia texto colado consegue participar.
3. A IA propõe; o humano aprova. Mudança oficial é um commit ou merge aprovado no Git.
4. O Git é o único sistema de versão e de histórico.
5. Nenhuma IA presume acesso a arquivos ou conversas de outra. O compartilhamento acontece pelos arquivos deste protocolo.

## 2. Estrutura de um projeto

Cada projeto é um repositório Git independente:

```
<projeto>/
├── PROJECT.md      contexto, objetivos, regras e metadados
├── DECISIONS.md    decisões e seu histórico
└── tasks/
    ├── TASK-001.md uma tarefa: metadados, objetivo, estado e handoff
    └── TASK-002.md
```

Outros arquivos (código, roteiros, pesquisas, referências) podem existir no repositório. O protocolo só regula estes três tipos.

## 3. PROJECT.md

Metadados obrigatórios:

| Campo | Valores |
| --- | --- |
| `id` | minúsculas, números e hífens (ex.: `teaser-lancamento`) |
| `name` | texto livre |
| `type` | `software` · `business` · `research` · `marketing` · `education` · `creative` · `personal` · `other` |
| `owner` | quem aprova commits e decisões |
| `status` | `active` · `paused` · `done` |
| `protocol` | `ai-hub v0.4` |

Opcionais: `sensitivity` (`normal` · `high`), `language`, `reviewed_at`.

O corpo deve conter a seção `## Regras para qualquer IA` (copiada do template) e o contexto essencial do projeto. Recomendação: o arquivo inteiro com até cerca de 3 mil tokens.

## 4. DECISIONS.md

Cada decisão é uma seção:

```markdown
## D-001: Título
- **Status:** accepted
- **Data:** 2026-11-01
- **Aprovado por:** Nome
- **Decisão:** ...
- **Motivo:** ...
- **Substitui:** —
```

Regras:

- IDs no formato `D-NNN`, únicos e em ordem crescente.
- Status: `proposed` · `accepted` · `superseded`. Só o humano marca `accepted`.
- Nunca apagar. Para revogar: a decisão nova indica `Substitui: D-00X`, e a antiga passa a `superseded`.

## 5. TASK-NNN.md

Metadados obrigatórios:

| Campo | Valores |
| --- | --- |
| `id` | `TASK-NNN`, igual ao nome do arquivo |
| `project` | igual ao `id` do PROJECT.md |
| `title` | texto livre |
| `status` | ver seção 6 |
| `owner` | quem responde pela tarefa |
| `created` / `updated` | data `AAAA-MM-DD`; `updated` não pode ser anterior a `created` |
| `last_agent` | quem trabalhou por último (`human`, `claude`, `gpt`, `gemini`...); obrigatório fora de `todo` |

Opcional: `last_model` (nome e versão exatos do modelo).

Seções do corpo, nesta ordem: Objetivo · Critério de pronto · Leitura obrigatória · Estado atual · Handoff · Propostas de decisão · Log de sessões.

- **Estado atual** é reescrito a cada sessão: descreve onde o trabalho está agora.
- **Log de sessões** ganha uma linha por sessão, a mais recente no topo.

## 6. Estados

| Estado | Significado |
| --- | --- |
| `todo` | ainda não começou |
| `doing` | em andamento |
| `review` | pronta para o humano revisar e aprovar |
| `done` | aprovada; ou cancelada, com o motivo no Estado atual |
| `blocked` | parada; o motivo precisa estar em Bloqueios atuais |

## 7. Handoff

Toda IA, ao encerrar uma sessão, preenche a seção `## Handoff` com estes três itens obrigatórios:

1. **Arquivos alterados:** caminhos, ou `nenhum`.
2. **Bloqueios atuais:** o que impede o avanço, ou `nenhum`.
3. **Próximos 3 passos:** três ações exatas e numeradas para a próxima IA.

Item recomendado (gera aviso se faltar, não erro):

4. **Validação:** o que foi verificado e como, ou `não verificado`.

O handoff descreve o estado real do trabalho, não um resumo da conversa.

## 8. Fluxo de uma sessão

1. A IA recebe `PROJECT.md`, `DECISIONS.md` e o `TASK-NNN.md` da tarefa.
2. Trabalha seguindo as regras do `PROJECT.md`.
3. Atualiza o `TASK-NNN.md` (metadados, Estado atual, Handoff, Log).
4. Devolve cada arquivo alterado completo, num bloco de código com o caminho na primeira linha.
5. O humano revisa, roda o validador e faz o commit.

## 9. Critério de sucesso do MVP

Uma tarefa iniciada por uma IA é continuada corretamente por outra, de outro fornecedor, recebendo apenas os arquivos do protocolo.

**Teste de retomada:** antes de trabalhar, a nova IA responde, só com os arquivos, a cinco perguntas:

1. Qual é o objetivo da tarefa?
2. Qual é a decisão aceita mais recente que afeta a tarefa?
3. Qual é o próximo passo?
4. O que está bloqueado?
5. Qual arquivo foi alterado por último?

Meta: 5 de 5 sem perguntas ao humano.

## 10. Fora do escopo da v0.4

Permissões em arquivo, agentes especializados, registro de custos, MCP, interfaces, RAG e automações. Entram só com necessidade comprovada.
