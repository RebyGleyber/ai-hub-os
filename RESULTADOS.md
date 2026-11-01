# Resultados dos testes de continuidade

Uma linha por handoff testado, o mais recente no topo. Teste de retomada: SPEC.md, seção 9.

| Data | Projeto / tarefa | De → Para | Retomada | Continuou sem perguntar? | Falhas encontradas | Correção |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-11-01 | creative-teaser-cafe / TASK-001 | Claude → Grok | 5/5 | Sim | 1) "Bloqueios atuais" misturava "nenhum" com uma dependência opcional (D-003), gerando dúvida sobre o que é bloqueio. 2) Validação fraca: o validador confere a forma, não a verdade. | 1) v0.4.2: regra na SPEC (bloqueio = só o que impede agora) e aviso no validador. 2) Conhecido; mitigado por revisão humana (SPEC, seção 8). Em aberto. |
