# ADR 0003 — Estratégia MCP (próprio + externo)

| Campo | Valor |
| :--- | :--- |
| Status | Aceito |
| Data | 2026-11-22 |

## Contexto

RM4 exige servidor MCP próprio (≥2 tools sobre a camada de serviço) e pelo menos um MCP externo comprovado.

## Decisão

- **MCP próprio** via stdio, com tools que **apenas** chamam `app.service` (ex.: listar livros, emprestar, devolver) — alvo: 3 tools.  
- **MCP externo:** filesystem restrito a `docs/` e `evals/` (sem segredos no JSON de config).  
- MCP **não** importa rotas FastAPI e **não** abre SQL próprio; logs nunca em `stdout`.

## Consequências

- Mesmas RNs para HTTP e agente.  
- Evidências em testes isolados + `docs/evidencias/` na etapa MCP.  
- Implementação fica para planos 002/003 (após esta SPEC).
