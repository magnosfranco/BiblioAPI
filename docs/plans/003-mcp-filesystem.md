# Plano 003 — MCP externo (filesystem)

| Campo | Valor |
| :--- | :--- |
| Issue | [#14](https://github.com/magnosfranco/BiblioAPI/issues/14) |
| Branch sugerida | `feat/plano-003-mcp-filesystem` |
| SPEC / ADR | ADR 0003 · RM4 externo |

## Decisão humana

| Item | Status |
| :--- | :--- |
| Decisão humana: aceita | **aceita** |
| Aprovador | Magno da Silva Franco |
| Data | 2026-11-22 |

> Não há linhas `pendente` neste plano.

## 1. Objetivo

Configurar e comprovar uso de **MCP filesystem** externo restrito a `docs/` e `evals/`, sem segredos no JSON.

## 2. Pré-requisitos

- Plano 002 concluído ou em paralelo seguro  
- Cursor: aprovar servidor MCP na 1ª conexão

## 3. Escopo

### Inclui

- `.cursor/mcp.json` (ou equivalente) sem tokens  
- Escopo de paths: `docs/`, `evals/`  
- Evidência de chamada real em `docs/evidencias/mcp-filesystem.md`  

### Não inclui

- Acesso a `.env`, chaves, ou fora de `docs/`/`evals/`

## 4. Critérios de aceite

- [x] Config versionada sem segredos — `.cursor/mcp.json`  
- [x] Evidência de chamada — `docs/evidencias/mcp-filesystem.md` + `tests/test_mcp_externo.py`  
- [ ] PR com merge commit  
