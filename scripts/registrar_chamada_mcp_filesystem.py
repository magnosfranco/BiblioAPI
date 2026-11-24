"""Uma chamada real ao MCP filesystem externo. Grava o transcript em docs/evidencias.

O servidor 2.x fala JSON por linha, não Content-Length. No Windows o npx.cmd
não repassa stdin, então o script procura o dist/index.js já baixado e chama
o node direto. Não entra no CI.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAIDA = ROOT / "docs" / "evidencias" / "mcp-filesystem-chamada.json"


def _entrada() -> list[str]:
    node = shutil.which("node")
    if node is None:
        raise SystemExit("node não está no PATH")
    override = os.environ.get("MCP_FILESYSTEM_ENTRY")
    if override:
        return [node, override, "docs", "evals"]
    candidatos = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "npm-cache" / "_npx",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Temp" / "cursor-sandbox-cache",
    ]
    for base in candidatos:
        if not base.is_dir():
            continue
        for package in base.rglob("package.json"):
            if package.parent.name != "server-filesystem":
                continue
            entry = package.parent / "dist" / "index.js"
            if entry.is_file():
                return [node, str(entry), "docs", "evals"]
    raise SystemExit(
        "Pacote @modelcontextprotocol/server-filesystem não encontrado. "
        "Rode uma vez: npx -y @modelcontextprotocol/server-filesystem docs evals"
    )


def _enviar(proc: subprocess.Popen[bytes], mensagem: dict) -> None:
    assert proc.stdin is not None
    proc.stdin.write((json.dumps(mensagem) + "\n").encode("utf-8"))
    proc.stdin.flush()


def _ler(proc: subprocess.Popen[bytes]) -> dict:
    assert proc.stdout is not None
    linha = proc.stdout.readline()
    if not linha:
        raise RuntimeError("o servidor MCP fechou a saída")
    return json.loads(linha.decode("utf-8"))


def _chamar(proc: subprocess.Popen[bytes], req_id: int, nome: str, argumentos: dict) -> dict:
    _enviar(
        proc,
        {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": "tools/call",
            "params": {"name": nome, "arguments": argumentos},
        },
    )
    return _ler(proc)


def main() -> None:
    proc = subprocess.Popen(
        _entrada(),
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    try:
        _enviar(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "biblioapi-evidencia", "version": "1"},
                },
            },
        )
        init = _ler(proc)
        _enviar(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})
        permitidos = _chamar(proc, 2, "list_allowed_directories", {})
        lista = _chamar(proc, 3, "list_directory", {"path": str(ROOT / "docs" / "evidencias")})
        fora = _chamar(proc, 4, "list_directory", {"path": str(ROOT / "app")})
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.kill()
        proc.wait(timeout=10)

    transcript = {
        "servidor": "@modelcontextprotocol/server-filesystem",
        "versao_protocolo": "2025-03-26",
        "roots_na_linha_de_comando": ["docs", "evals"],
        "initialize": init,
        "list_allowed_directories": permitidos,
        "list_directory_docs_evidencias": lista,
        "list_directory_app_fora_do_root": fora,
    }
    SAIDA.write_text(json.dumps(transcript, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(SAIDA)


if __name__ == "__main__":
    main()
