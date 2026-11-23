# Plano 004 — Recomendações (Ollama + fallback)

| Campo | Valor |
| :--- | :--- |
| Issue | [#16](https://github.com/magnosfranco/BiblioAPI/issues/16) |
| Branch sugerida | `feat/plano-004-recomendacoes` |
| SPEC / ADR | RN13–RN14 · ADR 0004 · RM10 |

## Decisão humana

| Item | Status |
| :--- | :--- |
| Decisão humana: aceita | **aceita** |
| Aprovador | Magno da Silva Franco |
| Data | 2026-11-22 |

> Não há linhas `pendente` neste plano.

## 1. Objetivo

Implementar `POST /recomendacoes` com Ollama local e fallback determinístico; golden set ≥10 com gates (RM10).

## 2. Pré-requisitos

- Catálogo e empréstimos operacionais (histórico para popularidade)  
- Ollama no host; ADR 0004  

## 3. Escopo

### Inclui

- Cliente Ollama (`format=json`, timeout curto)  
- Fallback por popularidade (RN14) e campo `origem`  
- `evals/golden_set_recomendacoes.json` + runner com gates  
- Testes com mock de Ollama no CI (não depender de modelo no runner)  

### Não inclui

- Skill `auditar-biblioapi` (pode ser PR irmã na Etapa 6)  
- Threat model completo (RM9 — PR dedicada)

## 4. Critérios de aceite

- [x] Endpoint conforme SPEC — `POST /recomendacoes`  
- [x] Fallback coberto por teste — `tests/test_recomendacoes_bdd.py`  
- [x] Golden set ≥10 + relatório — `evals/golden_set_recomendacoes.json` (12) e `evals/relatorio_recomendacoes.md`  
- [x] CI verde sem Ollama no runner — PR #17, checks `test` e `gitleaks`  
