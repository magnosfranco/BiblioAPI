"""Testes isolados do MCP próprio (plano 002) — sem rotas; SQL só via service."""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path

import pytest

from app import db, service
from mcp_server import server as mcp_mod

REPO = Path(__file__).resolve().parents[1]
SERVER_PY = REPO / "mcp_server" / "server.py"


@pytest.fixture()
def db_ready(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_file = tmp_path / "mcp.db"
    monkeypatch.setenv("BIBLIO_DB_PATH", str(db_file))
    os.environ["BIBLIO_DB_PATH"] = str(db_file)
    db.init_schema()


def test_mcp_source_sem_sqlite_nem_rotas() -> None:
    tree = ast.parse(SERVER_PY.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    assert "sqlite3" not in imports
    assert not any(name.startswith("app.routes") or name == "fastapi" for name in imports)
    assert "StreamHandler(sys.stderr)" in SERVER_PY.read_text(encoding="utf-8")


def test_tres_tools_registradas() -> None:
    assert mcp_mod.list_tool_names() == ["devolver", "emprestar", "listar_livros"]


def test_tools_list_jsonrpc_shape() -> None:
    resp = mcp_mod._handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}})
    assert resp is not None
    names = {t["name"] for t in resp["result"]["tools"]}
    assert names == {"listar_livros", "emprestar", "devolver"}


def test_listar_emprestar_devolver_via_tools(db_ready: None) -> None:
    socio = service.criar_socio("Ana", "ana.mcp@biblioteca.example.com")
    livro = service.criar_livro("Dom Casmurro", "Machado de Assis", 1)

    catalogo = mcp_mod.listar_livros()
    assert len(catalogo) == 1
    assert catalogo[0]["exemplares_disponiveis"] == 1

    out = mcp_mod.emprestar(int(socio["id"]), int(livro["id"]))
    assert out["ok"] is True
    emp_id = int(out["emprestimo"]["id"])
    assert out["emprestimo"]["status"] == "aberto"

    mid = mcp_mod.listar_livros()[0]
    assert mid["exemplares_disponiveis"] == 0

    conflict = mcp_mod.emprestar(int(socio["id"]), int(livro["id"]))
    assert conflict["ok"] is False
    assert conflict["code"] == 409

    call = mcp_mod._handle(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "devolver", "arguments": {"emprestimo_id": emp_id}},
        }
    )
    assert call is not None
    assert call["result"]["isError"] is False
    payload = json.loads(call["result"]["content"][0]["text"])
    assert payload["ok"] is True
    assert payload["emprestimo"]["status"] == "devolvido"
    assert mcp_mod.listar_livros()[0]["exemplares_disponiveis"] == 1


def test_emprestar_404_e_devolver_404(db_ready: None) -> None:
    assert mcp_mod.emprestar(999, 999)["code"] == 404
    assert mcp_mod.devolver(999)["code"] == 404
