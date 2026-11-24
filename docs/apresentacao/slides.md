# Slides — BiblioAPI

Narrativa versionada. O deck de estudo fica em `INTERNO/` e não entra no Git. A tag `entrega-final` ainda não existe.

## Capa

API de biblioteca. Sócios, livros, reservas FIFO, empréstimos e recomendações. Camada única `app/service.py`. Main após o PR #24: `1bc18b8`.

## RM1 — spec antes do código

`SPEC.md`, features e ADRs 0001–0004 no commit `c5c12e5`, sem `app/`. Merge: PR #3 `ba4e313`.

## RM2 — AGENTS.md

v1 no PR #1, v2 no PR #3, v3 no PR #19 `aca9b1f`. Quatro commits no arquivo.

## RM3 — vibe × spec

Vibe: PR #6 `5394d4e`, cerca de 5 min, 1 retrabalho. Spec+Plano: PR #10 `709adec`, cerca de 14–16 min, 2 retrabalhos. Conclusão: PR #11 `015f5db`. Mais previsível: Spec+Plano.

## RM4 — MCP

Próprio: PR #13 `dcb50d0`, três tools em `app.service`. Externo: PR #15 `17b5e65`, roots `docs` e `evals`. Chamada real: PR #22 `95967de`. `app/` responde `Access denied`.

## RM5 — skill

`auditar-biblioapi`. Runner sem modelo. F1 0,71 → 1,00. PR #19.

## RM6 — guardrail

`.cursor/hooks.json` chama `scripts/guardrail_check.py`. Padrão: Estágio B. PR #19.

## RM7 — CI

Jobs `test` e `gitleaks`. A v3 mede `app` e `mcp_server`, piso 70%, e já executa o teste de injection. A prova da rubrica no SHA da tag ainda não existe.

## RM8 — revisão

Comentário `spec-reviewer (RM8)` e resposta de Magno nos PRs #10, #13, #17, #20, #22 e #24. O requisito não se encerra.

## RM9 — ameaças

`docs/threat-model.md` e `tests/test_prompt_injection.py`. PR #24 `1bc18b8`.

## RM10 — golden set

12/12 em `evals/relatorio_recomendacoes.md`. Modelo `llama3.1:8b`. PR #17 e PR #19.

## RM11 — rastreio

Cadeias com plano: #10, #13, #15, #17, #22 e #24. O PR #19 tem issue e não tem plano. Ficou fora da amostra mínima.

## RM12 — este relatório

`ADLC-REPORT.md` lista ferramenta e modelo por fase. A tag fica para a data da Aula 5.

## Demo

README, cinco comandos: `docker compose build`, `docker compose run --rm api pytest -q`, `docker compose up -d api`, `curl -s http://localhost:8000/saude`, `docker compose down`. No ao vivo: guardrail negando e o relatório de eval.
