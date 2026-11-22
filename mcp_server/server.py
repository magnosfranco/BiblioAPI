"""Servidor MCP stdio (JSON-RPC) — 3 tools sobre app.service (plano 002 / RM4).

Implementação mínima em stdlib (sem SQL próprio; sem rotas FastAPI).
Logs apenas em stderr — stdout é o canal do protocolo.
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any, Callable

from app import service

_log = logging.getLogger("biblioapi.mcp")
if not _log.handlers:
    _handler = logging.StreamHandler(sys.stderr)
    _handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
    _log.addHandler(_handler)
    _log.setLevel(logging.INFO)

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "biblioapi", "version": "0.1.0"}


def _erro(exc: Exception, code: int) -> dict[str, Any]:
    message = getattr(exc, "message", str(exc))
    _log.info("tool error code=%s msg=%s", code, message)
    return {"ok": False, "error": message, "code": code}


def listar_livros() -> list[dict[str, Any]]:
    """Lista o catálogo com exemplares_disponiveis (RN10)."""
    return service.listar_livros()


def emprestar(socio_id: int, livro_id: int) -> dict[str, Any]:
    """Cria empréstimo para o par sócio/livro (RN11)."""
    try:
        emp = service.emprestar(int(socio_id), int(livro_id))
        return {"ok": True, "emprestimo": emp}
    except service.NotFoundError as exc:
        return _erro(exc, 404)
    except service.ConflictError as exc:
        return _erro(exc, 409)


def devolver(emprestimo_id: int) -> dict[str, Any]:
    """Devolve empréstimo por id e promove a fila (RN12/RN07)."""
    try:
        emp = service.devolver(int(emprestimo_id))
        return {"ok": True, "emprestimo": emp}
    except service.NotFoundError as exc:
        return _erro(exc, 404)
    except service.ConflictError as exc:
        return _erro(exc, 409)


ToolFn = Callable[..., Any]

TOOLS: dict[str, dict[str, Any]] = {
    "listar_livros": {
        "description": "Lista o catálogo com exemplares_disponiveis (RN10).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "handler": listar_livros,
    },
    "emprestar": {
        "description": "Cria empréstimo para o par sócio/livro (RN11).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "socio_id": {"type": "integer"},
                "livro_id": {"type": "integer"},
            },
            "required": ["socio_id", "livro_id"],
            "additionalProperties": False,
        },
        "handler": emprestar,
    },
    "devolver": {
        "description": "Devolve empréstimo por id e promove a fila (RN12/RN07).",
        "inputSchema": {
            "type": "object",
            "properties": {"emprestimo_id": {"type": "integer"}},
            "required": ["emprestimo_id"],
            "additionalProperties": False,
        },
        "handler": devolver,
    },
}


def list_tool_names() -> list[str]:
    return sorted(TOOLS.keys())


def call_tool(name: str, arguments: dict[str, Any] | None = None) -> Any:
    if name not in TOOLS:
        raise KeyError(f"tool desconhecida: {name}")
    handler: ToolFn = TOOLS[name]["handler"]
    args = arguments or {}
    return handler(**args)


def _tools_list_payload() -> list[dict[str, Any]]:
    return [
        {
            "name": name,
            "description": meta["description"],
            "inputSchema": meta["inputSchema"],
        }
        for name, meta in TOOLS.items()
    ]


def _read_message() -> dict[str, Any] | None:
    """Lê uma mensagem MCP (Content-Length) de stdin."""
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        decoded = line.decode("utf-8").strip()
        if ":" in decoded:
            key, value = decoded.split(":", 1)
            headers[key.strip().lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    body = sys.stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def _write_message(payload: dict[str, Any]) -> None:
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii"))
    sys.stdout.buffer.write(raw)
    sys.stdout.buffer.flush()


def _handle(msg: dict[str, Any]) -> dict[str, Any] | None:
    method = msg.get("method")
    req_id = msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": _tools_list_payload()},
        }

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        try:
            result = call_tool(str(name), arguments)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False),
                        }
                    ],
                    "isError": False,
                },
            }
        except Exception as exc:  # noqa: BLE001 — borda do protocolo
            _log.exception("tools/call failed")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": str(exc)}],
                    "isError": True,
                },
            }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if req_id is None:
        return None

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def main() -> None:
    _log.info("MCP biblioapi listening on stdio")
    while True:
        msg = _read_message()
        if msg is None:
            break
        response = _handle(msg)
        if response is not None:
            _write_message(response)


if __name__ == "__main__":
    main()
