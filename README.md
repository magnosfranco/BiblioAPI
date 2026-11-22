# BiblioAPI

API HTTP de biblioteca comunitária (sócios, catálogo, reservas FIFO, empréstimos e recomendações com LLM local), construída com ADLC no Cursor.

## Pré-requisitos

- Docker Desktop + Docker Compose
- (Host Windows deste grupo) certificado raiz do Norton em `docker/certs/*.crt` **antes** do `docker compose build`
- Ollama local opcional em `http://localhost:11434` (recomendação com fallback)

## Subir e testar (≤ 5 comandos)

```bash
docker compose build
docker compose run --rm api pytest -q
docker compose up -d api
curl -s http://localhost:8000/saude
docker compose down
```

Documentação interativa (quando a API estiver no ar): `http://localhost:8000/docs`.

## Estrutura (visão)

| Caminho | Papel |
| :--- | :--- |
| `AGENTS.md` | Regras do agente (fonte canônica) |
| `CLAUDE.md` | Ponte para `AGENTS.md` |
| `scripts/guardrail_check.py` | Guardrail determinístico (Estágio A no setup) |
| `app/` | API (criada após SPEC — Gate G2) |
| `docs/` | PRD, ADRs, planos, vibe-vs-spec |
| `mcp_server/` | MCP próprio sobre a camada de serviço |
| `evals/` | Golden set e evals de skill |

## Arquitetura (resumo)

Rotas HTTP e tools MCP delegam para uma **camada única de serviço** (`app/service.py`) sobre SQLite. Uso de `sqlite3` apenas em `app/db.py` e `app/service.py`.
