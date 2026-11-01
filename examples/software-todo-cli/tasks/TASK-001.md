---
id: TASK-001
project: software-todo-cli
title: Implementar os comandos add e list
status: done
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: human
last_model:
---

# TASK-001: Implementar os comandos add e list

## Objetivo

`python todo.py add "texto"` salva um item e `python todo.py list` mostra todos, seguindo D-001 e D-002.

## Critério de pronto

- [x] `add` cria itens com IDs sequenciais e salva em `todo.json`
- [x] `list` mostra `[ ]` ou `[x]` antes de cada item
- [x] Testes automatizados cobrindo `add` e `list`
- [x] Revisão humana aprovada

## Leitura obrigatória

- `PROJECT.md`
- `DECISIONS.md` (D-001 e D-002)
- `todo.py`

## Estado atual

Concluída. Aprovada pelo humano em 2026-11-01 junto com a TASK-002, que se apoia neste código.

## Handoff

- **Arquivos alterados:** `tasks/TASK-001.md`
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1. Nenhum trabalho pendente nesta tarefa.
  2. A continuação está registrada na TASK-002 (concluída).
  3. Novas funções entram como novas tarefas.
- **Validação:** aprovação humana registrada; os testes de `add` e `list` seguem passando na suíte atual (12 testes).

## Propostas de decisão

- nenhuma

## Log de sessões

Uma linha por sessão, a mais recente no topo.

- 2026-11-01 · human · aprovou junto com a TASK-002; status → done
- 2026-11-01 · claude · implementou add e list com 4 testes; enviado para revisão
- 2026-11-01 · human · tarefa criada
