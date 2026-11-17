# Atividades

Lista operacional do cronograma. Todas as atividades estão planejadas. O status muda quando a etapa correspondente for registrada.

## Etapa 1 — após a Aula 1

| ID | Atividade | RM | Status |
| --- | --- | --- | --- |
| A1.1 | Registrar o grupo e os papéis | — | planejada |
| A1.2 | Iniciar o repositório e o ambiente que sobe a API | — | planejada |
| A1.3 | Escrever `SPEC.md` antes de `app/` | RM1 | planejada |
| A1.4 | Escrever pelo menos 8 cenários BDD | RM1 | planejada |
| A1.5 | Escrever pelo menos 2 ADRs | RM1 | planejada |
| A1.6 | Versionar `AGENTS.md` em pelo menos 3 commits | RM2 | planejada |
| A1.7 | Ligar cada regra do agente a uma verificação | RM2 | planejada |
| A1.8 | Implementar a feature em vibe: reservas e fila | RM3 | planejada |
| A1.9 | Guardar código, métricas e conclusão da passagem vibe | RM3 | planejada |

## Etapa 2 — após a Aula 2

| ID | Atividade | RM | Status |
| --- | --- | --- | --- |
| A2.1 | Abrir issue da fatia de empréstimos e escrever o plano em `docs/plans/` antes do código | RM11 | planejada |
| A2.2 | Implementar `POST /emprestimos` e `POST /emprestimos/{id}/devolucao` a partir desse plano | RM3, RM11 | planejada |
| A2.3 | Contar empréstimos abertos em `exemplares_disponiveis` e promover a fila na devolução | RM3 | planejada |
| A2.4 | Automatizar os dois cenários de `features/emprestimos.feature` | RM1, RM3 | planejada |
| A2.5 | Publicar servidor MCP próprio com pelo menos 2 tools sobre o serviço | RM4 | planejada |
| A2.6 | Usar pelo menos 1 MCP externo, com config versionada, teste e evidência de chamada | RM4 | planejada |
| A2.7 | Fechar a trilha issue → plano → branch → PR pequeno, com `Co-Authored-By` | RM11 | planejada |
| A2.8 | Completar `docs/vibe-vs-spec/` com a coluna spec + plano | RM3 | planejada |

## Etapa 3 — após a Aula 3

| ID | Atividade | RM | Status |
| --- | --- | --- | --- |
| A3.1 | Implementar `POST /recomendacoes` com modelo e fallback determinístico | escopo | planejada |
| A3.2 | Escrever uma skill do projeto em `.agents/skills/` | RM5 | planejada |
| A3.3 | Medir o trigger com pelo menos 5 positivos e 5 negativos e publicar precisão, recall e F1 | RM5 | planejada |
| A3.4 | Instalar um hook ou uma regra de permissão e testar o bloqueio | RM6 | planejada |

## Etapa 4 — após a Aula 4

| ID | Atividade | RM | Status |
| --- | --- | --- | --- |
| A4.1 | Workflow verde com testes, cobertura de pelo menos 70%, secret scan e auditoria de dependências | RM7 | planejada |
| A4.2 | Revisão por agente em pelo menos 3 PRs, com resposta humana a cada comentário | RM8 | planejada |
| A4.3 | Escrever `docs/threat-model.md` em uma página, nos 7 pilares | RM9 | planejada |
| A4.4 | Testar prompt injection | RM9 | planejada |
| A4.5 | Montar golden set com pelo menos 10 casos e relatório com métricas e gates | RM10 | planejada |
| A4.6 | Reunir amostra de 5 PRs na trilha do RM11 | RM11 | planejada |

## Etapa 5 — antes da Aula 5

| ID | Atividade | RM | Status |
| --- | --- | --- | --- |
| A5.1 | Escrever `ADLC-REPORT.md` por fase, com custo, percentual aceito, drift e lições | RM12 | planejada |
| A5.2 | Fechar os slides da Aula 5 e ensaiar a demo em até 8 minutos | apresentação | planejada |
| A5.3 | Na demo, mostrar um guardrail bloqueando e o relatório de eval | apresentação | planejada |
| A5.4 | Criar a tag `entrega-final` até 24 horas antes da Aula 5 | entrega | planejada |
| A5.5 | Confirmar que API e testes sobem em até 5 comandos | entrega | planejada |
| A5.6 | Cada integrante percorre uma parte que não apresentou, usando o repositório como evidência | apresentação | planejada |

## Fora do caminho crítico

Bônus, só se as doze atividades obrigatórias couberem no prazo: A2A entre dois agentes, UI declarativa gerada pelo agente, comparação de duas ferramentas, LLM-as-judge calibrado com notas humanas. Cada um vale +2, com teto de +5 no conjunto.
