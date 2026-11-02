---
id: TASK-001
project: ai-hub-os
title: Interface v1 do AI HUB OS
status: review
owner: Gleyber Rodrigues
assignee: claude
reviewer: gpt
created: 2026-11-01
updated: 2026-11-02
last_agent: claude
last_model: claude-opus-5-5
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
- `INTERFACE.md` (a proposta)

## Estado atual

Proposta da Fase 1 escrita pelo Claude em `INTERFACE.md`, a partir do briefing do humano de 02/11/2026 ("Nova fase: Dashboard e Gestão Inteligente de Projetos"), que pediu a proposta diretamente ao Claude. Responsável e revisor trocados (agora Claude e GPT), com a mudança registrada na proposta D-004. Nenhum código foi escrito. Aguardando a revisão do GPT e a aprovação do humano. Questão em aberto para o humano: se a entrega 6 (envio automático via OpenRouter) entra na Fase 1.

## Handoff

- **Arquivos alterados:** `INTERFACE.md`, `DECISIONS.md`, `tasks/TASK-001.md`
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1. GPT revisa `INTERFACE.md` contra o Critério de pronto, D-002 e D-003, e registra o parecer em Propostas de decisão ou num comentário do PR.
  2. Humano aprova a proposta (merge do PR) e decide sobre a D-004 e a entrega 6.
  3. Claude começa pela entrega 1 (`hub_core.py`), sem mudar o comportamento do validador.
- **Validação:** conferido que os números citados batem com os arquivos (Plano B: 5 tarefas e 17 decisões; 72 testes; pacote com cerca de 18 mil caracteres). Arquitetura e estimativa de esforço: não verificadas, são proposta.

## Propostas de decisão

- D-004 (em `DECISIONS.md`, status `proposed`): Claude constrói, GPT revisa.

## Log de sessões

Uma linha por sessão, a mais recente no topo.

- 2026-11-02 · claude · proposta da Fase 1 do painel em `INTERFACE.md`; D-004 proposta; enviado para revisão do GPT
- 2026-11-01 · human · tarefa criada; responsável GPT, revisor Claude
