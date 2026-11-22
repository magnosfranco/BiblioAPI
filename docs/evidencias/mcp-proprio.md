# Evidência — MCP próprio (plano 002 / RM4)

| Campo | Valor |
| :--- | :--- |
| Data | 2026-11-22 |
| Issue | [#12](https://github.com/magnosfranco/BiblioAPI/issues/12) |
| Branch | `feat/plano-002-mcp-proprio` |
| ADR | `docs/adr/0003-estrategia-mcp.md` |

## Servidor

| Item | Valor |
| :--- | :--- |
| Módulo | `mcp_server/server.py` |
| Transporte | stdio (JSON-RPC + `Content-Length`, estilo MCP) |
| Dependência | **stdlib** — sem pacote PyPI `mcp` (evita TLS/Norton no host; CI sem dep extra) |

## Tools (3)

| Tool | Delega a | RN |
| :--- | :--- | :--- |
| `listar_livros` | `app.service.listar_livros` | RN10 |
| `emprestar` | `app.service.emprestar` | RN11 |
| `devolver` | `app.service.devolver` | RN12 / RN07 |

## Invariantes comprovadas

- Sem `import sqlite3` / SQL no `mcp_server/`  
- Sem import de `app.routes` / FastAPI  
- Logs via `logging` → **stderr** apenas  
- Testes: `tests/test_mcp_proprio.py`  

## Como rodar (host MCP)

```text
python -m mcp_server.server
```

Ou apontar o cliente MCP (Inspector / Cursor) para o mesmo comando com cwd = raiz do `repo/`.
