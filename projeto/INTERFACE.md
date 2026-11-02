# Proposta: Painel do AI HUB OS, Fase 1

Status: **proposta para aprovação do Product Owner** (TASK-001). Autor: Claude. Revisor: ChatGPT.
Base: briefing "Nova fase: Dashboard e Gestão Inteligente de Projetos" (02/11/2026), D-001 a D-003, `SPEC.md` e `EQUIPE.md`.

## 1. Resumo em 6 linhas

- Um painel que roda **no seu Mac**, aberto no navegador, com a cara de um chat moderno em modo escuro.
- Ele **lê e grava os mesmos arquivos Markdown** dos repositórios. Não há banco de dados nem segunda fonte de verdade (D-002).
- Você nunca vê YAML nem Git: clica em "Aprovar" e o painel grava o arquivo, roda o validador e faz o commit.
- Reaproveita o que já existe: o validador vira o "leitor" do painel, o `hub_pack.py` vira o botão "Enviar para uma IA" e o `hub_ask.py` vira o envio automático.
- A Fase 1 sai em **6 entregas pequenas**, cada uma usável e conferível por você. A primeira tela útil aparece na entrega 2.
- Custo de operação: **US$ 0** sem chamadas automáticas às IAs. Com o envio automático (entrega 6, opcional), paga-se só o consumo de tokens, que fica registrado por tarefa.

## 2. As 4 perguntas do Product Owner

| Pergunta | Resposta |
| --- | --- |
| Qual problema real resolve? | Os dois atritos medidos: você copia e cola contexto entre as IAs e não tem uma visão única de projetos, tarefas e decisões. |
| Impede o MVP? | Não. O MVP do protocolo já foi atingido (`RESULTADOS.md`). O painel fica por cima do protocolo, sem mudá-lo. |
| Implementação mais simples? | Um programa local em Python que reaproveita os três scripts e serve uma única página. Sem nuvem, sem login e sem banco. |
| Como testar? | Cada entrega tem um teste de aceite na seção 7, feito por você em minutos, e testes automatizados no repositório. |

## 3. O que já existe e o que falta

| Função do painel | Já existe | Falta construir |
| --- | --- | --- |
| Ler projeto, decisões e tarefas | `hub_validate.py` já interpreta todos os arquivos | Expor essa leitura como dados para a tela (`hub_core.py`) |
| Garantir que nada inválido seja gravado | Validador com 72 testes | Rodar o validador antes de cada gravação e mostrar o resultado em português simples |
| Mandar uma tarefa para uma IA | `hub_pack.py`, com omissão das linhas CONFIDENCIAL | Botão "Copiar pacote" e tela "Colar resposta" |
| Receber a resposta de uma IA | Formato fixo: arquivos completos em blocos de código com o caminho | Leitor desses blocos, tela de diferenças e botão "Aprovar" |
| Falar com as IAs sem copiar e colar | `hub_ask.py` (OpenRouter), com registro de tokens | Botão "Enviar" no chat, com escolha do modelo (entrega 6) |
| Responsável e revisor | Campos `assignee` e `reviewer`; o validador barra quem revisa a própria entrega | Mostrar e editar esses campos na tela |
| Modelos de projeto e tarefa | `templates/` | Assistente "Novo projeto" e formulário "Nova tarefa" |
| Histórico | Git | Mostrar "quem fez o quê, quando" lendo o Log das tarefas e o `git log` |

## 4. Arquitetura mínima

```text
 Seu navegador (http://localhost:8765)
        │  telas
        ▼
 hub_app.py ── programa local em Python (FastAPI)
        │
        ├── hub_core.py      ← leitura extraída do hub_validate.py
        ├── hub_validate.py  ← valida antes de gravar
        ├── hub_pack.py      ← monta o pacote para a IA
        ├── hub_ask.py       ← envio automático (entrega 6, opcional)
        └── git              ← "Aprovar" = gravar + validar + commit + push
        │
        ▼
 Pastas dos projetos no seu Mac (clones Git: ai-hub-os, plano-b-brasil, ...)
```

Regras da arquitetura:

1. **Uma fonte de verdade.** O painel não guarda dados próprios. Toda tela é lida dos arquivos na hora. A única configuração local é a lista das pastas de projeto, em `~/.aihub/config.json`, fora do repositório.
2. **Nada é gravado sem o seu clique.** Antes de "Aprovar" você vê o que muda (diferenças), o resultado do validador e a mensagem do commit. Erro do validador bloqueia o botão.
3. **Conversas também são arquivos.** Cada conversa de um projeto fica em `conversas/AAAA-MM-DD-assunto.md` no próprio repositório: o pedido, o modelo usado, a resposta e os tokens. Outra IA que abrir o repositório encontra o histórico.
4. **Segredos fora do Git.** A chave do OpenRouter fica no Keychain do Mac, nunca num arquivo do repositório.
5. **O protocolo não muda.** Um projeto editado no painel continua editável à mão, por qualquer IA ou pelo GitHub, e vice-versa.

