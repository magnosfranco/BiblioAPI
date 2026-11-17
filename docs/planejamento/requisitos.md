# Requisitos mínimos

Cada RM abaixo é o recorte do `projeto.pdf`. Falhar um RM zera o critério da rubrica ligado a ele. RM6 e RM7 entram em dois critérios.

Cada requisito abaixo está planejado. O status passa a registrar execução só quando a etapa for fechada.

## RM1 — Spec, BDD e ADRs antes do código

Escrever `SPEC.md`, pelo menos 8 cenários BDD e pelo menos 2 ADRs, e commitá-los antes de `app/`.

- Verificação: histórico do Git, commits de spec anteriores aos de `app/`.
- Critério: Spec e planejamento, 10 pontos, junto com RM3.
- Etapa: após a Aula 1.
- Status: planejado para depois da Aula 1. A verificação será o histórico: commits de spec anteriores aos de `app/`. O BDD no CI, que a faixa Excelente pede, fica na etapa 4.

## RM2 — AGENTS.md evolutivo e verificável

Versionar `AGENTS.md` (ou equivalente) e alterá-lo ao longo do projeto, com pelo menos 3 commits e regras verificáveis.

- Verificação: pelo menos 3 commits no arquivo; cada regra aponta para um teste ou uma checagem objetiva.
- Critério: Contexto e harness, 6 pontos, junto com RM6.
- Etapa: após a Aula 1, e o arquivo continua mudando nas etapas seguintes.
- Status: planejado para depois da Aula 1. O arquivo segue previsto para mudar nas etapas seguintes.

## RM3 — Uma feature em vibe e outra em spec + plano

Uma feature sai sem plano. Outra sai com spec e plano aprovado. A pasta `docs/vibe-vs-spec/` guarda código, métricas e conclusão.

- Verificação: a pasta existe e compara as duas passagens.
- Critério: Spec e planejamento, 10 pontos, junto com RM1.
- Etapa: a passagem vibe é a Aula 1. A passagem com plano é a Aula 2. A conclusão única fecha quando as duas colunas existem.
- Status: planejado. A passagem vibe fica na Aula 1 e a passagem com plano na Aula 2.

## RM4 — MCP próprio e um MCP externo

Servidor MCP do projeto com pelo menos 2 tools sobre a camada de serviço, mais o uso de pelo menos 1 MCP externo.

- Verificação: código, config versionada, teste e evidência de chamada.
- Critério: MCP, 6 pontos.
- Etapa: após a Aula 2.
- Status: planejado.

## RM5 — Skill com eval de trigger

Uma skill própria. O eval de disparo tem pelo menos 5 casos positivos e 5 negativos, com precisão, recall e F1.

- Verificação: `SKILL.md`, arquivo de casos e resultado numérico.
- Critério: Skill, 6 pontos. Excelente pede iteração documentada.
- Etapa: após a Aula 3.
- Status: planejado.

## RM6 — Hook ou permissão como guardrail

Pelo menos um hook ou uma regra de permissão, com teste que prova o bloqueio.

- Verificação: config da ferramenta e teste do bloqueio.
- Critério: Contexto e harness (6) e Segurança (6). Falhar este RM zera os dois.
- Etapa: após a Aula 3.
- Status: planejado.

## RM7 — CI com testes, segredo e dependências

Workflow verde no commit da entrega: testes, cobertura de pelo menos 70%, secret scan e auditoria de dependências.

- Verificação: workflow verde.
- Critério: Implementação e testes (14) e Segurança (6). Falhar este RM zera os dois. É o maior bloco de pontos.
- Etapa: após a Aula 4.
- Status: planejado para depois da Aula 4.

## RM8 — Revisão por agente em PRs

Pelo menos 3 pull requests com comentário do agente e resposta humana a cada comentário.

- Verificação: PRs fechados com os dois lados da conversa.
- Critério: Avaliação e revisão, 4 pontos, junto com RM10.
- Etapa: após a Aula 4. O hábito de PR pequeno começa na etapa 2, porque o RM11 pede essa trilha.
- Status: planejado.

## RM9 — Injeção e threat model

Teste de prompt injection e threat model de uma página, mapeado aos 7 pilares.

- Verificação: `tests/` e `docs/threat-model.md`.
- Critério: Segurança, 6 pontos, junto com RM6 e RM7.
- Etapa: após a Aula 4.
- Status: planejado.

## RM10 — Golden set da funcionalidade com LLM

Pelo menos 10 casos para a funcionalidade com LLM e um relatório de eval com métricas e gates.

- Verificação: `evals/` e o relatório.
- Critério: Avaliação e revisão, 4 pontos, junto com RM8.
- Etapa: após a Aula 4. A funcionalidade em si entra na etapa 3. O golden set e os gates entram na etapa 4.
- Status: planejado.

## RM11 — Rastreabilidade

Issue, plano, branch, PR pequeno e commits com coautoria do agente. A amostra da correção é de 5 PRs. O trailer é `Co-Authored-By`.

- Verificação: amostra de 5 PRs e os trailers.
- Critério: Rastreabilidade e docs, 8 pontos, junto com RM12.
- Etapa: após a Aula 2, e a amostra continua até a entrega.
- Status: planejado para depois da Aula 2, com a amostra seguindo até a entrega.

## RM12 — ADLC-REPORT.md

Retrospectiva por fase, com custo, percentual aceito, drift e lições. O modelo é o do TriageDesk.

- Verificação: arquivo na raiz.
- Critério: Rastreabilidade e docs, 8 pontos, junto com RM11.
- Etapa: antes da Aula 5.
- Status: planejado.

## Fora dos doze, e mesmo assim obrigatório na entrega

- Tag `entrega-final` até 24 horas antes da Aula 5. Commit posterior à tag fica de fora da correção.
- README sobe a API e os testes em até 5 comandos.
- Agentes declarados. Cada integrante explica qualquer parte no Q&A.
- Segredos e dados pessoais reais ficam fora do Git.

## Bônus

Até +5 pontos nos artefatos, teto de 100. Cada item vale +2: A2A entre dois agentes, UI declarativa gerada pelo agente, comparação documentada de duas ferramentas, LLM-as-judge calibrado com notas humanas. Quatro itens somariam +8, então o teto de +5 corta a soma. Nenhum bônus está em andamento.

## Nota descrita no PDF

Artefatos valem 60 pontos. Apresentação vale 20: demo 12, narrativa 4, perguntas 4. Os outros 20 pontos do curso não aparecem neste PDF. A faixa dentro de cada critério de artefato é 100%, 60%, 20% ou 0.
