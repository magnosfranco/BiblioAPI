# evals/

Pasta do MCP filesystem (plano 003 / RM4) e do golden set de recomendações (plano 004 / RM10).

| Conteúdo | Quando |
| :--- | :--- |
| `golden_set_recomendacoes.json` | Plano 004 — 12 casos |
| `run_llm_eval.py` + `relatorio_recomendacoes.md` | Plano 004 — gates sem Ollama real |
| Eval de skill | Etapa da skill (ainda não) |

O servidor `@modelcontextprotocol/server-filesystem` em `.cursor/mcp.json` só pode acessar **`docs/`** e **`evals/`** — nunca `.env` nem `app/`.
