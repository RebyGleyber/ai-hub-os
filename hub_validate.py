#!/usr/bin/env python3
"""Validador do AI HUB Protocol v0.4.

Uso:
    python hub_validate.py CAMINHO_DO_PROJETO [OUTRO_PROJETO ...] [--strict]

Sai com código 1 se houver erros (ou avisos, com --strict).
Única dependência: PyYAML.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML não está instalado. Rode: pip install pyyaml")

PROTOCOL_VERSION = "ai-hub v0.4"

PROJECT_TYPES = {
    "software", "business", "research", "marketing",
    "education", "creative", "personal", "other",
}
PROJECT_STATUS = {"active", "paused", "done"}
SENSITIVITY = {"normal", "high"}
TASK_STATUS = {"todo", "doing", "review", "done", "blocked"}
DECISION_STATUS = {"proposed", "accepted", "superseded"}

PROJECT_REQUIRED = ["id", "name", "type", "owner", "status", "protocol"]
TASK_REQUIRED = ["id", "project", "title", "status", "owner", "created", "updated"]

SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TASK_ID_RE = re.compile(r"^TASK-\d{3,}$")
TASK_FILE_RE = re.compile(r"^TASK-\d{3,}\.md$")
DECISION_HEADING_RE = re.compile(r"^##\s+(D-\d{3,})\s*:\s*(.*)$", re.MULTILINE)
DECISION_REF_RE = re.compile(r"\bD-\d{3,}\b")
FIELD_RE = re.compile(r"^\s*[-*]\s*\*\*(.+?):\*\*\s*(.*)$")
NUMBERED_RE = re.compile(r"^\s*\d+[.)]\s*(.*)$")

EMPTY_VALUES = {"", "-", "—", "–"}
NONE_VALUES = {"nenhum", "nenhuma", "none", "n/a"}

# Rótulos aceitos (português e inglês), comparados pelo início do texto.
HANDOFF_LABELS = {
    "files": ("arquivos alterados", "files changed"),
    "blockers": ("bloqueios", "current blockers", "blockers"),
    "next": ("próximos", "proximos", "next"),
    "validation": ("validação", "validacao", "validation"),
}
SECTION_ALIASES = {
    "objective": ("objetivo", "goal", "objective"),
    "state": ("estado atual", "current state"),
    "handoff": ("handoff",),
}
PROJECT_RULES_ALIASES = ("regras para qualquer ia", "rules for any ai")


@dataclass
class Issue:
    level: str  # "ERRO" ou "AVISO"
    file: str
    message: str

    def __str__(self) -> str:
        return f"  {self.level:<5}  {self.file}: {self.message}"


class Report:
    def __init__(self) -> None:
        self.issues: list[Issue] = []

    def error(self, file: str, message: str) -> None:
        self.issues.append(Issue("ERRO", file, message))

    def warn(self, file: str, message: str) -> None:
        self.issues.append(Issue("AVISO", file, message))

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "ERRO"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "AVISO"]


# ---------------------------------------------------------------- utilidades

def split_front_matter(text: str) -> tuple[dict | None, str, str | None]:
    """Separa o bloco YAML do topo e o corpo. Retorna (metadados, corpo, erro)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, "sem metadados YAML no topo (bloco entre linhas ---)"
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            raw = "\n".join(lines[1:idx])
            body = "\n".join(lines[idx + 1:])
            try:
                meta = yaml.safe_load(raw) or {}
            except yaml.YAMLError as exc:
                return None, body, f"YAML inválido nos metadados: {exc}"
            if not isinstance(meta, dict):
                return None, body, "os metadados YAML precisam ser pares chave: valor"
            return meta, body, None
    return None, text, "bloco de metadados YAML não foi fechado com ---"


def as_date(value) -> dt.date | None:
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def is_empty(value) -> bool:
    return value is None or str(value).strip() in EMPTY_VALUES


def find_section(body: str, aliases: tuple[str, ...]) -> str | None:
    """Retorna o texto de uma seção '## Título' (até a próxima '## ')."""
    lines = body.splitlines()
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("## "):
            title = line[3:].strip().casefold()
            if start is not None:
                return "\n".join(lines[start:idx])
            if title.startswith(aliases):
                start = idx + 1
    if start is not None:
        return "\n".join(lines[start:])
    return None


def label_key(label: str, table: dict[str, tuple[str, ...]]) -> str | None:
    norm = label.strip().casefold()
    for key, prefixes in table.items():
        if norm.startswith(prefixes):
            return key
    return None


def parse_handoff(section: str) -> dict:
    """Extrai os itens do handoff: valores dos rótulos e passos numerados."""
    values: dict[str, str] = {}
    steps: list[str] = []
    current = None
    for line in section.splitlines():
        field = FIELD_RE.match(line)
        if field:
            current = label_key(field.group(1), HANDOFF_LABELS)
            if current:
                values[current] = field.group(2).strip()
            continue
        numbered = NUMBERED_RE.match(line)
        if numbered and current == "next":
            steps.append(numbered.group(1).strip())
    return {"values": values, "steps": steps}


