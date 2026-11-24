# Plano 005 — Pendências desta fase

| Campo | Valor |
| :--- | :--- |
| Issue | [#21](https://github.com/magnosfranco/BiblioAPI/issues/21) |
| Branch sugerida | `docs/plano-005-pendencias-fase` |
| RMs | RM4, RM8, RM11 |

## Decisão humana

| Item | Status |
| :--- | :--- |
| Decisão humana: aceita | **aceita** |
| Aprovador | Magno da Silva Franco |
| Data | 2026-11-23 |

> Não há linhas pendente neste plano. O pedido foi corrigir o que a verificação desta fase deixou aberto, sem abrir a fase seguinte.

## 1. Objetivo

Fechar as provas incompletas do que já foi feito. A quinta cadeia issue → plano → branch → PR é este próprio plano.

## 2. Escopo

### Inclui

- Atualizar `docs/evidencias/revisao-agente-rm8.md`: a amostra #10, #13 e #17 tem resposta, e o RM8 continua em evolução.
- Registrar uma chamada real do `@modelcontextprotocol/server-filesystem` com roots `docs` e `evals`, e a recusa de `app/`.
- Escrever `docs/arquitetura.md` como página que aponta o contrato já existente no `SPEC.md` §2.

### Não inclui

- Threat model, teste de prompt injection, `ADLC-REPORT.md`, slides no Git.
- A skill `gerar-docs-adlc`.
- Renomear `features/` ou reabrir o PR #19 com um plano retroativo.

## 3. Critérios de aceite

- [x] Transcript da chamada em `docs/evidencias/mcp-filesystem-chamada.json`
- [x] Teste lê esse transcript e confere roots e recusa
- [x] Evidência do RM8 deixa de dizer que a resposta humana está pendente
- [x] PR com o assunto citando RM4, RM8 e RM11, e comentário do spec-reviewer — PR #22, `95967de`
