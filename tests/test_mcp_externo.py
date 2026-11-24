"""Plano 003 — MCP filesystem: config sem segredos e escopo docs/evals."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MCP_JSON = REPO / ".cursor" / "mcp.json"

SECRET_RE = re.compile(
    r"(\.env\b|sk-[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9\-._~+/]+)",
    re.I,
)


def test_mcp_json_exists_and_parseable() -> None:
    assert MCP_JSON.is_file(), ".cursor/mcp.json obrigatório (plano 003)"
    data = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    assert "mcpServers" in data
    servers = data["mcpServers"]
    assert "biblio-filesystem" in servers


def test_mcp_json_sem_segredos() -> None:
    raw = MCP_JSON.read_text(encoding="utf-8")
    assert SECRET_RE.search(raw) is None, "mcp.json não pode conter segredos"


def test_filesystem_roots_somente_docs_evals() -> None:
    data = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    fs = data["mcpServers"]["biblio-filesystem"]
    assert fs["command"] == "npx"
    args = fs["args"]
    assert "@modelcontextprotocol/server-filesystem" in args
    # Últimos argumentos = roots permitidos
    roots = [a.replace("\\", "/").rstrip("/") for a in args if a not in ("-y",) and not a.startswith("@")]
    # npx -y pkg docs evals → roots = docs, evals
    assert roots[-2:] == ["docs", "evals"] or set(roots[-2:]) == {"docs", "evals"}


def test_docs_e_evals_existem() -> None:
    assert (REPO / "docs").is_dir()
    assert (REPO / "evals").is_dir()
    assert (REPO / "evals" / "README.md").is_file()
    assert (REPO / "docs" / "evidencias" / "mcp-filesystem.md").is_file()


def test_mcp_proprio_ainda_no_mesmo_arquivo() -> None:
    data = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    own = data["mcpServers"]["biblioapi-service"]
    assert own["command"] == "python"
    assert "-m" in own["args"] and "mcp_server" in own["args"]


def test_chamada_real_fica_em_docs_e_evals() -> None:
    bruto = (REPO / "docs" / "evidencias" / "mcp-filesystem-chamada.json").read_text(encoding="utf-8")
    dados = json.loads(bruto)
    permitido = dados["list_allowed_directories"]["result"]["content"][0]["text"]
    assert "docs" in permitido and "evals" in permitido
    listado = dados["list_directory_docs_evidencias"]["result"]["content"][0]["text"]
    assert "mcp-filesystem.md" in listado
    fora = dados["list_directory_app_fora_do_root"]["result"]
    assert fora["isError"] is True
    assert "Access denied" in fora["content"][0]["text"]
    assert "sk-" not in bruto and "ghp_" not in bruto
