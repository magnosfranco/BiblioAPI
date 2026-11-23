# Evidência — skill de disparo (RM5) e hook Estágio B (RM6)

| Campo | Valor |
| :--- | :--- |
| Data | 2026-11-23 |
| Skill | `.agents/skills/auditar-biblioapi/SKILL.md` (description v2) |
| Eval | `evals/skill_trigger_cases.json` — 5 positivos e 5 negativos |
| Relatório | `evals/relatorio_skill_trigger.md` |
| Hook | `scripts/guardrail_check.py` padrão `GUARDRAIL_STAGE=B` |

## RM5

A description v1 citava Docker, CI e Git, então esses pedidos disparavam a skill. Precisão 0,56, recall 1,00, F1 0,71 (4 falsos positivos).

A v2 restringe o gatilho a regra de negócio, RN, fila, empréstimo, reserva, recomendação e endpoint, e declara o que não usar. Precisão 1,00, recall 1,00, F1 1,00. O runner não chama modelo.

## RM6

O Estágio B é o padrão do hook. Editar `app/` ou `mcp_server/` exige plano com `Decisão humana: aceita` e sem célula `| pendente |`. Os planos 001–004 estão aceitos, então a edição segue liberada. Um plano pendente bloqueia: `tests/test_guardrail.py`. `GUARDRAIL_STAGE=A` ainda existe para reproduzir o comportamento da vibe. `AGENTS.md` está na v3.