### Por que local, e não um site

| Opção | Vantagem | Por que não agora |
| --- | --- | --- |
| **Local no Mac (proposta)** | Custo zero, usa o Git que já está no Mac, sem login, sem expor dados confidenciais | Não abre no celular |
| Site hospedado (Vercel + API do GitHub) | Abre de qualquer lugar | Exige login, guardar tokens num servidor e custo mensal; aumenta o risco para o Plano B |

O celular entra na Fase 2 ou 3, com o mesmo código de tela, quando o uso no Mac estiver provado.

## 5. Tecnologia

| Camada | Escolha | Motivo |
| --- | --- | --- |
| Servidor local | **Python + FastAPI** | Os três scripts já são Python: o painel os importa diretamente, sem reescrever nada |
| Tela | **React + TypeScript + Vite + Tailwind** | Chat fluido, quadro de tarefas e painéis da Fase 2 sem trocar de tecnologia; modo escuro nativo |
| Componentes | shadcn/ui (código aberto, copiado para o projeto) | Visual moderno e consistente sem dependência de fornecedor |
| Git | Comando `git` do próprio Mac | Usa o seu login do GitHub, já configurado |
| Instalação | Um arquivo de duplo clique, `Abrir AI HUB.command` | Você não precisa de terminal; a tela vem pronta (compilada), então não é preciso instalar Node |

Alternativa descartada: páginas geradas pelo servidor (HTMX). É mais simples, mas o chat e o quadro de tarefas ficariam menos fluidos e a Fase 2 obrigaria a trocar de tecnologia.

## 6. Navegação e organização visual

```text
┌──────────────────┬────────────────────────────────────────────────────────┐
│  AI HUB OS       │  Plano B Brasil                    ● ativo   ⚠ 2 bloq. │
│                  │  Conversas | Visão geral | Tarefas | Decisões | Arquivos│
│  ◧ Painel geral  ├────────────────────────────────────────────────────────┤
│  ＋ Novo projeto  │                                        ┌─────────────┐ │
│                  │  Você → GPT · TASK-001 (quiz)          │ TASK-001    │ │
│  PROJETOS        │  "Faça a próxima etapa..."             │ doing · GPT │ │
│  ● Plano B Brasil│                                        │ revisor:    │ │
│  ● AI HUB OS     │  GPT → resposta (2 arquivos)           │ Claude      │ │
│  ○ Teaser Café   │  ✔ validador: 0 erros                  │ próximos    │ │
│                  │  [Ver diferenças] [Aprovar]            │ passos: ... │ │
│  ⚙ Equipe        │                                        └─────────────┘ │
│  ⚙ Configurações │  [Tarefa ▾] [IA ▾]  Escreva...    [Copiar] [Enviar]    │
└──────────────────┴────────────────────────────────────────────────────────┘
```

- **Barra lateral:** Painel geral, Novo projeto, lista de projetos (cor = status), Equipe (a `EQUIPE.md` legível) e Configurações (pastas e chave).
- **Painel geral:** cartões com o que precisa de você (tarefas em `review`, decisões `proposed`), tarefas bloqueadas, o trabalho de cada IA e a última atividade de cada projeto.
- **Dentro do projeto,** a primeira aba é **Conversas**, como o coração do sistema (a sua orientação no briefing). Ao lado do chat fica o cartão da tarefa ativa.
  - Visão geral: objetivo, situação e progresso por status.
  - Tarefas: quadro por status (todo, doing, review, done, blocked).
  - Decisões: lista com filtros; aprovar uma proposta é um clique seu.
  - Arquivos: leitura dos documentos do projeto.
- **Equipes e Finanças não aparecem na Fase 1.** Pelo seu próprio critério, nenhuma aba entra sem dados reais por trás. Elas chegam na Fase 2, também como arquivos (seção 9).

## 7. Entregas da Fase 1

Cada entrega termina com testes automatizados passando, validador sem erros e um teste de aceite que você faz.

| # | Entrega | Seu teste de aceite | Complexidade |
| --- | --- | --- | --- |
| 1 | `hub_core.py`: a leitura sai do validador e vira dados para a tela; o validador continua igual | Nenhuma tela ainda; os 72 testes atuais continuam passando, mais os novos | Baixa |
| 2 | Painel somente leitura: barra lateral, Painel geral, Visão geral, Tarefas e Decisões, com duplo clique para abrir | Abrir no Mac e conferir que o Plano B mostra as 5 tarefas e as 17 decisões com os status certos | Média |
| 3 | Conversa manual: escolher tarefa e IA, "Copiar pacote", colar a resposta, ver diferenças e validador, "Aprovar" = commit | Repetir a entrega real do GPT na TASK-002 do Todo CLI; uma resposta com erro precisa ser barrada | Média-alta |
| 4 | Edição pelo painel: nova tarefa, mudar status, responsável e revisor, propor e aceitar decisão | Criar uma tarefa pelo painel e ver o arquivo `TASK-NNN.md` correto no GitHub | Média |
| 5 | Novo projeto (assistente a partir dos templates) e aba Arquivos | Criar um projeto de teste do zero, sem terminal | Baixa-média |
| 6 | **Opcional, depende da sua aprovação:** botão "Enviar" no chat, via OpenRouter, com escolha do modelo e tokens registrados na conversa | Uma pergunta real a um modelo, com resposta e tokens gravados em `conversas/` | Baixa (reaproveita o `hub_ask.py`) |

