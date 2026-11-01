"""Testes do validador do AI HUB Protocol v0.4.

Cada teste parte de uma cópia do template (válido) e quebra uma regra.
"""
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import hub_validate  # noqa: E402

TEMPLATE = ROOT / "templates"
EXAMPLES = sorted(p for p in (ROOT / "examples").iterdir() if p.is_dir())

STARTED_HANDOFF = """## Handoff

- **Arquivos alterados:** `roteiro.md`
- **Bloqueios atuais:** nenhum
- **Próximos 3 passos:**
  1. Passo um.
  2. Passo dois.
  3. Passo três.
- **Validação:** não verificado
"""


@pytest.fixture
def project(tmp_path):
    dest = tmp_path / "proj"
    shutil.copytree(TEMPLATE, dest)
    return dest


def replace(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text, f"trecho não encontrado em {path.name}: {old!r}"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def start_task(project: Path, handoff: str = STARTED_HANDOFF) -> Path:
    """Muda a TASK-001 do template para 'doing' com um handoff completo,
    como se a IA 'claude' tivesse trabalhado nela e alterado roteiro.md."""
    for name in ("roteiro.md", "script.md"):
        (project / name).write_text("rascunho\n", encoding="utf-8")
    task = project / "tasks" / "TASK-001.md"
    replace(task, "status: todo", "status: doing")
    replace(task, "last_agent: human", "last_agent: claude")
    replace(task, "- 2026-11-01 · human · tarefa criada",
            "- 2026-11-01 · claude · trabalhou no roteiro\n- 2026-11-01 · human · tarefa criada")
    text = task.read_text(encoding="utf-8")
    start = text.index("## Handoff")
    end = text.index("## Propostas de decisão")
    task.write_text(text[:start] + handoff + "\n" + text[end:], encoding="utf-8")
    return task


def messages(report, level=None):
    return [i.message for i in report.issues if level is None or i.level == level]


def has(report, fragment, level="ERRO"):
    return any(fragment in m for m in messages(report, level))


# ------------------------------------------------------------ arquivos válidos

def test_template_is_clean():
    report = hub_validate.validate_project(TEMPLATE)
    assert report.issues == [], messages(report)


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_examples_have_no_errors(path):
    # exemplos guardam sessões reais de IAs e podem ter avisos documentados
    # em RESULTADOS.md; erros, nunca
    report = hub_validate.validate_project(path)
    assert report.errors == [], messages(report, "ERRO")


def test_started_task_with_full_handoff_is_valid(project):
    start_task(project)
    assert hub_validate.validate_project(project).issues == []


# --------------------------------------------------------------- estrutura

@pytest.mark.parametrize("name", ["PROJECT.md", "DECISIONS.md"])
def test_missing_required_file(project, name):
    (project / name).unlink()
    report = hub_validate.validate_project(project)
    assert any(i.file == name and "não encontrado" in i.message for i in report.errors)


def test_missing_tasks_folder(project):
    shutil.rmtree(project / "tasks")
    assert has(hub_validate.validate_project(project), "pasta obrigatória")


def test_empty_tasks_folder(project):
    (project / "tasks" / "TASK-001.md").unlink()
    assert has(hub_validate.validate_project(project), "nenhuma tarefa")


def test_badly_named_task_file_is_warned(project):
    (project / "tasks" / "notas.md").write_text("rascunho", encoding="utf-8")
    report = hub_validate.validate_project(project)
    assert report.errors == []
    assert has(report, "fora do padrão", level="AVISO")


# ----------------------------------------------------------- PROJECT.md

def test_project_without_front_matter(project):
    path = project / "PROJECT.md"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.split("---", 2)[2], encoding="utf-8")
    assert has(hub_validate.validate_project(project), "sem metadados YAML")


def test_project_invalid_yaml(project):
    replace(project / "PROJECT.md", "name: Nome do Projeto", "name: [sem fechar")
    assert has(hub_validate.validate_project(project), "YAML inválido")


def test_project_missing_required_field(project):
    replace(project / "PROJECT.md", "owner: Nome do responsável", "owner:")
    assert has(hub_validate.validate_project(project), "'owner'")


@pytest.mark.parametrize("old,new,field", [
    ("type: business", "type: marketing-digital", "'type' inválido"),
    ("status: active", "status: ativo", "'status' inválido"),
    ("id: nome-do-projeto", "id: Nome Do Projeto", "'id' inválido"),
])
def test_project_invalid_values(project, old, new, field):
    replace(project / "PROJECT.md", old, new)
    assert has(hub_validate.validate_project(project), field)


