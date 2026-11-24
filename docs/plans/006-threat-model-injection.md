# Plano 006 — Threat model e prompt injection

| Campo | Valor |
| :--- | :--- |
| Issue | [#23](https://github.com/magnosfranco/BiblioAPI/issues/23) |
| Branch sugerida | `docs/plano-006-ameacas` |
| RMs | RM9 |

## Decisão humana

| Item | Status |
| :--- | :--- |
| Decisão humana: aceita | **aceita** |
| Aprovador | Magno da Silva Franco |
| Data | 2026-11-24 |

> Não há linha de revisão em aberto neste plano. A autorização foi avançar para a Aula 4.

## 1. Objetivo

Registrar os 7 pilares em uma página e provar, com teste, que um título malicioso em `POST /recomendacoes` não inventa `livro_id`, não vaza um system prompt e não cria empréstimo.

## 2. Escopo

### Inclui

- `docs/threat-model.md`, uma página.
- `tests/test_prompt_injection.py`, com o Ollama substituído. O CI não chama a rede.
- Marcar o último critério do plano 005, já cumprido pelo PR #22.

### Não inclui

- Mudança de regra em `app/` ou `mcp_server/`.
- `ADLC-REPORT.md`, slides no Git, tag `entrega-final`, cobertura de `mcp_server` no CI e bônus.

## 3. Critérios de aceite

- [x] A página nomeia spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege e abuso de LLM.
- [x] O teste recusa o `livro_id` inventado, não devolve campo extra do modelo e não altera o estoque.
- [ ] PR com RM9 no assunto e comentário do spec-reviewer.
