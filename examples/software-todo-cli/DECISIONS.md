# Decisões

Regras: só adicione no fim; nunca apague. Para revogar, crie uma decisão nova com `Substitui: D-00X` e mude o status da antiga para `superseded`.
Status possíveis: `proposed` | `accepted` | `superseded`. Só o humano marca `accepted`.

---

## D-001: Só biblioteca padrão do Python

- **Status:** accepted
- **Data:** 2026-11-01
- **Aprovado por:** Gleyber Rodrigues
- **Decisão:** O programa usa apenas a biblioteca padrão do Python 3.10 ou superior. Testes usam pytest, que não é dependência do programa.
- **Motivo:** Qualquer IA ou pessoa consegue rodar sem instalar nada.
- **Substitui:** —

## D-002: Itens salvos em todo.json

- **Status:** accepted
- **Data:** 2026-11-01
- **Aprovado por:** Gleyber Rodrigues
- **Decisão:** Os itens ficam numa lista JSON em `todo.json`, na pasta atual, com os campos `id`, `text` e `done`.
- **Motivo:** Formato legível e fácil de inspecionar.
- **Substitui:** —
