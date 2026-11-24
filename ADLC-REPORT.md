# ADLC-REPORT — BiblioAPI

Relatório por fase. A tag `entrega-final` ainda não existe. Os SHAs abaixo são os merges já na `main`.

Ferramenta de código em todas as fases: Cursor, com `AGENTS.md`, rules, hooks e subagentes no repositório. CI: GitHub Actions, Python 3.11, ruff, pytest, pip-audit e gitleaks.

## Fase 0 — setup

| Campo | Valor |
| :--- | :--- |
| Ferramenta | Cursor, Docker Desktop, GitHub Actions |
| Modelo de produto | nenhum |
| Prova | [PR #1](https://github.com/magnosfranco/BiblioAPI/pull/1) `a1a5829`. Certificado Norton no [PR #2](https://github.com/magnosfranco/BiblioAPI/pull/2) `42fb429` |

## Fase 1 — spec antes do código

| Campo | Valor |
| :--- | :--- |
| Ferramenta | Cursor |
| Modelo de produto | nenhum |
| Prova | [PR #3](https://github.com/magnosfranco/BiblioAPI/pull/3) `ba4e313`. SPEC, 4 ADRs e os `.feature` no commit `c5c12e5`, antes de `app/` |

## Fase 2 — vibe

| Campo | Valor |
| :--- | :--- |
| Ferramenta | Cursor, sem ler `docs/plans/` |
| Modelo de produto | nenhum |
| Métrica | cerca de 5 min, 1 retrabalho |
| Prova | [PR #6](https://github.com/magnosfranco/BiblioAPI/pull/6) `5394d4e`. Métricas nos PRs #7 e #8 |

## Fase 3 — planos e harness

| Campo | Valor |
| :--- | :--- |
| Ferramenta | Cursor. Guardrail em `scripts/guardrail_check.py` |
| Modelo de produto | nenhum |
| Prova | Planos 001–004 no PR #4. Estágio B e `AGENTS.md` v3 no [PR #19](https://github.com/magnosfranco/BiblioAPI/pull/19) `aca9b1f` |

## Fase 4 — empréstimos com plano

| Campo | Valor |
| :--- | :--- |
| Ferramenta | Cursor, plano 001, issue #9 |
| Modelo de produto | nenhum |
| Métrica | cerca de 14–16 min, 2 retrabalhos. Mais previsível que a vibe |
| Prova | [PR #10](https://github.com/magnosfranco/BiblioAPI/pull/10) `709adec`. Conclusão no [PR #11](https://github.com/magnosfranco/BiblioAPI/pull/11) `015f5db` |

## Fase 5 — MCP

| Campo | Valor |
| :--- | :--- |
| Ferramenta | Cursor. MCP próprio em stdio. Filesystem npm `@modelcontextprotocol/server-filesystem` 2.4.0 |
| Modelo de produto | nenhum |
| Prova | [PR #13](https://github.com/magnosfranco/BiblioAPI/pull/13) `dcb50d0`, [PR #15](https://github.com/magnosfranco/BiblioAPI/pull/15) `17b5e65`. Transcript no [PR #22](https://github.com/magnosfranco/BiblioAPI/pull/22) `95967de` |

## Fase 6 — LLM, skill e ameaças

| Campo | Valor |
| :--- | :--- |
| Ferramenta | Cursor + Ollama 0.40.17 no host |
| Modelo | `llama3.1:8b`. Não adotado: `qwen3.5:4b` |
| Hardware | Intel Core Ultra 7 255HX, 31,4 GB, RTX 5070 Laptop 8151 MiB |
| Métrica de produto | Ana 4,5 s, Bruno 1,1 s, Clara 1,0 s, origem `ollama`. O Qwen 3.5 no modo thinking levou 14,0 / 12,8 / 20,9 s |
| Métrica da skill | Runner sem modelo. F1 0,71 → 1,00 |
| Prova | [PR #17](https://github.com/magnosfranco/BiblioAPI/pull/17) `197f70c`, PR #19 `aca9b1f`, [PR #24](https://github.com/magnosfranco/BiblioAPI/pull/24) `1bc18b8` |

## Drift

A linha de base é `llama3.1:8b`, timeout 15 s, `format=json`, temperatura 0. O `qwen3.5:4b` com raciocínio ligado passa de 15 s no caso da Clara, então não substitui o padrão. O CI não chama o Ollama: o golden set (12/12) e o eval da skill usam código determinístico. Detalhe em `docs/evidencias/ollama-escolha-modelo.md`.

## O que esta fase não fecha

- A tag `entrega-final` espera a data da Aula 5.
- O RM8 continua em evolução: cada PR novo tem comentário e resposta.
- Com id válido, `motivo` ainda repete texto do modelo, cortado em 200 caracteres. Não executa ação. Está em `docs/threat-model.md`.
- O bônus P1 tem contrato em `docs/a2a-handoff.md`. O P2 espera uma sessão real numa segunda ferramenta. P3 e P4 não começaram.

## Lições

- A resposta humana no PR precisa ser uma segunda mensagem. A conta que publica o spec-reviewer é a mesma de Magno.
- No Windows, `npx.cmd` não entrega o stdin ao servidor MCP. A prova chama o `node` no `dist/index.js`.
- O Estágio B só edita `app/` e `mcp_server/` com plano aceito e sem célula de revisão aberta.
