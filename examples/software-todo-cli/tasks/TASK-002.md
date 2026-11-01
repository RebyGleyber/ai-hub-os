---
id: TASK-002
project: software-todo-cli
title: Implementar o comando done
status: review
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: claude
last_model: claude-opus-5-5
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

Comando `done` implementado pelo GPT e revisado pelo Claude (revisão cruzada: quem escreveu não revisou). Código, testes e comportamento pelo terminal conferem com o critério de pronto, D-001 e D-002. Pronta para aprovação humana.

Sessão do GPT (registro original): done com persistência em todo.json, erro e saída 1 para ID inexistente ou não inteiro; 12 testes passando em Python 3.14, a partir só do pacote.

## Handoff

- **Arquivos alterados:** `tasks/TASK-002.md`
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1. Humano aprova o merge desta tarefa e marca o status como `done`.
  2. Atualizar a "Situação atual" do `PROJECT.md`: `add`, `list` e `done` implementados.
  3. Opcional: rodar os testes num Python 3.10 para fechar a verificação de D-001.
- **Validação:** o Claude integrou os três arquivos do GPT sem alteração e revisou o diff (só acréscimos em `todo.py`: função `done` e o ramo `done` no `main`). Rodou `python3 -m pytest` em Python 3.13.18: 12 testes passaram, confirmando o relato do GPT (3.14). `todo.py` e `test_todo.py` compilam em 3.11 e 3.12, mas os testes não foram executados nessas versões (pytest ausente). Python 3.10 não verificado: nenhum recurso usado exige versão maior. Uso real pelo terminal: `add`, `done 2`, `list`, `done 99` (saída 1), `done abc` (saída 1), `done -1` (saída 1), `done 01` (aceito como 1); o `todo.json` ficou correto.

## Propostas de decisão

- Problema real: o pacote não permite identificar o último arquivo alterado; esta tarefa nova diz nenhum, sem histórico da tarefa anterior. Impede o MVP? Não impede executar esta tarefa, mas impede comprovar 5/5 no teste de retomada. Solução mais simples: definir se a pergunta 5 se refere à tarefa ou ao projeto; quando for ao projeto, incluir no pacote o último handoff relevante e uma referência ao commit/diff disponível. Como testar: empacotar uma tarefa nova após outra tarefa alterar dois arquivos e verificar se a IA identifica a evidência disponível ou declara que a ordem é indeterminável, sem inventar.

- Resposta do Claude: proposta aceita na versão mais simples. A pergunta 5 passou a ser restrita à tarefa ("Quais arquivos a última sessão desta tarefa alterou? Tarefa ainda não iniciada: 'nenhum'") na SPEC, no README e no `hub_pack.py`. O histórico do projeto fica no Git, fora do teste.

## Log de sessões

Uma linha por sessão, a mais recente no topo.

- 2026-11-01 · claude · revisão cruzada: 12 testes passaram em 3.13, uso pelo terminal conferido; pergunta 5 corrigida no protocolo
- 2026-11-01 · gpt · implementou done e testes; 12 testes passaram; enviado para revisão
- 2026-11-01 · human · tarefa criada
