---
id: TASK-001
project: software-todo-cli
title: Implementar os comandos add e list
status: review
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: claude
last_model: claude-opus-5-5
---

# TASK-001: Implementar os comandos add e list

## Objetivo

`python todo.py add "texto"` salva um item e `python todo.py list` mostra todos, seguindo D-001 e D-002.

## Critério de pronto

- [x] `add` cria itens com IDs sequenciais e salva em `todo.json`
- [x] `list` mostra `[ ]` ou `[x]` antes de cada item
- [x] Testes automatizados cobrindo `add` e `list`
- [ ] Revisão humana aprovada

## Leitura obrigatória

- `PROJECT.md`
- `DECISIONS.md` (D-001 e D-002)
- `todo.py`

## Estado atual

Comandos `add` e `list` implementados em `todo.py`, com 4 testes em `test_todo.py`. Aguardando revisão humana. O comando `done` ficou fora desta tarefa e está na TASK-002.

## Handoff

- **Arquivos alterados:** `todo.py`, `test_todo.py`
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1. Humano revisa `todo.py` e aprova o merge desta tarefa.
  2. Mudar o status desta tarefa para `done` após o merge.
  3. Iniciar a TASK-002 (comando `done`).
- **Validação:** rodei `python -m pytest` na pasta do projeto: 4 testes passaram. Não testei manualmente pelo terminal.

## Propostas de decisão

- nenhuma

## Log de sessões

- 2026-11-01 · claude · implementou add e list com 4 testes; enviado para revisão
- 2026-11-01 · human · tarefa criada
