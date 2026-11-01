import subprocess
import sys
from pathlib import Path

import pytest

import todo


def test_add_creates_sequential_ids(tmp_path):
    data = tmp_path / "todo.json"
    first = todo.add("Comprar café", data)
    second = todo.add("Ligar para o cliente", data)
    assert (first["id"], second["id"]) == (1, 2)


def test_add_persists_items(tmp_path):
    data = tmp_path / "todo.json"
    todo.add("Comprar café", data)
    assert todo.load(data) == [{"id": 1, "text": "Comprar café", "done": False}]


def test_format_list_shows_status():
    items = [{"id": 1, "text": "A", "done": False}, {"id": 2, "text": "B", "done": True}]
    assert todo.format_list(items) == "1. [ ] A\n2. [x] B"


def test_format_list_empty():
    assert todo.format_list([]) == "Nenhum item."


def test_done_persists_only_selected_item(tmp_path):
    data = tmp_path / "todo.json"
    todo.add("A", data)
    todo.add("B", data)
    todo.done(2, data)
    assert todo.load(data) == [
        {"id": 1, "text": "A", "done": False},
        {"id": 2, "text": "B", "done": True},
    ]
    assert todo.format_list(todo.load(data)) == "1. [ ] A\n2. [x] B"


def test_done_is_idempotent(tmp_path):
    data = tmp_path / "todo.json"
    todo.add("A", data)
    todo.done(1, data)
    todo.done(1, data)
    assert todo.load(data) == [{"id": 1, "text": "A", "done": True}]


def test_done_missing_id_preserves_file(tmp_path):
    data = tmp_path / "todo.json"
    todo.add("A", data)
    before = data.read_bytes()
    with pytest.raises(ValueError, match="Item não encontrado: 99"):
        todo.done(99, data)
    assert data.read_bytes() == before


def run_cli(tmp_path, *args):
    return subprocess.run(
        [sys.executable, str(Path(todo.__file__).resolve()), *args],
        cwd=tmp_path, capture_output=True, text=True,
    )


def test_cli_done_and_list(tmp_path):
    assert run_cli(tmp_path, "add", "Comprar café").returncode == 0
    result = run_cli(tmp_path, "done", "1")
    assert result.returncode == 0
    assert "Concluído: 1. Comprar café" in result.stdout
    result = run_cli(tmp_path, "list")
    assert result.returncode == 0
    assert result.stdout.strip() == "1. [x] Comprar café"


@pytest.mark.parametrize("args", [("done", "99"), ("done", "abc"), ("done",), ("done", "1", "2")])
def test_cli_invalid_done_returns_one_without_creating_data(tmp_path, args):
    result = run_cli(tmp_path, *args)
    assert result.returncode == 1
    assert result.stdout or result.stderr
    assert not (tmp_path / "todo.json").exists()
