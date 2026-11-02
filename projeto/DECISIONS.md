# Decisões

Regras: só adicione no fim; nunca apague. Para revogar, crie uma decisão nova com `Substitui: D-00X` e mude o status da antiga para `superseded`.
Status possíveis: `proposed` | `accepted` | `superseded`. Só o humano marca `accepted`.

---

## D-001: Protocolo antes de plataforma

- **Status:** accepted
- **Data:** 2026-11-01
- **Aprovado por:** Gleyber Rodrigues
- **Decisão:** O AI HUB OS começa como protocolo (SPEC.md v0.4): PROJECT.md, DECISIONS.md e tasks/TASK-NNN.md com handoff. Ferramentas só entram com necessidade comprovada.
- **Motivo:** Evitar construir plataforma antes de provar a continuidade entre IAs.
- **Substitui:** —

## D-002: Git e Markdown são a fonte de verdade

- **Status:** accepted
- **Data:** 2026-11-01
- **Aprovado por:** Gleyber Rodrigues
- **Decisão:** Toda informação oficial vive em arquivos Markdown versionados no Git. Interfaces e automações leem e escrevem nesses arquivos; nunca guardam estado próprio que o Git não tenha.
- **Motivo:** Independência de fornecedor e histórico auditável.
- **Substitui:** —

## D-003: Interface mínima, construída pelo GPT

- **Status:** accepted
- **Data:** 2026-11-01
- **Aprovado por:** Gleyber Rodrigues
- **Decisão:** Construir a interface v1 (TASK-001), com o ChatGPT como responsável e o Claude como revisor. Na v1, a interface organiza o fluxo e não chama modelos de IA por conta própria.
- **Motivo:** O atrito medido é copiar e colar e não ver o estado das tarefas num lugar só.
- **Substitui:** —

## D-004: Claude constrói a Fase 1 do painel; GPT revisa

- **Status:** proposed
- **Data:** 2026-11-02
- **Aprovado por:** —
- **Decisão:** Pelo briefing de 02/11/2026, o Claude passa a ser o responsável pela TASK-001 (proposta e construção da Fase 1, conforme `INTERFACE.md`) e o ChatGPT passa a ser o revisor. O resto da D-003 continua: o painel só chama uma IA quando o humano clica em "Enviar".
- **Motivo:** O humano pediu a proposta técnica e a implementação diretamente ao Claude.
- **Substitui:** —
