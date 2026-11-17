# Cronograma

Plano sugerido de 20 horas do `projeto.pdf`. As horas são do grupo, não um teto de esforço. A ordem é a da disciplina: cada janela depende da anterior.

| Ordem | Janela | Horas | Foco | RMs | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Após a Aula 1 | 4 h | Grupo, repositório, spec, BDD, ADRs, AGENTS.md, feature em vibe | RM1, RM2, RM3 | planejada |
| 2 | Após a Aula 2 | 5 h | API de empréstimos com spec + plano, testes, MCP próprio e MCP externo | RM4, RM11 | planejada |
| 3 | Após a Aula 3 | 4 h | Recomendação com LLM, skill com eval de trigger, hook ou permissão | RM5, RM6 | planejada |
| 4 | Após a Aula 4 | 5 h | CI, revisão por agente, threat model, teste de injeção, golden set | RM7, RM8, RM9, RM10 | planejada |
| 5 | Antes da Aula 5 | 2 h | ADLC-REPORT, slides, ensaio da demo, tag `entrega-final` | RM12 | planejada |

Soma: 20 h.

## Sequência

A etapa 1 congela o contrato e prova a ordem no Git. A etapa 2 usa esse contrato para a fatia com plano e abre a trilha issue → plano → PR. A etapa 3 acrescenta o comportamento com modelo e o guardrail. A etapa 4 coloca CI, segurança e avaliação em cima do que já roda. A etapa 5 só relata, ensaia e etiqueta. Commit depois da tag não entra na correção.

## O que a apresentação final precisa mostrar

Na Aula 5, em até 8 minutos de narrativa, a demo roda ao vivo, um guardrail bloqueia e o relatório de eval aparece. O Q&A é individual. Os slides dessa aula saem da etapa 5. As apresentações em `docs/apresentacao/` acompanham cada etapa e alimentam esse fechamento.

## Datas que o PDF fixa e este repositório ainda não numera

O PDF amarra a tag às 24 horas anteriores à Aula 5 e a proposta de domínio à Aula 2. O domínio BiblioAPI já foi escolhido neste repositório. O dia civil da Aula 5 não está no PDF. A tag só é criada quando essa data estiver confirmada.
