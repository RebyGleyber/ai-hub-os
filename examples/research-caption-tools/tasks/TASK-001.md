---
id: TASK-001
project: research-caption-tools
title: Comparar 3 ferramentas e recomendar uma
status: blocked
owner: Gleyber Rodrigues
created: 2026-11-01
updated: 2026-11-01
last_agent: claude
last_model: claude-opus-5-5
---

# TASK-001: Comparar 3 ferramentas e recomendar uma

## Objetivo

Arquivo `comparacao.md` com 3 ferramentas avaliadas pelos critérios de D-001 e uma recomendação final justificada.

## Critério de pronto

- [x] Critérios e pesos definidos (`criterios.md`)
- [ ] Teto de orçamento mensal definido pelo humano
- [ ] 3 ferramentas escolhidas dentro do teto (D-003)
- [ ] Tabela comparativa com fontes e datas de consulta
- [ ] Recomendação final

## Leitura obrigatória

- `PROJECT.md`
- `DECISIONS.md` (D-001 e D-003; D-002 foi substituída)
- `criterios.md`

## Estado atual

Critérios prontos em `criterios.md`. A escolha das 3 ferramentas depende do teto de orçamento mensal, que ainda não foi informado. Nenhuma pesquisa de ferramenta foi feita.

## Handoff

- **Arquivos alterados:** `criterios.md`
- **Bloqueios atuais:** falta o teto de orçamento mensal (em dólares), que só o humano pode definir
- **Próximos 3 passos:**
  1. Humano informa o teto de orçamento mensal neste arquivo, em Estado atual, e muda o status para `doing`.
  2. Listar 3 ferramentas dentro do teto, com link da página de preços e data de consulta.
  3. Criar `comparacao.md` com a tabela pelos critérios de `criterios.md` e a recomendação final.
- **Validação:** conferi que os pesos de `criterios.md` somam 100%. Nenhum dado de ferramenta foi coletado ainda.

## Propostas de decisão

- nenhuma

## Log de sessões

- 2026-11-01 · claude · definiu critérios; bloqueado por falta do teto de orçamento
- 2026-11-01 · human · tarefa criada
