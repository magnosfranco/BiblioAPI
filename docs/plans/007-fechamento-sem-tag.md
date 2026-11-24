# Plano 007 — CI v3, relatório e slides, sem a tag

| Campo | Valor |
| :--- | :--- |
| Issue | [#25](https://github.com/magnosfranco/BiblioAPI/issues/25) |
| Branch sugerida | `docs/plano-007-fechamento` |
| RMs | RM7, RM12 |

## Decisão humana

| Item | Status |
| :--- | :--- |
| Decisão humana: aceita | **aceita** |
| Aprovador | Magno da Silva Franco |
| Data | 2026-11-24 |

> A autorização foi avançar até o conteúdo final e deixar a tag para depois.

## 1. Objetivo

Versionar o que a entrega lê no repositório, sem criar a tag `entrega-final`.

## 2. Escopo

### Inclui

- CI v3: o job `test` mede `app` e `mcp_server`, com o mesmo piso de 70%.
- `ADLC-REPORT.md` com ferramenta e modelo por fase.
- `docs/apresentacao/slides.md`.
- Revalidação do filesystem em 2026-11-24 no transcript já existente.
- Marcar o critério de PR do plano 006, cumprido pelo PR #24.

### Não inclui

- A tag `entrega-final`.
- Bônus P1–P4.
- `docs/sessoes/`.
- Mudança em `app/` ou `mcp_server/`.

## 3. Critérios de aceite

- [x] `ADLC-REPORT.md` cita ferramenta e modelo de cada fase já mergeada.
- [x] O workflow declara CI v3 e inclui `--cov=mcp_server`.
- [x] Slides no Git apontam PR ou SHA de cada RM já feito.
- [ ] PR com RM7 e RM12 no assunto e comentário do spec-reviewer.
