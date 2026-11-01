#!/usr/bin/env python3
"""Envia um pedido (pacote de contexto) a várias IAs pela API do OpenRouter
e grava cada resposta num arquivo. Feito para rodar no GitHub Actions, onde
há acesso à internet e a chave fica num segredo do repositório.

Uso:
    OPENROUTER_API_KEY=... python hub_ask.py rodadas/2026-11-01-x/pedido.md \
        --models rodadas/modelos.txt
    python hub_ask.py pedido.md --models modelos.txt --dry-run   # teste sem API

As respostas vão para <pasta do pedido>/respostas/<modelo>.md.
Só biblioteca padrão do Python.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELS_URL = "https://openrouter.ai/api/v1/models"
TIMEOUT = 600


def read_models(path: Path) -> list[str]:
    models = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            models.append(line)
    return models


def safe_name(model: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", model)


def post_json(url: str, payload: dict, key: str) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "X-Title": "AI HUB OS"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def available_models(provider: str) -> list[str]:
    try:
        with urllib.request.urlopen(MODELS_URL, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8")).get("data", [])
        return sorted(m["id"] for m in data if m.get("id", "").startswith(provider + "/"))
    except Exception:  # noqa: BLE001 — lista de ajuda; falhar aqui não é grave
        return []


def ask(model: str, prompt: str, key: str) -> tuple[str, dict]:
    data = post_json(API_URL, {"model": model, "messages": [{"role": "user", "content": prompt}]}, key)
    if "error" in data:
        raise RuntimeError(json.dumps(data["error"], ensure_ascii=False))
    text = data["choices"][0]["message"]["content"]
    return text, data.get("usage", {})


def header(model: str, usage: dict | None = None) -> str:
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"<!-- modelo: {model} · data: {now}"]
    if usage:
        lines.append(f"     tokens: entrada {usage.get('prompt_tokens', '?')}, saída {usage.get('completion_tokens', '?')}")
    return "\n".join(lines) + " -->\n\n"


def run(request: Path, models: list[str], dry_run: bool = False) -> int:
    prompt = request.read_text(encoding="utf-8")
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not dry_run and not key:
        print("Falta a variável OPENROUTER_API_KEY (segredo do repositório).", file=sys.stderr)
        return 2
    out_dir = request.parent / "respostas"
    out_dir.mkdir(exist_ok=True)

    ok = 0
    for model in models:
        target = out_dir / f"{safe_name(model)}.md"
        if dry_run:
            target.write_text(header(model) + f"[dry-run] resposta simulada de {model} ({len(prompt)} caracteres recebidos)\n", encoding="utf-8")
            ok += 1
            print(f"OK (simulado)  {model}")
            continue
        try:
            text, usage = ask(model, prompt, key)
            target.write_text(header(model, usage) + text.rstrip() + "\n", encoding="utf-8")
            ok += 1
            print(f"OK    {model}  {usage}")
        except (urllib.error.HTTPError, urllib.error.URLError, RuntimeError, KeyError, TimeoutError) as exc:
            detail = exc.read().decode("utf-8", "replace") if isinstance(exc, urllib.error.HTTPError) else str(exc)
            hint = available_models(model.split("/", 1)[0]) if "/" in model else []
            msg = f"ERRO ao consultar {model}:\n\n```\n{detail[:2000]}\n```\n"
            if hint:
                msg += "\nModelos disponíveis deste fornecedor (troque a linha em modelos.txt):\n\n" + "\n".join(f"- `{m}`" for m in hint[:40]) + "\n"
            (out_dir / f"{safe_name(model)}.ERRO.md").write_text(header(model) + msg, encoding="utf-8")
            print(f"ERRO  {model}: {detail[:200]}", file=sys.stderr)
    print(f"{ok} de {len(models)} respostas gravadas em {out_dir}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Envia um pedido a várias IAs via OpenRouter.")
    parser.add_argument("request", help="arquivo do pedido (ex.: rodadas/<nome>/pedido.md)")
    parser.add_argument("--models", required=True, help="arquivo com um modelo por linha")
    parser.add_argument("--dry-run", action="store_true", help="simula sem chamar a API")
    args = parser.parse_args(argv)
    return run(Path(args.request), read_models(Path(args.models)), args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
