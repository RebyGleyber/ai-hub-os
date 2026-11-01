---
id: TASK-001
project: creative-teaser-cafe
title: Escrever o roteiro do teaser
status: review
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: grok
last_model: grok-4
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

Roteiro completo em `roteiro.md` (0 a 30 s). Cena 4 escrita com duas opções de som (com e sem narração), respeitando D-001 e D-002. Aguardando aprovação humana e decisão sobre D-003.

## Handoff

- **Arquivos alterados:** `roteiro.md`, `tasks/TASK-001.md`
- **Bloqueios atuais:** nenhum. Aguardando decisão humana sobre D-003 (narração) e aprovação do roteiro.
- **Próximos 3 passos:**
  1. Humano aprovar ou rejeitar D-003.
  2. Humano revisar o roteiro completo e marcar a tarefa como `done` ou devolver com ajustes.
  3. Se aprovado, abrir TASK-002 para lista de cenas pronta para gravação.
- **Validação:** Tempos somam 30 s. Nenhum termo proibido por D-002. Nome da marca completo. Data e horário presentes. Duas versões de som registradas.

## Propostas de decisão

- D-003 (narração em voz feminina) continua aguardando decisão do humano.

## Log de sessões

- 2026-11-01 · grok · escreveu a cena 4 com duas opções de som; status → review
- 2026-11-01 · claude · escreveu as cenas 1 a 3; cena 4 pendente
- 2026-11-01 · human · tarefa criada