def test_project_other_protocol_version_is_warning(project):
    replace(project / "PROJECT.md", "protocol: ai-hub v0.4", "protocol: ai-hub v0.1")
    report = hub_validate.validate_project(project)
    assert report.errors == []
    assert has(report, "'protocol'", level="AVISO")


# ---------------------------------------------------------- DECISIONS.md

NEW_DECISION = """
## D-002: Nova decisão

- **Status:** accepted
- **Data:** 2026-11-02
- **Aprovado por:** Nome
- **Decisão:** Algo.
- **Motivo:** Algo.
- **Substitui:** {replaces}
"""


def add_decision(project, text):
    path = project / "DECISIONS.md"
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def test_decision_invalid_status(project):
    replace(project / "DECISIONS.md", "**Status:** accepted", "**Status:** aprovada")
    assert has(hub_validate.validate_project(project), "status inválido")


def test_decision_duplicate_id(project):
    add_decision(project, NEW_DECISION.replace("D-002", "D-001").format(replaces="—"))
    assert has(hub_validate.validate_project(project), "repetido")


def test_decision_out_of_order(project):
    replace(project / "DECISIONS.md", "## D-001:", "## D-005:")
    add_decision(project, NEW_DECISION.format(replaces="—"))
    assert has(hub_validate.validate_project(project), "fora de ordem")


def test_supersede_requires_old_decision_marked(project):
    add_decision(project, NEW_DECISION.format(replaces="D-001"))
    assert has(hub_validate.validate_project(project), "não está como 'superseded'")


def test_supersede_done_correctly(project):
    replace(project / "DECISIONS.md", "**Status:** accepted", "**Status:** superseded")
    add_decision(project, NEW_DECISION.format(replaces="D-001"))
    assert hub_validate.validate_project(project).errors == []


def test_supersede_unknown_decision(project):
    add_decision(project, NEW_DECISION.format(replaces="D-009"))
    assert has(hub_validate.validate_project(project), "D-009, que não existe")


# -------------------------------------------------------------- TASK-NNN.md

def test_task_id_must_match_filename(project):
    replace(project / "tasks" / "TASK-001.md", "id: TASK-001", "id: TASK-002")
    assert has(hub_validate.validate_project(project), "mas o arquivo se chama")


def test_task_invalid_status(project):
    replace(project / "tasks" / "TASK-001.md", "status: todo", "status: in_progress")
    assert has(hub_validate.validate_project(project), "'status' inválido")


def test_task_project_must_match(project):
    replace(project / "tasks" / "TASK-001.md", "project: nome-do-projeto", "project: outro-projeto")
    assert has(hub_validate.validate_project(project), "'project' é 'outro-projeto'")


def test_task_dates(project):
    replace(project / "tasks" / "TASK-001.md", "updated: 2026-11-01", "updated: 2026-10-01")
    assert has(hub_validate.validate_project(project), "anterior a 'created'")


def test_task_invalid_date(project):
    replace(project / "tasks" / "TASK-001.md", "created: 2026-11-01", "created: ontem")
    assert has(hub_validate.validate_project(project), "não é uma data")


def test_started_task_requires_last_agent(project):
    task = start_task(project)
    replace(task, "last_agent: claude", "last_agent:")
    assert has(hub_validate.validate_project(project), "'last_agent'")


def test_task_unknown_decision_reference(project):
    replace(project / "tasks" / "TASK-001.md", "- `DECISIONS.md`", "- `DECISIONS.md` (D-004)")
    assert has(hub_validate.validate_project(project), "cita D-004")


def test_task_missing_handoff_section(project):
    task = project / "tasks" / "TASK-001.md"
    replace(task, "## Handoff", "## Passagem")
    assert has(hub_validate.validate_project(project), "'## Handoff'")


def test_todo_task_may_have_blank_steps(project):
    # o template tem passos em branco e status todo: válido
    assert hub_validate.validate_project(project).errors == []


# ----------------------------------------------------------------- handoff

def test_handoff_requires_three_steps(project):
    start_task(project, STARTED_HANDOFF.replace("  3. Passo três.\n", "  3.\n"))
    assert has(hub_validate.validate_project(project), "2 de 3 próximos passos")