Ordem: 1 → 2 → 3 → 4 → 5, e a 6 quando você liberar a chave. A primeira tela utilizável é a entrega 2; a partir da 3, o painel já substitui o copiar e colar com cada IA.

Estimativa de esforço: cerca de 6 a 8 sessões de trabalho do Claude no total, com revisão do GPT a cada entrega. Não verificado: é uma estimativa, a ser medida em `RESULTADOS.md`.

## 8. Custos operacionais

| Item | Custo | Observação |
| --- | --- | --- |
| Hospedagem | US$ 0 | Roda no seu Mac |
| Software do painel | US$ 0 | Todas as peças são de código aberto |
| Entregas 1 a 5 | US$ 0 a mais | Você continua usando as assinaturas que já tem (ChatGPT, Claude, Gemini, Grok) |
| Entrega 6 (envio automático) | Por consumo | Tokens × preço do modelo no OpenRouter. Um pacote de tarefa tem hoje cerca de 18 mil caracteres, ou seja, alguns milhares de tokens de entrada, mais a resposta. O valor real de cada chamada fica gravado na conversa, e o limite de gastos fica na própria chave. |

Não incluí valores em dólar por chamada porque os preços mudam por modelo e por mês. O painel vai mostrar o custo medido de cada tarefa, que é o dado confiável para comparar modelos (passo 5 da sua lista de economia de tokens).

## 9. Como as Fases 2 e 3 entram sem quebrar nada

A Fase 1 já deixa o terreno pronto. Tudo continua em arquivo:

- **Departamentos e funções (Fase 2):** um campo `area:` nas tarefas (Marketing, Produto, Jurídico...) e um arquivo `TIME.md` por projeto com as funções, dizendo se cada uma é pessoa ou IA. Funções regulamentadas, como advogado e contador, são sempre pessoas: o painel não deixa atribuir uma IA a elas.
- **Finanças (Fase 2):** `FINANCAS.md` por projeto, com uma tabela de itens, cada um marcado como `estimativa` ou `real` e com a premissa escrita ao lado. Nenhum número entra sem premissa.
- **Planejamento por IA (Fase 2):** "Novo projeto a partir de uma ideia" gera uma *proposta* de departamentos, tarefas, custos e riscos. Só depois da sua aprovação o painel cria os arquivos (a sua seção 8).
- **Orquestração e economia de tokens (Fase 3):** o consumo registrado por conversa na Fase 1 alimenta a comparação de custo e desempenho e, mais tarde, a escolha automática do modelo.

## 10. Pontos de atenção

1. **D-003 precisa ser atualizada.** Ela diz que o GPT constrói e o Claude revisa. Com este briefing, você passou a construção para o Claude. A proposta D-004 registra a troca: o Claude constrói e o GPT revisa. O resto da D-003 continua valendo, porque o painel só chama uma IA quando você clica em "Enviar".
2. **"Argon" é o Gemini.** Isso já foi corrigido na `EQUIPE.md`. Os papéis do briefing (Gemini para pesquisa) e da EQUIPE (Gemini como auditor) são hipóteses a medir, não regras do painel: na tela, você escolhe a IA de cada tarefa.
3. **Proteção da main.** Se você ativar "Do not allow bypassing" no GitHub, o botão "Aprovar" do painel, que faz push com o seu login, também será recusado. Recomendo deixar a proteção sem essa opção, ou não ativá-la por enquanto. O painel já garante que nada é gravado sem você.
4. **Confidencialidade.** O botão "Copiar pacote" usa o `hub_pack.py`, que omite as linhas CONFIDENCIAL. Para o GPT, que tem acesso direto ao Plano B (D-017), isso não muda nada.
5. **Celular fica fora da Fase 1** (seção 4).

## 11. O que preciso de você

1. Aprovar esta proposta: o merge do PR ou um "aprovo a INTERFACE".
2. Aceitar a D-004.
3. Dizer se a entrega 6 (envio automático pelo OpenRouter) entra já na Fase 1 ou fica para a Fase 3. Sem ela, o chat da Fase 1 funciona copiando o pacote e colando a resposta, só que tudo dentro do painel.
