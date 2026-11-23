---
name: auditar-biblioapi
description: >
  Audita conformidade das regras RN01–RN14 da BiblioAPI: fila FIFO, empréstimos,
  reservas, recomendações e camada de serviço. Use quando o pedido for revisar
  regra de negócio, invariante ou endpoint da biblioteca. Não use para Docker,
  CI, Git, certificado, formatação ou infraestrutura.
---

# Auditar BiblioAPI

Skill de auditoria de domínio (RM5). O gatilho é o campo `description` acima (versão v2). A v1, mais larga, fica arquivada em `evals/skill_trigger_cases.json`.

## Quando usar

Pedido sobre regra de negócio, RN, fila FIFO, reserva, empréstimo, recomendação, SPEC ou endpoint da biblioteca.

## Quando não usar

Docker, CI, Git, certificado Norton, formatação e infraestrutura. Esses pedidos não disparam esta skill.

## Procedimento

1. Ler `SPEC.md` (RN01–RN14) e o plano aceito em `docs/plans/`, se a mudança for em `app/` ou `mcp_server/` (Estágio B).
2. Confrontar `app/service.py` com a regra citada. Rotas e MCP só delegam.
3. Apontar o desvio com o id da RN e o teste que falta. Não inventar endpoint fora do SPEC.
4. Se for corrigir código, manter o rito de branch e PR. O hook bloqueia edição sem plano aceito.
