---
id: TASK-002
project: creative-teaser-cafe
title: Montar a lista de cenas para a gravação
status: review
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: gemini
last_model: gemini-2.5-pro
---

# TASK-002: Montar a lista de cenas para a gravação

## Objetivo

Arquivo `lista-de-cenas.md` com tudo o que a equipe precisa para gravar o teaser num único dia, a partir do roteiro aprovado (D-004).

## Critério de pronto

- [x] Uma linha por plano a gravar, cobrindo as cenas 1 a 4 de `roteiro.md`
- [x] Para cada plano: local, enquadramento vertical 9:16 (D-001), ação, quem aparece, objetos de cena e horário de luz
- [x] Ordem de gravação otimizada para um único dia (restrição do PROJECT.md)
- [x] Nenhum ator pago: só equipe e clientes voluntários (restrição do PROJECT.md)
- [x] Gravação da narração listada como item condicional, dependente de D-003

## Leitura obrigatória

- `PROJECT.md`
- `DECISIONS.md` (D-001, D-002, D-004 e a proposta D-003)
- `roteiro.md`

## Estado atual

O arquivo `lista-de-cenas.md` foi criado cobrindo integralmente as cenas 1 a 4 de `roteiro.md`, desmembradas em 5 planos operacionais (`P-01` a `P-05`, separando a Cena 2 em `P-02` para a abertura da porta com luz natural às 07h15 e `P-05` para o detalhe da máquina de espresso às 09h30). A ordem de gravação foi organizada cronologicamente pela posição do sol (06h45 às 10h30) para execução em um único dia, utilizando apenas equipe interna e clientes voluntários. A gravação da narração feminina para a Cena 4 foi incluída em seção dedicada como item estritamente condicional, dependente da decisão `D-003` (que segue `proposed`), mantendo compatibilidade com as Versões A e B exigidas pela `D-004`. Tarefa pronta para revisão humana.

## Handoff

- **Arquivos alterados:** `lista-de-cenas.md` (criado), `tasks/TASK-002.md` (atualizado)
- **Bloqueios atuais:** Decisão `D-003` (narração em voz feminina na cena 4) permanece com status `proposed` em `DECISIONS.md` (não bloqueia a aprovação de `lista-de-cenas.md`, mas define se o item condicional de locução será executado na diária/edição).
- **Próximos 3 passos:**
  1. Humano (`Gleyber Rodrigues`) revisar e aprovar `lista-de-cenas.md` e definir o status de `D-003` (`accepted` ou revogada) em `DECISIONS.md`.
  2. Marcar `tasks/TASK-002.md` como `done` após o commit/merge na branch principal.
  3. Abrir a `TASK-003` para acompanhar a execução da diária de gravação e a montagem das versões finais do vídeo de 30s (9:16).
- **Validação:** não verificado (conferência manual de conformidade contra os critérios de pronto de `TASK-002.md`, `roteiro.md`, `PROJECT.md` e decisões `D-001`, `D-002` e `D-004`; validador automatizado não executado nesta sessão).

## Propostas de decisão

- nenhuma

## Log de sessões

Uma linha por sessão, a mais recente no topo.

- 2026-11-01 · gemini · (gemini-2.5-pro) criou `lista-de-cenas.md` com 5 planos otimizados por luz para 1 dia e narração condicional (D-003); atualizou `tasks/TASK-002.md` para `review`
- 2026-11-01 · human · tarefa criada a partir da aprovação da TASK-001
