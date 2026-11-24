# Handoff — doc-architect → spec-reviewer

Bônus P1. Os dois papéis já estão em `.cursor/agents/`. Este arquivo é o contrato do que um entrega ao outro. Não é rota, não altera `SPEC.md` e não chama modelo.

O arquiteto preenche o pacote e para. O revisor preenche só o veredito, no mesmo fio de PR, e também para. Magno responde. Nenhum dos dois mergeia.

## Pacote (doc-architect)

| Campo | O que leva |
| :--- | :--- |
| RM | Número do requisito ou do bônus |
| Issue | Link da issue |
| Plano | Arquivo em `docs/plans/` com decisão aceita |
| Requisito | Frase do enunciado ou da SPEC, sem regra nova |
| Critério | O que prova que o pacote está pronto |
| Teste ou arquivo | Caminho que o CI ou o leitor confere |
| Fora | O que este pacote não faz |

## Veredito (spec-reviewer)

| Campo | O que leva |
| :--- | :--- |
| Bloqueantes | Vazio, ou arquivo + motivo |
| Sugestões | O que não impede o merge |
| Resultado | `LGTM` ou `LGTM condicional` |
| Comentário | Link do `gh pr comment` |

## Exemplo já ocorrido — RM9, PR #24

Pacote escrito no plano 006 antes do merge. Veredito copiado do comentário que está no GitHub. Não é uma conversa refeita.

| Campo | Valor |
| :--- | :--- |
| RM | RM9 |
| Issue | [#23](https://github.com/magnosfranco/BiblioAPI/issues/23) |
| Plano | `docs/plans/006-threat-model-injection.md` |
| Requisito | Uma página com 7 pilares e um teste de prompt injection em `POST /recomendacoes` |
| Critério | Id inventado não sai na resposta, campo extra do modelo não vira efeito, estoque não muda |
| Teste ou arquivo | `docs/threat-model.md`, `tests/test_prompt_injection.py` |
| Fora | Tag, `ADLC-REPORT.md`, mudança de regra em `app/` |

| Campo | Valor |
| :--- | :--- |
| Bloqueantes | Nenhum |
| Sugestões | O critério de PR do plano 006 estava desmarcado. Com id válido, `motivo` ainda repete texto do modelo, cortado em 200 caracteres, e não executa ação |
| Resultado | LGTM |
| Comentário | [PR #24](https://github.com/magnosfranco/BiblioAPI/pull/24#issuecomment-7146868305) |
| Resposta humana | «Aprovado!» em 2026-11-24. Merge `1bc18b8` |
