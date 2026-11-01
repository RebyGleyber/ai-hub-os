# AI HUB OS

Um protocolo simples para que qualquer IA (Claude, ChatGPT, Gemini, Grok ou outra) continue o trabalho de outra, em qualquer tipo de projeto, usando só arquivos de texto e Git.

- Especificação: [`SPEC.md`](SPEC.md) (AI HUB Protocol v0.4)
- Templates: [`templates/`](templates)
- Exemplos preenchidos: [`examples/`](examples) (software, criativo e pesquisa; marcas fictícias)
- Validador: [`hub_validate.py`](hub_validate.py)

## Instalação

Requer Python 3.10 ou superior.

```bash
pip install -r requirements.txt
python hub_validate.py examples/*
```

Saída esperada: `Resultado: 0 erro(s), 0 aviso(s)`.

Para rodar os testes automatizados:

```bash
pip install pytest
python -m pytest
```

---

## 1. Como criar um projeto

1. Crie um repositório Git novo, um por projeto.
2. Copie para ele o conteúdo de `templates/`: `PROJECT.md`, `DECISIONS.md` e `tasks/TASK-001.md`.
3. No `PROJECT.md`, preencha os metadados (`id`, `name`, `type`, `owner`, `status`) e as seções Objetivo e Contexto essencial. Mantenha a seção "Regras para qualquer IA" como está.
4. Em `DECISIONS.md`, registre as decisões que já existem, ou apague a D-001 de exemplo.
5. Rode `python hub_validate.py caminho/do/projeto` e faça o primeiro commit.

## 2. Como abrir uma tarefa

1. Copie `tasks/TASK-001.md` para o próximo número livre, por exemplo `tasks/TASK-002.md`.
2. Ajuste `id` (igual ao nome do arquivo), `title`, `created` e `updated`.
3. Escreva o Objetivo e o Critério de pronto com itens verificáveis.
4. Deixe `status: todo`, `last_agent: human` e o handoff em branco.

## 3. Como trocar de IA

**Jeito rápido:** gere o pacote da tarefa e cole o conteúdo inteiro na IA. Ele já traz as instruções abaixo e todos os arquivos necessários, para IAs que não conseguem abrir links do GitHub.

```bash
python hub_pack.py caminho/do/projeto TASK-002 -o pacote.md
```

**Jeito manual:** cole na IA escolhida os três arquivos (`PROJECT.md`, `DECISIONS.md` e a tarefa) e esta mensagem:

```text
Você vai continuar a tarefa TASK-NNN seguindo as regras do PROJECT.md.
Antes de trabalhar, responda só com os arquivos:
1. Qual é o objetivo da tarefa?
2. Qual é a decisão aceita mais recente que afeta a tarefa?
3. Qual é o próximo passo?
4. O que está bloqueado?
5. Quais arquivos a última sessão desta tarefa alterou? (tarefa ainda não iniciada: "nenhum")
Depois, execute os próximos passos. Ao terminar, atualize a tarefa
(updated, last_agent, Estado atual, Handoff e uma linha no Log) e devolva
cada arquivo alterado completo, num bloco de código com o caminho na primeira linha.
```

Se a IA errar alguma das cinco respostas, o handoff anterior estava incompleto: registre isso antes de continuar.

## 4. Como registrar decisões

1. A IA escreve a proposta na seção "Propostas de decisão" da tarefa.
2. Você decide. Se aprovar, adicione no fim de `DECISIONS.md` com o próximo ID (`D-NNN`) e `Status: accepted`.
3. Para revogar uma decisão, nunca apague: crie uma nova com `Substitui: D-00X` e mude a antiga para `superseded`.

## 5. Como aprovar alterações

1. Salve os arquivos devolvidos pela IA no repositório.
2. Rode `python hub_validate.py .` e corrija os erros apontados (ou peça à IA que corrija).
3. Revise as mudanças (`git diff`).
4. Aprovado: `git commit`. Se usar branches, o merge na branch principal é a aprovação oficial.

## 6. Como recuperar um projeto após uma interrupção

1. Rode `python hub_validate.py .` para confirmar que os arquivos estão íntegros.
2. Procure as tarefas em andamento: `grep -l "status: doing\|status: blocked" tasks/*.md`.
3. Em cada uma, leia Estado atual e Handoff. Os próximos 3 passos dizem exatamente por onde recomeçar.
4. Se o handoff estiver desatualizado, `git log -p tasks/TASK-NNN.md` mostra o que mudou em cada sessão.

---

## 7. Como fazer as IAs conversarem sem copiar e colar

Use o GitHub como ponto de encontro: um pedido gravado no repositório do projeto é enviado pelo GitHub Actions a várias IAs (via OpenRouter), e as respostas voltam gravadas no repositório.

1. Crie uma chave no OpenRouter, com limite de gastos, e salve-a como segredo `OPENROUTER_API_KEY` no repositório do projeto (Settings → Secrets and variables → Actions).
2. Copie para o projeto o workflow `.github/workflows/rodada.yml` e o arquivo `rodadas/modelos.txt` (um modelo por linha).
3. Para uma rodada nova, grave `rodadas/<nome>/pedido.md` (por exemplo, um pacote do `hub_pack.py`) e faça o push. As respostas aparecem em `rodadas/<nome>/respostas/`.

Teste local sem gastar: `python hub_ask.py pedido.md --models modelos.txt --dry-run`.

## O que o validador verifica

| Arquivo | Verificações |
| --- | --- |
| Estrutura | `PROJECT.md`, `DECISIONS.md`, `tasks/` e ao menos um `TASK-NNN.md` |
| `PROJECT.md` | metadados YAML válidos, campos obrigatórios, `id`, `type`, `status` e `sensitivity` permitidos |
| `DECISIONS.md` | IDs `D-NNN` únicos e em ordem, status válido, datas, substituições coerentes |
| `TASK-NNN.md` | metadados, `id` igual ao nome do arquivo, `project` igual ao do projeto, estado válido, datas, `last_agent` em tarefa iniciada, seções obrigatórias, referências a decisões existentes |
| Handoff | em tarefa iniciada: arquivos alterados, bloqueios e 3 próximos passos preenchidos; `blocked` com bloqueio real; aviso se faltar Validação |

Erros fazem o comando sair com código 1. Use `--strict` para tratar avisos como erros.

## Fora do escopo do MVP

MCP próprio, interfaces, LibreChat, LiteLLM, RAG, banco vetorial, LangGraph, n8n, painel e agentes autônomos. Só entram com necessidade comprovada (ver `SPEC.md`, seção 10).
