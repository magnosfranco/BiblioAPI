# ADR 0001 — Camada única de serviço + SQLite

| Campo | Valor |
| :--- | :--- |
| Status | Aceito |
| Data | 2026-11-22 |
| Contexto | BiblioAPI / escopo isonômico pequeno |

## Contexto

Precisamos de persistência simples e de um ponto único de regras de negócio compartilhado por HTTP e MCP (RM4 exige tools sobre a camada de serviço).

## Decisão

- Usar **SQLite** em arquivo (volume Docker).  
- Toda regra de negócio e SQL de domínio em **`app/service.py`**.  
- `app/db.py` apenas path, conexão e DDL (`init_schema`).  
- **Proibido** `repository`/`DAO` e `sqlite3` fora de `db.py`/`service.py`.

## Consequências

- MCP e rotas permanecem finos (só adaptação de protocolo).  
- Testes e guardrails podem verificar a fronteira `sqlite3` de forma objetiva.  
- Escala horizontal / multi-tenant fica fora de escopo (aceitável no envelope do curso).
