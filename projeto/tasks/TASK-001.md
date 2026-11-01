---
id: TASK-001
project: ai-hub-os
title: Interface v1 do AI HUB OS
status: todo
owner: Gleyber Rodrigues
assignee: gpt
reviewer: claude
created: 2026-11-01
updated: 2026-11-01
last_agent: human
last_model:
---

# TASK-001: Interface v1 do AI HUB OS

## Objetivo

Uma interface simples, usada pelo humano no computador, que mostra o estado de todos os projetos e tarefas e tira o copiar e colar do caminho: o humano escolhe a tarefa, gera o pacote para a IA, registra a resposta e aprova, tudo num lugar só. Primeira entrega: `INTERFACE.md` com a proposta técnica para aprovação, antes de qualquer código.

## Critério de pronto

- [ ] `INTERFACE.md` com a proposta: telas, tecnologia, como roda no computador do humano e como lê e grava nos repositórios Git, aprovada pelo humano antes do código
- [ ] Mostra projetos e tarefas com status, responsável, revisor e bloqueios, lidos dos arquivos (D-002)
- [ ] Para uma tarefa: gera o pacote pronto para copiar ou baixar, reaproveitando `hub_pack.py`
- [ ] Recebe a resposta da IA (arquivos devolvidos) e mostra o resultado do validador antes de gravar
- [ ] Aprovação humana vira commit; nada é gravado sem o clique do humano
- [ ] Não chama modelos de IA por conta própria (D-003; EQUIPE.md, regra 6)
- [ ] Sem banco de dados nem servidor novo; roda localmente; segredos fora do repositório
- [ ] Testes automatizados para a lógica nova e instruções de instalação para quem não programa

## Leitura obrigatória

- `PROJECT.md`
- `DECISIONS.md` (D-001, D-002, D-003)
- `../SPEC.md` (o protocolo)
- `../EQUIPE.md` (fluxo e papéis do time)

## Estado atual

Tarefa ainda não iniciada. Responsável: GPT. Revisor: Claude. A primeira sessão entrega só a proposta (`INTERFACE.md`), sem código.

## Handoff

- **Arquivos alterados:** nenhum
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1.
  2.
  3.
- **Validação:** não verificado

## Propostas de decisão

- nenhuma

## Log de sessões

Uma linha por sessão, a mais recente no topo.

- 2026-11-01 · human · tarefa criada; responsável GPT, revisor Claude