def test_handoff_requires_files_changed(project):
    start_task(project, STARTED_HANDOFF.replace("`roteiro.md`", ""))
    assert has(hub_validate.validate_project(project), "'Arquivos alterados' vazio")


def test_handoff_requires_blockers(project):
    start_task(project, STARTED_HANDOFF.replace("**Bloqueios atuais:** nenhum", "**Bloqueios atuais:**"))
    assert has(hub_validate.validate_project(project), "'Bloqueios atuais' vazio")


def test_handoff_without_validation_is_only_a_warning(project):
    start_task(project, STARTED_HANDOFF.replace("- **Validação:** não verificado\n", ""))
    report = hub_validate.validate_project(project)
    assert report.errors == []
    assert has(report, "sem 'Validação'", level="AVISO")


def test_blockers_mixing_none_with_dependency_is_warning(project):
    # caso real do 1º teste de continuidade (Grok): "nenhum que impeça..., só X depende de D-003"
    ambiguous = STARTED_HANDOFF.replace(
        "**Bloqueios atuais:** nenhum",
        "**Bloqueios atuais:** nenhum que impeça a cena 4; só a narração depende de aprovação")
    start_task(project, ambiguous)
    report = hub_validate.validate_project(project)
    assert report.errors == []
    assert has(report, "mistura 'nenhum'", level="AVISO")


def test_blocked_task_needs_a_real_blocker(project):
    task = start_task(project)
    replace(task, "status: doing", "status: blocked")
    assert has(hub_validate.validate_project(project), "diz que não há bloqueio")


def test_english_labels_are_accepted(project):
    english = """## Handoff

- **Files changed:** `script.md`
- **Current blockers:** none
- **Next 3 steps:**
  1. One.
  2. Two.
  3. Three.
- **Validation:** not verified
"""
    start_task(project, english)
    assert hub_validate.validate_project(project).issues == []


# ------------------------------------------- coerência do registro (v0.4.1)

def test_listed_file_must_exist(project):
    start_task(project, STARTED_HANDOFF.replace("`roteiro.md`", "`roteiro-final.md`"))
    assert has(hub_validate.validate_project(project), "`roteiro-final.md`, que não existe")


def test_listed_files_without_backticks_is_warning(project):
    start_task(project, STARTED_HANDOFF.replace("`roteiro.md`", "roteiro.md"))
    report = hub_validate.validate_project(project)
    assert report.errors == []
    assert has(report, "entre crases", level="AVISO")


def test_log_must_match_last_agent(project):
    task = start_task(project)
    replace(task, "last_agent: claude", "last_agent: gemini")
    assert has(hub_validate.validate_project(project), "mas 'last_agent' é 'gemini'")


def test_log_must_match_updated(project):
    task = start_task(project)
    replace(task, "updated: 2026-11-01", "updated: 2026-11-03")
    assert has(hub_validate.validate_project(project), "mas 'updated' é 2026-11-03")


def test_log_section_required(project):
    replace(project / "tasks" / "TASK-001.md", "## Log de sessões", "## Histórico")
    assert has(hub_validate.validate_project(project), "'## Log de sessões'")


def test_log_needs_entries(project):
    replace(project / "tasks" / "TASK-001.md", "- 2026-11-01 · human · tarefa criada", "(vazio)")
    assert has(hub_validate.validate_project(project), "sem entradas")


def test_done_with_open_criteria_is_warning(project):
    task = start_task(project)
    replace(task, "status: doing", "status: done")
    report = hub_validate.validate_project(project)
    assert report.errors == []
    assert has(report, "2 critério(s) de pronto desmarcado(s)", level="AVISO")


def test_todo_with_closed_criteria_is_warning(project):
    replace(project / "tasks" / "TASK-001.md", "- [ ] Critério verificável 1", "- [x] Critério verificável 1")
    assert has(hub_validate.validate_project(project), "já marcado", level="AVISO")


# --------------------------------------------------------------------- CLI

def test_cli_exit_codes(project, capsys):
    assert hub_validate.main([str(project)]) == 0
    start_task(project, STARTED_HANDOFF.replace("- **Validação:** não verificado\n", ""))
    assert hub_validate.main([str(project)]) == 0          # só aviso
    assert hub_validate.main([str(project), "--strict"]) == 1  # aviso vira erro
    replace(project / "tasks" / "TASK-001.md", "status: doing", "status: x")
    assert hub_validate.main([str(project)]) == 1
    assert "erro(s)" in capsys.readouterr().out
