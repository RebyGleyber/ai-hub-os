import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import hub_ask  # noqa: E402


def test_read_models_ignores_comments_and_blank_lines(tmp_path):
    f = tmp_path / "modelos.txt"
    f.write_text("# lista\nopenai/gpt-5\n\ngoogle/gemini-2.5-pro  # auditor\n", encoding="utf-8")
    assert hub_ask.read_models(f) == ["openai/gpt-5", "google/gemini-2.5-pro"]


def test_safe_name():
    assert hub_ask.safe_name("x-ai/grok-4") == "x-ai_grok-4"


def test_dry_run_writes_one_file_per_model(tmp_path):
    req = tmp_path / "rodada" / "pedido.md"
    req.parent.mkdir()
    req.write_text("pacote de teste", encoding="utf-8")
    assert hub_ask.run(req, ["openai/gpt-5", "x-ai/grok-4"], dry_run=True) == 0
    files = sorted(p.name for p in (req.parent / "respostas").iterdir())
    assert files == ["openai_gpt-5.md", "x-ai_grok-4.md"]


def test_missing_key_fails_clearly(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    req = tmp_path / "pedido.md"
    req.write_text("x", encoding="utf-8")
    assert hub_ask.run(req, ["openai/gpt-5"]) == 2
    assert "OPENROUTER_API_KEY" in capsys.readouterr().err
