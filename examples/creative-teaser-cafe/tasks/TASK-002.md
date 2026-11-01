---
id: TASK-002
project: creative-teaser-cafe
title: Montar a lista de cenas para a gravação
status: review
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: claude
last_model: claude-opus-5-5
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

`lista-de-cenas.md` criado pelo Gemini: 5 planos (P-01 a P-05) cobrindo de 0 a 30 s, em ordem de luz para um único dia, só com equipe e voluntários, e a narração como item condicional. O Claude corrigiu uma inconsistência: a narração estava a 10h15–10h45 na tabela de áudio e a 10h00–10h30 no cronograma; ficou 10h00–10h30 nos dois. Recomendação: gravar a narração de qualquer jeito (30 min) e decidir D-003 na edição, com as duas versões prontas. Aguardando revisão humana.

## Handoff

- **Arquivos alterados:** `lista-de-cenas.md`, `tasks/TASK-002.md`
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1. Revisão cruzada da `lista-de-cenas.md` por uma IA que não a escreveu (o GPT), contra os critérios de pronto.
  2. Humano aprova a lista e marca esta tarefa como `done`.
  3. Abrir a TASK-003: execução da diária de gravação e montagem das versões A e B.
- **Validação:** conferido por script que os trechos cobrem de 0 a 30 s sem buracos, que não há termos proibidos por D-002 e que todas as menções à marca são "Café Aurora". Os horários da narração agora coincidem nas duas seções. A viabilidade real dos horários de luz não foi verificada.

## Propostas de decisão

- nenhuma

## Log de sessões

Uma linha por sessão, a mais recente no topo.

- 2026-11-01 · claude · alinhou o horário da narração (10h00–10h30) entre tabela e cronograma; handoff atualizado
- 2026-11-01 · gemini · (gemini-2.5-pro) criou `lista-de-cenas.md` com 5 planos otimizados por luz para 1 dia e narração condicional (D-003); atualizou `tasks/TASK-002.md` para `review`
- 2026-11-01 · human · tarefa criada a partir da aprovação da TASK-001
