---
id: TASK-002
project: software-todo-cli
title: Implementar o comando done
status: done
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: human
last_model:
---

# TASK-002: Implementar o comando done

## Objetivo

`python todo.py done 2` marca o item 2 como concluído e `list` passa a mostrar `[x]` nele.

## Critério de pronto

- [x] `done <id>` marca o item e salva em `todo.json` (D-002)
- [x] ID inexistente mostra mensagem de erro e sai com código 1
- [x] Testes novos em `test_todo.py`, todos passando

## Leitura obrigatória

- `PROJECT.md`
- `DECISIONS.md` (D-001 e D-002)
- `todo.py` e `test_todo.py`

## Estado atual

Concluída e aprovada pelo humano em 2026-11-01, após a revisão cruzada do Claude. O comando `done` está no ar.

## Handoff

- **Arquivos alterados:** `tasks/TASK-002.md`, `tasks/TASK-001.md`, `PROJECT.md`
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1. Nenhum trabalho pendente nesta tarefa.
  2. Novas funções do Todo CLI entram como novas tarefas (TASK-003 em diante).
  3. Opcional: rodar os testes num Python 3.10 para fechar a verificação de D-001.
- **Validação:** aprovação humana registrada. Testes conferidos na revisão do Claude (12 passando em 3.13).

## Propostas de decisão

- Problema real: o pacote não permite identificar o último arquivo alterado; esta tarefa nova diz nenhum, sem histórico da tarefa anterior. Impede o MVP? Não impede executar esta tarefa, mas impede comprovar 5/5 no teste de retomada. Solução mais simples: definir se a pergunta 5 se refere à tarefa ou ao projeto; quando for ao projeto, incluir no pacote o último handoff relevante e uma referência ao commit/diff disponível. Como testar: empacotar uma tarefa nova após outra tarefa alterar dois arquivos e verificar se a IA identifica a evidência disponível ou declara que a ordem é indeterminável, sem inventar.

- Resposta do Claude: proposta aceita na versão mais simples. A pergunta 5 passou a ser restrita à tarefa ("Quais arquivos a última sessão desta tarefa alterou? Tarefa ainda não iniciada: 'nenhum'") na SPEC, no README e no `hub_pack.py`. O histórico do projeto fica no Git, fora do teste.

## Log de sessões

Uma linha por sessão, a mais recente no topo.

- 2026-11-01 · human · aprovou o merge; status → done
- 2026-11-01 · claude · revisão cruzada: 12 testes passaram em 3.13, uso pelo terminal conferido; pergunta 5 corrigida no protocolo
- 2026-11-01 · gpt · implementou done e testes; 12 testes passaram; enviado para revisão
- 2026-11-01 · human · tarefa criada
