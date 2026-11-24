# Arquitetura — BiblioAPI

O contrato está no `SPEC.md` §2 e no ADR 0001. Esta página só aponta o que já está na main.

```
HTTP (routes) ──┐
                ├──► app/service.py ──► SQLite
MCP (tools)  ───┘         │
                          └── app/ollama_client.py ──► Ollama (só em /recomendacoes)
```

- Não há `repository` nem DAO.
- `sqlite3` só em `app/db.py` e `app/service.py`.
- Rotas e o MCP próprio só chamam `app.service`. O MCP não importa FastAPI e não escreve log em stdout.
- `app/ollama_client.py` é a borda HTTP do modelo. Quem decide o fallback é `app.service.recomendar`.
- O MCP externo (`biblio-filesystem`) não entra nessa cadeia. Ele só lê `docs/` e `evals/`.
