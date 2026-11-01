"""Todo CLI: gerenciador de itens pelo terminal (projeto de exemplo do AI HUB OS)."""
import json
import sys
from pathlib import Path

DATA_FILE = Path("todo.json")


def load(path: Path = DATA_FILE) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save(items: list[dict], path: Path = DATA_FILE) -> None:
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def add(text: str, path: Path = DATA_FILE) -> dict:
    items = load(path)
    item = {"id": max((i["id"] for i in items), default=0) + 1, "text": text, "done": False}
    items.append(item)
    save(items, path)
    return item


def done(item_id: int, path: Path = DATA_FILE) -> dict:
    items = load(path)
    for item in items:
        if item["id"] == item_id:
            item["done"] = True
            save(items, path)
            return item
    raise ValueError(f"Item não encontrado: {item_id}")


def format_list(items: list[dict]) -> str:
    if not items:
        return "Nenhum item."
    return "\n".join(f"{i['id']}. [{'x' if i['done'] else ' '}] {i['text']}" for i in items)


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[0] == "add":
        item = add(" ".join(argv[1:]))
        print(f"Adicionado: {item['id']}. {item['text']}")
        return 0
    if argv == ["list"]:
        print(format_list(load()))
        return 0
    if len(argv) == 2 and argv[0] == "done":
        try:
            item_id = int(argv[1])
        except ValueError:
            print("Erro: o ID deve ser um número inteiro.", file=sys.stderr)
            return 1
        try:
            item = done(item_id)
        except ValueError as exc:
            print(f"Erro: {exc}", file=sys.stderr)
            return 1
        print(f"Concluído: {item['id']}. {item['text']}")
        return 0
    print('Uso: python todo.py add "texto" | python todo.py list | python todo.py done <id>')
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
