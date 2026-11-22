# Evidência — MCP filesystem externo (plano 003 / RM4)

| Campo | Valor |
| :--- | :--- |
| Data | 2026-11-22 |
| Issue | [#14](https://github.com/magnosfranco/BiblioAPI/issues/14) |
| Branch | `feat/plano-003-mcp-filesystem` |
| Config | `.cursor/mcp.json` (sem tokens / sem `.env`) |
| Pacote | `@modelcontextprotocol/server-filesystem` |

## Escopo permitido

| Path | Motivo |
| :--- | :--- |
| `docs/` | SPEC, ADRs, planos, evidências |
| `evals/` | Golden set / evals futuros (placeholder `evals/README.md`) |

**Fora de escopo:** `app/`, `.env`, chaves, `INTERNO/` (nem está no Git do repo).

## Entrada no `mcp.json`

Servidor `biblio-filesystem`:

```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "docs", "evals"]
}
```

Também versionado no mesmo arquivo: `biblioapi-service` (`python -m mcp_server`) — MCP **próprio** (plano 002), para o agente usar os dois canais no Cursor.

## Como comprovar (humano · Cursor)

1. Abrir o workspace na pasta **`repo/`** (clone BiblioAPI).  
2. Cursor Settings → MCP → habilitar `biblio-filesystem` (aprovar na 1ª conexão).  
3. No chat agente, pedir por exemplo: *liste arquivos em docs/evidencias/*.  
4. Confirmar que tools do filesystem respondem só dentro de `docs/` / `evals/`.  
5. Tentar path fora (ex. `.env`) → deve ser recusado pelo servidor.

> **Norton / TLS:** `npx` no host pode falhar com SSL Inspection (mesmo padrão do `pip mcp`). Mitigações: cert Norton no ambiente Node, ou validar via MCP Inspector em máquina sem inspeção. A **config versionada + testes de artefato** cobrem o RM4 no Git; a aprovação no Cursor é o passo humano.

## Teste automatizado

`tests/test_mcp_externo.py` — garante JSON sem segredos, roots `docs`+`evals`, pastas existentes.

## Checklist de aceite (plano 003)

- [x] Config versionada sem segredos  
- [x] Evidência documentada (este arquivo) + teste  
- [ ] PR com merge commit (após autorização Magno)  
