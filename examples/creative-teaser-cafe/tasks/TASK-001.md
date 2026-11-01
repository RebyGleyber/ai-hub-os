---
id: TASK-001
project: creative-teaser-cafe
title: Escrever o roteiro do teaser
status: done
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: human
last_model:
---

# TASK-001: Escrever o roteiro do teaser

## Objetivo

Roteiro completo de 30 segundos em `roteiro.md`, cena a cena, pronto para aprovação e gravação.

## Critério de pronto

- [x] Cenas 1 a 3 escritas com tempo, imagem, texto e som
- [x] Cena 4 (fechamento) escrita, com data e horário da inauguração
- [x] Soma dos tempos igual a 30 s (D-001)
- [x] Nenhuma linguagem de promoção (D-002)

## Leitura obrigatória

- `PROJECT.md`
- `DECISIONS.md` (D-001, D-002 e a proposta D-003)
- `roteiro.md`

## Estado atual

Concluída. Roteiro aprovado pelo humano (D-004), com as duas versões de som na cena 4. A escolha entre elas depende de D-003, ainda `proposed`. A continuação está na TASK-002.

## Handoff

- **Arquivos alterados:** `DECISIONS.md`, `tasks/TASK-001.md`, `tasks/TASK-002.md`
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1. Executar a TASK-002 (lista de cenas para gravação).
  2. Humano decidir D-003 (narração) antes da edição final.
  3. Depois da TASK-002, abrir a tarefa de gravação.
- **Validação:** aprovação dada pelo humano em 2026-11-01. As afirmações da sessão do Grok (tempos, termos proibidos, marca e data) foram conferidas por script e são verdadeiras.

## Propostas de decisão

- D-003 (narração em voz feminina) continua aguardando decisão do humano.

## Log de sessões

- 2026-11-01 · human · aprovou o roteiro (D-004); status → done; abriu a TASK-002
- 2026-11-01 · grok · escreveu a cena 4 com duas opções de som; status → review
- 2026-11-01 · claude · escreveu as cenas 1 a 3; cena 4 pendente
- 2026-11-01 · human · tarefa criada
