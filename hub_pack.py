#!/usr/bin/env python3
"""Monta o pacote de contexto de uma tarefa para colar em qualquer IA.

Uso:
    python hub_pack.py CAMINHO_DO_PROJETO TASK-002 [-o pacote.md]

O pacote traz as instruções de retomada e, na íntegra: PROJECT.md,
DECISIONS.md, os arquivos citados em "Leitura obrigatória" e a tarefa.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import hub_validate

PROMPT = """# Pacote de contexto: {task_id} ({project_id})

Você vai continuar a tarefa {task_id} seguindo as regras do PROJECT.md abaixo.
Todos os arquivos de que você precisa estão neste pacote; não tente abrir links.

Antes de trabalhar, responda só com os arquivos:
1. Qual é o objetivo da tarefa?
2. Qual é a decisão aceita mais recente que afeta a tarefa?
3. Qual é o próximo passo?
4. O que está bloqueado?
5. Quais arquivos a última sessão desta tarefa alterou? (tarefa ainda não iniciada: "nenhum")

Depois, execute a tarefa. Ao terminar, atualize {task_path}
(updated, last_agent, Estado atual, Handoff e uma linha no Log) e devolva
cada arquivo alterado ou criado completo, num bloco de código com o caminho
(relativo à raiz do projeto) na primeira linha.

---
"""


def required_reading(task_body: str) -> list[str]:
    section = hub_validate.find_section(task_body, ("leitura obrigatória", "leitura obrigatoria", "required reading"))
    if section is None:
        return []
    paths: list[str] = []
    for line in section.splitlines():
        paths.extend(hub_validate.BACKTICK_RE.findall(line))
    return paths


def build_pack(root: Path, task_id: str) -> str:
    task_path = root / "tasks" / f"{task_id}.md"
    if not task_path.is_file():
        raise FileNotFoundError(f"tarefa não encontrada: {task_path}")

    meta, body, err = hub_validate.split_front_matter(task_path.read_text(encoding="utf-8"))
    if err:
        raise ValueError(f"tasks/{task_id}.md: {err}")

    files = ["PROJECT.md", "DECISIONS.md"]
    for rel in required_reading(body):
        if rel not in files and (root / rel).is_file():
            files.append(rel)
    task_rel = f"tasks/{task_id}.md"
    if task_rel in files:
        files.remove(task_rel)
    files.append(task_rel)  # a tarefa sempre por último

    project_meta, _, _ = hub_validate.split_front_matter((root / "PROJECT.md").read_text(encoding="utf-8"))
    project_id = (project_meta or {}).get("id", root.name)

    parts = [PROMPT.format(task_id=task_id, project_id=project_id, task_path=task_rel)]
    for rel in files:
        content = (root / rel).read_text(encoding="utf-8").rstrip("\n")
        lang = {".py": "python", ".yaml": "yaml", ".yml": "yaml", ".json": "json"}.get(Path(rel).suffix, "markdown")
        parts.append(f"\n## `{rel}`\n\n````{lang}\n{content}\n````\n")
    return "".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Monta o pacote de contexto de uma tarefa.")
    parser.add_argument("project", help="pasta do projeto")
    parser.add_argument("task", help="ID da tarefa, ex.: TASK-002")
    parser.add_argument("-o", "--output", help="arquivo de saída (padrão: imprime na tela)")
    args = parser.parse_args(argv)

    report = hub_validate.validate_project(args.project)
    if report.errors:
        for issue in report.errors:
            print(issue, file=sys.stderr)
        print("Corrija os erros acima antes de montar o pacote.", file=sys.stderr)
        return 1

    pack = build_pack(Path(args.project), args.task)
    if args.output:
        Path(args.output).write_text(pack, encoding="utf-8")
        print(f"Pacote salvo em {args.output} ({len(pack)} caracteres)")
    else:
        print(pack)
    return 0


if __name__ == "__main__":
    sys.exit(main())
