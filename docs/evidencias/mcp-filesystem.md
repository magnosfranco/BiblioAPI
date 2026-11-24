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

## Chamada real (2026-11-23)

`scripts/registrar_chamada_mcp_filesystem.py` falou com `@modelcontextprotocol/server-filesystem` 2.4.0 (protocolo `2025-03-26`) e gravou `docs/evidencias/mcp-filesystem-chamada.json`.

- `list_allowed_directories` devolveu só `docs/` e `evals/`.
- `list_directory` em `docs/evidencias` listou os arquivos da pasta.
- `list_directory` em `app/` voltou `isError: true` e `Access denied - path outside allowed directories`.

O `npx` no Windows não repassa o stdin, e o registry do npm neste host exige o certificado Norton (`NODE_EXTRA_CA_CERTS`). O script chama o `node` no `dist/index.js` já baixado. O CI não executa essa chamada: `tests/test_mcp_externo.py` confere o transcript versionado.

## Revalidação (2026-11-24)

Magno ligou `biblio-filesystem` na janela aberta em `repo/`. O Cursor criou o registro `project-0-repo-biblio-filesystem` nessa janela. A sessão de estudo, aberta na pasta pai, não recebeu as tools, e não havia processo `node.exe` no momento da checagem. A configuração foi reexecutada no mesmo dia: `list_allowed_directories` devolveu só `docs` e `evals`, e `list_directory` em `app/` voltou `Access denied`. O transcript foi atualizado.

## Como comprovar no Cursor

1. Abrir a janela na pasta **`repo/`**.  
2. Customize → MCPs → ligar `biblio-filesystem` (aprovar na 1ª conexão).  
3. Pedir a listagem de `docs/evidencias`. O servidor só responde dentro de `docs/` e `evals/`.

> **Norton / TLS:** `npx` no host pode falhar com SSL Inspection (mesmo padrão do `pip mcp`). Mitigações: cert Norton no ambiente Node, ou validar via MCP Inspector em máquina sem inspeção. A **config versionada + testes de artefato** cobrem o RM4 no Git; a aprovação no Cursor é o passo humano.

## Teste automatizado

`tests/test_mcp_externo.py` — garante JSON sem segredos, roots `docs`+`evals`, pastas existentes.

## Checklist de aceite (plano 003)

- [x] Config versionada sem segredos  
- [x] Evidência documentada (este arquivo) + teste  
- [x] PR #15 mergeado (`17b5e65`)  
- [x] Chamada real gravada em `mcp-filesystem-chamada.json`  
