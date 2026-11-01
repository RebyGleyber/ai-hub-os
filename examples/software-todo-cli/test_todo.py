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
