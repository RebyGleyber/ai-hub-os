import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import hub_pack  # noqa: E402

TEASER = ROOT / "examples" / "creative-teaser-cafe"


def test_pack_includes_required_reading_and_task_last():
    pack = hub_pack.build_pack(TEASER, "TASK-002")
    order = [pack.index(f"## `{name}`") for name in
             ("PROJECT.md", "DECISIONS.md", "roteiro.md", "tasks/TASK-002.md")]
    assert order == sorted(order)
    assert "Qual é a decisão aceita mais recente" in pack
    assert pack.count("## `tasks/TASK-002.md`") == 1


def test_pack_contains_full_file_contents():
    pack = hub_pack.build_pack(TEASER, "TASK-002")
    for name in ("PROJECT.md", "DECISIONS.md", "roteiro.md"):
        assert (TEASER / name).read_text(encoding="utf-8").strip() in pack


def test_pack_refuses_project_with_errors(tmp_path, capsys):
    (tmp_path / "tasks").mkdir()
    assert hub_pack.main([str(tmp_path), "TASK-001"]) == 1
    assert "Corrija os erros" in capsys.readouterr().err


def test_pack_writes_file(tmp_path):
    out = tmp_path / "pacote.md"
    assert hub_pack.main([str(TEASER), "TASK-002", "-o", str(out)]) == 0
    assert out.read_text(encoding="utf-8").startswith("# Pacote de contexto: TASK-002")
