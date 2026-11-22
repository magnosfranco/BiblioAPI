# evals/

Pasta reservada ao **MCP filesystem** (plano 003 / RM4) e, depois, ao golden set LLM (plano 004 / RM10).

| Conteúdo futuro | Quando |
| :--- | :--- |
| `golden_set_recomendacoes.json` | Plano 004 |
| Scripts de eval | Etapa LLM |

O servidor `@modelcontextprotocol/server-filesystem` em `.cursor/mcp.json` só pode acessar **`docs/`** e **`evals/`** — nunca `.env` nem `app/`.
