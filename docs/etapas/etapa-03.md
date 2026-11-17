# Etapa 3 — após a Aula 3

Status: não iniciada.

Janela sugerida: 4 h. RMs: RM5 e RM6.

## Objetivo

Entregar a recomendação com modelo e fallback determinístico, uma skill com eval de trigger e um guardrail que um teste prova bloquear.

## Atividades

A3.1 a A3.4, em [atividades.md](../planejamento/atividades.md). Nenhuma começou.

## Critério de saída

- `POST /recomendacoes` responde com o modelo e, na falha do modelo, com o fallback determinístico descrito na spec da própria etapa.
- `.agents/skills/` tem uma skill com `SKILL.md`.
- O eval de trigger tem pelo menos 5 positivos e 5 negativos, com precisão, recall e F1.
- Um hook ou uma regra de permissão bloqueia a ação prevista, e um teste falha se o bloqueio sumir.

## Premissas que esta etapa não reabre

P02, P19 e P26. A recomendação é a única funcionalidade com LLM. O contrato fino dela é escrito na spec antes do código da rota.

Este arquivo passa a descrever o que foi feito quando a etapa fechar. A apresentação correspondente é [etapa-03.html](../apresentacao/etapa-03.html).
