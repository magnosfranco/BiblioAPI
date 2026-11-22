# Plano 002 — MCP próprio (3 tools)

| Campo | Valor |
| :--- | :--- |
| Issue | A criar / #3 |
| Branch sugerida | `feat/plano-002-mcp-proprio` |
| SPEC / ADR | `SPEC.md` · ADR 0003 |

## Decisão humana

| Item | Status |
| :--- | :--- |
| Decisão humana: aceita | **aceita** |
| Aprovador | Magno da Silva Franco |
| Data | 2026-11-22 |

> Não há linhas `pendente` neste plano.

## 1. Objetivo

Servidor MCP próprio (stdio) com **3 tools** que apenas delegam a `app.service` (RM4).

## 2. Pré-requisitos

- API HTTP e `app/service.py` estáveis (pós-vibe + plano 001).  
- ADR 0003 aceito.

## 3. Escopo

### Inclui

- Tools sugeridas: `listar_livros`, `emprestar_livro`, `devolver_emprestimo` (nomes finais na implementação)  
- Sem SQL próprio; sem import de rotas FastAPI  
- Logs nunca em `stdout`  
- Testes isolados do MCP  

### Não inclui

- MCP filesystem externo (plano 003)  
- Novas regras de negócio

## 4. Critérios de aceite

- [ ] ≥2 tools (alvo 3) sobre a camada de serviço  
- [ ] Testes verdes sem abrir SQLite no processo MCP além do service  
- [ ] Evidência mínima em `docs/evidencias/`  