# ------------------------------------------------------------- validações

def validate_project_file(root: Path, report: Report) -> str | None:
    name = "PROJECT.md"
    path = root / name
    if not path.is_file():
        report.error(name, "arquivo obrigatório não encontrado")
        return None
    meta, body, err = split_front_matter(path.read_text(encoding="utf-8"))
    if err:
        report.error(name, err)
        return None

    for field in PROJECT_REQUIRED:
        if is_empty(meta.get(field)):
            report.error(name, f"campo obrigatório ausente ou vazio: '{field}'")

    project_id = meta.get("id")
    if not is_empty(project_id) and not SLUG_RE.match(str(project_id)):
        report.error(name, f"'id' inválido: '{project_id}' (use minúsculas, números e hífens)")

    checks = (("type", PROJECT_TYPES), ("status", PROJECT_STATUS), ("sensitivity", SENSITIVITY))
    for field, allowed in checks:
        value = meta.get(field)
        if not is_empty(value) and str(value) not in allowed:
            report.error(name, f"'{field}' inválido: '{value}' (use: {', '.join(sorted(allowed))})")

    protocol = meta.get("protocol")
    if not is_empty(protocol) and str(protocol).strip() != PROTOCOL_VERSION:
        report.warn(name, f"'protocol' é '{protocol}'; este validador verifica '{PROTOCOL_VERSION}'")

    if "reviewed_at" in meta and not is_empty(meta["reviewed_at"]) and as_date(meta["reviewed_at"]) is None:
        report.error(name, f"'reviewed_at' não é uma data AAAA-MM-DD: '{meta['reviewed_at']}'")

    if find_section(body, PROJECT_RULES_ALIASES) is None:
        report.warn(name, "seção '## Regras para qualquer IA' não encontrada")

    return None if is_empty(project_id) else str(project_id)


def validate_decisions_file(root: Path, report: Report) -> dict[str, str]:
    """Valida DECISIONS.md e retorna {id: status}."""
    name = "DECISIONS.md"
    path = root / name
    if not path.is_file():
        report.error(name, "arquivo obrigatório não encontrado")
        return {}
    text = path.read_text(encoding="utf-8")
    headings = list(DECISION_HEADING_RE.finditer(text))

    decisions: dict[str, dict] = {}
    previous_number = 0
    for idx, match in enumerate(headings):
        dec_id = match.group(1)
        end = headings[idx + 1].start() if idx + 1 < len(headings) else len(text)
        block = text[match.end():end]
        fields = {}
        for line in block.splitlines():
            field = FIELD_RE.match(line)
            if field:
                fields[field.group(1).strip().casefold()] = field.group(2).strip()

        if dec_id in decisions:
            report.error(name, f"ID de decisão repetido: {dec_id}")
            continue
        number = int(dec_id.split("-")[1])
        if number <= previous_number:
            report.error(name, f"{dec_id} fora de ordem crescente")
        previous_number = max(previous_number, number)

        status = fields.get("status", "")
        if is_empty(status):
            report.error(name, f"{dec_id} sem 'Status'")
        elif status not in DECISION_STATUS:
            report.error(name, f"{dec_id} com status inválido: '{status}' (use: {', '.join(sorted(DECISION_STATUS))})")

        date_value = fields.get("data", fields.get("date", ""))
        if is_empty(date_value):
            report.warn(name, f"{dec_id} sem 'Data'")
        elif as_date(date_value) is None:
            report.error(name, f"{dec_id} com data inválida: '{date_value}'")

        if is_empty(match.group(2)):
            report.warn(name, f"{dec_id} sem título")

        replaces = fields.get("substitui", fields.get("supersedes", ""))
        decisions[dec_id] = {"status": status, "replaces": DECISION_REF_RE.findall(replaces)}

    for dec_id, info in decisions.items():
        for target in info["replaces"]:
            if target == dec_id:
                report.error(name, f"{dec_id} não pode substituir a si mesma")
            elif target not in decisions:
                report.error(name, f"{dec_id} substitui {target}, que não existe")
            elif info["status"] == "accepted" and decisions[target]["status"] != "superseded":
                report.error(name, f"{dec_id} substitui {target}, mas {target} não está como 'superseded'")

    return {dec_id: info["status"] for dec_id, info in decisions.items()}


