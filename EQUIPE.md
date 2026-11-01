# Organização do time de IAs

Status: **proposta aguardando aprovação do Product Owner**. Base: proposta do Grok (01/11/2026), com as ressalvas do Gemini, do Claude e do ChatGPT. Vale para todos os projetos que usam o AI HUB Protocol.

## 1. Problema

O humano gasta tempo e crédito distribuindo tarefas e repetindo contexto. Deixar as IAs se organizarem livremente gera discussão cara, conflito de responsabilidade e handoffs fracos.

## 2. Princípio

As IAs propõem; o humano escolhe; o trabalho segue o protocolo (Markdown + Git). Nenhuma IA distribui tarefa para outra nem assume trabalho sem escolha explícita do humano.

## 3. O time

| IA | Papel principal | Quando chamar com prioridade |
| --- | --- | --- |
| Claude | Execução: construir, escrever, programar | Quando é preciso produzir |
| ChatGPT | Planejamento, quebra de tarefa e revisão técnica | Quando o problema ainda está nebuloso; revisão de entregas técnicas |
| Gemini | Auditoria de contexto e continuidade; simplificação e corte de excessos | Leitura inicial de muito material; auditoria depois de uma entrega; quando o projeto inchar |
| Grok | Teste adversarial e caça a riscos | Antes de decisões importantes e depois de entregas |

Os papéis são referência inicial, não camisa de força, e serão revistos conforme os resultados dos testes (`RESULTADOS.md`). "Argon" não é uma IA separada: era um identificador do próprio Gemini.

## 4. Fluxo

**Padrão, no dia a dia: atribuição direta.** Quem executa a próxima tarefa é quem o handoff anterior indica ou quem o humano escolhe. Sem rodada de candidaturas.

**Rodada de candidaturas: só quando houver dúvida sobre o responsável** (abertura de projeto ou tarefa ambígua), quando o humano pedir e apenas às IAs que ele considerar relevantes.

1. O humano escreve o objetivo em poucas frases.
2. Cada IA consultada responde, na ordem Claude → ChatGPT → Gemini → Grok, com **no máximo 8 linhas**:
   - a entrega concreta que posso produzir;
   - como ela será verificada;
   - como eu faria (a abordagem, sem autopromoção);
   - o que preciso receber;
   - esforço estimado (baixo, médio ou alto).
3. O humano escolhe uma proposta (ou junta partes) e define o responsável e o revisor.
4. Daí em diante, o protocolo normal.

**Em toda tarefa, o fluxo é:** pedido → responsável escolhido → execução → revisão por outra IA → aprovação humana.

**O que fica registrado no arquivo da tarefa antes de começar:** responsável (`assignee`), revisor (`reviewer`), entrega esperada (Objetivo) e critérios de pronto. A próxima IA a trabalhar também precisa estar designada.

**Autorização por escopo:** a escolha do humano autoriza a IA a executar todos os passos necessários dentro do escopo da tarefa, sem pedir aprovação a cada ação. Qualquer mudança relevante de escopo volta ao humano.

Quando a rodada automática estiver ligada (`hub_ask.py` no GitHub Actions), as candidaturas podem ser coletadas por ela, sem o humano copiar e colar.

## 5. Regras de ouro

1. Nenhuma IA fala pela outra.
2. Nenhuma IA assume tarefa sem o humano ter escolhido.
3. Discussão entre IAs só no formato de candidatura (curto). Sem "reuniões" longas.
4. Quem executa uma entrega não é quem a revisa.
5. O Git e os arquivos Markdown são a única fonte oficial de verdade.
6. Ferramentas automáticas (rodadas no GitHub, interface futura) só disparam a partir de um pedido aprovado pelo humano, e tudo o que voltam é proposta, nunca decisão.

## 6. Hipóteses a medir

- Que os papéis acima são os melhores para cada IA.
- Que este fluxo reduz custo e tempo do humano. Medir em `RESULTADOS.md` antes de tratar como fato.

## 7. Votos

| Participante | Voto | Ressalvas |
| --- | --- | --- |
| Grok | Autor | — |
| Gemini | Concordo com ressalvas | Atalho direto no dia a dia; candidatura só na abertura ou em tarefa ambígua; limite de 8 linhas; Argon removido do time; papel do Gemini ampliado para leitura inicial e simplificação |
| Claude | Concordo com ressalvas | As mesmas do Gemini; quem executa não revisa; candidaturas pela rodada automática; sem autopromoção nas candidaturas; automação só a partir de pedido aprovado pelo humano |
| ChatGPT | Concordo com ressalvas | Candidatura só quando houver dúvida e só às IAs relevantes; comparar propostas pela entrega concreta e pela forma de verificação; autorização vale para o escopo da tarefa; registrar responsável, entrega, critérios e revisor na tarefa; papéis e economia de custo são hipóteses a medir |
| Product Owner | Pendente | — |
