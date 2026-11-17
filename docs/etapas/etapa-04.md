# Etapa 4 — após a Aula 4

Status: não iniciada.

Janela sugerida: 5 h. RMs: RM7, RM8, RM9 e RM10. A amostra de 5 PRs do RM11 também fecha aqui, se a etapa 2 ainda não a completou.

## Objetivo

Colocar a API sob CI verde, revisão de agente com resposta humana, threat model, teste de injeção e golden set da recomendação.

## Atividades

A4.1 a A4.6, em [atividades.md](../planejamento/atividades.md). Nenhuma começou.

## Critério de saída

- O workflow do commit de entrega está verde, com cobertura de pelo menos 70%, secret scan e auditoria de dependências.
- Pelo menos 3 PRs têm comentário de agente e resposta humana.
- `docs/threat-model.md` cabe em uma página e nomeia os 7 pilares.
- Existe teste de prompt injection.
- `evals/` tem pelo menos 10 casos da recomendação e um relatório com métricas e gates.
- A amostra de rastreabilidade chega a 5 PRs.

## Premissas que esta etapa não reabre

P05, P10, P11 e P14. O CI não baixa a cobertura para fazer o workflow ficar verde, e o golden set usa dados sintéticos.

Este arquivo passa a descrever o que foi feito quando a etapa fechar. A apresentação correspondente é [etapa-04.html](../apresentacao/etapa-04.html).