def validate_task_file(path: Path, project_id: str | None, decisions: dict[str, str], report: Report) -> None:
    name = f"tasks/{path.name}"
    meta, body, err = split_front_matter(path.read_text(encoding="utf-8"))
    if err:
        report.error(name, err)
        return

    for field in TASK_REQUIRED:
        if is_empty(meta.get(field)):
            report.error(name, f"campo obrigatório ausente ou vazio: '{field}'")

    task_id = meta.get("id")
    if not is_empty(task_id):
        if not TASK_ID_RE.match(str(task_id)):
            report.error(name, f"'id' inválido: '{task_id}' (use TASK-001)")
        elif str(task_id) != path.stem:
            report.error(name, f"'id' é '{task_id}', mas o arquivo se chama {path.name}")

    if project_id and not is_empty(meta.get("project")) and str(meta["project"]) != project_id:
        report.error(name, f"'project' é '{meta['project']}', mas o PROJECT.md tem id '{project_id}'")

    status = meta.get("status")
    status = None if is_empty(status) else str(status)
    if status and status not in TASK_STATUS:
        report.error(name, f"'status' inválido: '{status}' (use: {', '.join(sorted(TASK_STATUS))})")

    created, updated = meta.get("created"), meta.get("updated")
    created_d, updated_d = as_date(created), as_date(updated)
    if not is_empty(created) and created_d is None:
        report.error(name, f"'created' não é uma data AAAA-MM-DD: '{created}'")
    if not is_empty(updated) and updated_d is None:
        report.error(name, f"'updated' não é uma data AAAA-MM-DD: '{updated}'")
    if created_d and updated_d and updated_d < created_d:
        report.error(name, "'updated' é anterior a 'created'")

    if status and status != "todo" and is_empty(meta.get("last_agent")):
        report.error(name, "'last_agent' é obrigatório quando a tarefa já começou")

    for key in ("objective", "state"):
        if find_section(body, SECTION_ALIASES[key]) is None:
            label = "## Objetivo" if key == "objective" else "## Estado atual"
            report.error(name, f"seção '{label}' não encontrada")

    for ref in sorted(set(DECISION_REF_RE.findall(body))):
        if ref not in decisions:
            report.error(name, f"cita {ref}, que não existe em DECISIONS.md")

    handoff_text = find_section(body, SECTION_ALIASES["handoff"])
    if handoff_text is None:
        report.error(name, "seção '## Handoff' não encontrada")
        return
    if status in (None, "todo"):
        return  # tarefa não iniciada: handoff ainda pode estar em branco

    handoff = parse_handoff(handoff_text)
    values, steps = handoff["values"], handoff["steps"]

    if is_empty(values.get("files")):
        report.error(name, "handoff incompleto: 'Arquivos alterados' vazio (use 'nenhum' se for o caso)")
    if is_empty(values.get("blockers")):
        report.error(name, "handoff incompleto: 'Bloqueios atuais' vazio (use 'nenhum' se for o caso)")
    filled_steps = [s for s in steps if s]
    if "next" not in values:
        report.error(name, "handoff incompleto: item 'Próximos 3 passos' não encontrado")
    elif len(filled_steps) < 3:
        report.error(name, f"handoff incompleto: {len(filled_steps)} de 3 próximos passos preenchidos")
    if is_empty(values.get("validation")):
        report.warn(name, "handoff sem 'Validação' (recomendado: o que foi verificado e como, ou 'não verificado')")

    if status == "blocked" and str(values.get("blockers", "")).strip().casefold() in NONE_VALUES:
        report.error(name, "status 'blocked', mas 'Bloqueios atuais' diz que não há bloqueio")


def validate_project(root: Path | str) -> Report:
    root = Path(root)
    report = Report()
    if not root.is_dir():
        report.error(str(root), "pasta do projeto não encontrada")
        return report

    project_id = validate_project_file(root, report)
    decisions = validate_decisions_file(root, report)

    tasks_dir = root / "tasks"
    if not tasks_dir.is_dir():
        report.error("tasks/", "pasta obrigatória não encontrada")
        return report
    task_files = sorted(p for p in tasks_dir.iterdir() if p.is_file() and TASK_FILE_RE.match(p.name))
    for other in sorted(p for p in tasks_dir.iterdir() if p.is_file() and not TASK_FILE_RE.match(p.name)):
        report.warn(f"tasks/{other.name}", "nome fora do padrão TASK-NNN.md; arquivo ignorado")
    if not task_files:
        report.error("tasks/", "nenhuma tarefa encontrada (esperado: tasks/TASK-001.md)")
    for task in task_files:
        validate_task_file(task, project_id, decisions, report)
    return report


# --------------------------------------------------------------------- CLI

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Valida projetos no formato AI HUB Protocol v0.4.")
    parser.add_argument("projects", nargs="+", help="pasta(s) de projeto")
    parser.add_argument("--strict", action="store_true", help="trata avisos como erros")
    args = parser.parse_args(argv)

    total_errors = total_warnings = 0
    for project in args.projects:
        report = validate_project(project)
        print(f"[projeto] {project}")
        if not report.issues:
            print("  OK")
        for issue in report.issues:
            print(issue)
        total_errors += len(report.errors)
        total_warnings += len(report.warnings)

    print(f"\nResultado: {total_errors} erro(s), {total_warnings} aviso(s)")
    failed = total_errors > 0 or (args.strict and total_warnings > 0)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
