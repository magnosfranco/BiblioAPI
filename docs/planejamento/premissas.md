# Premissas

Restrições que valem para todas as atividades. Uma atividade que fure uma premissa não conta como concluída. Premissa nova entra neste arquivo antes de orientar a etapa seguinte.

Há dois blocos: o que o `projeto.pdf` impõe e o que este repositório já decidiu. O terceiro bloco lista o que ainda precisa de confirmação do professor. Isso não é premissa adotada.

## Da disciplina

- P01. O envelope é uma API HTTP com 5 a 8 endpoints de negócio, persistência em SQLite ou equivalente e OpenAPI.
- P02. Existe pelo menos uma funcionalidade com LLM e um fallback determinístico. Modelo local, como Ollama, é aceito.
- P03. O domínio pode ser sugerido ou proposto até a Aula 2. TriageDesk é o exemplo e o modelo de repositório. Usá-lo como domínio do grupo está fora do escopo. Copiar arquivo dele para este domínio, sem adaptação, não pontua.
- P04. Os doze RMs, a rubrica, o prazo e o formato de entrega são os mesmos para todos os grupos.
- P05. Falhar um RM zera o critério da rubrica ligado a ele. RM6 zera contexto e segurança. RM7 zera implementação e segurança.
- P06. `SPEC.md`, os cenários BDD e os ADRs entram no Git antes do código de `app/`.
- P07. `AGENTS.md` muda ao longo do projeto, em pelo menos 3 commits, com regras verificáveis.
- P08. Uma feature é feita em vibe, sem plano. Outra é feita com spec e plano. A comparação fica em `docs/vibe-vs-spec/`.
- P09. O uso de agente é obrigatório e declarado com `Co-Authored-By` e no `ADLC-REPORT.md`.
- P10. A trilha de uma mudança de produto é issue → plano → branch → PR pequeno → commits com coautoria.
- P11. Segredos, chaves e dados pessoais reais ficam fora do Git. Dados de exemplo são sintéticos.
- P12. Copiar artefato de outro grupo, inclusive skill e golden set, sem atribuição, é plágio.
- P13. Cada integrante explica qualquer parte do projeto no Q&A.
- P14. A tag `entrega-final` existe até 24 horas antes da Aula 5. Commit posterior a ela não é avaliado.
- P15. O README sobe a API e os testes em até 5 comandos num ambiente limpo.
- P16. O ambiente de referência tem Python 3.11 ou superior, Git e Node.js 18 ou superior. Pelo menos uma ferramenta de agente está em uso.
- P17. Excelente, Adequado, Insuficiente e Ausente valem 100%, 60%, 20% e 0% dos pontos do critério.

## Deste repositório

- P18. O domínio é a BiblioAPI: catálogo, reservas, fila, empréstimos e recomendação.
- P19. A feature em vibe é reservas e fila. A feature com plano é empréstimo e devolução. A funcionalidade com LLM é `POST /recomendacoes`.
- P20. A stack aceita é FastAPI, SQLite e SQLAlchemy, na imagem Docker deste repositório. Decisão em `docs/adr/0001-fastapi-sqlite-oito-endpoints.md`.
- P21. Os endpoints de negócio param em oito. `GET /saude` é operacional e não entra na conta. A fila é lida em `GET /livros`.
- P22. A fila é FIFO e mora em `reservas.posicao`. Promoção é síncrona no cancelamento e, na etapa 2, na devolução. Decisão em `docs/adr/0002-fila-fifo-na-reserva.md`.
- P23. Status públicos: `pronta`, `aguardando`, `cancelada`. Caminhos em português: `/socios`, `/livros`, `/reservas`, `/emprestimos`, `/recomendacoes`.
- P24. Email de exemplo usa o sufixo `@biblioteca.example.com`.
- P25. Exemplares disponíveis = exemplares do livro − reservas `pronta` − empréstimos abertos. Na etapa 1 a terceira parcela é zero. A etapa 2 substitui esse zero. Não criar outro contador paralelo.
- P26. Empréstimo e recomendação não ganham rota antes da etapa correspondente. `tests/test_openapi.py` vigia isso até a etapa 2 e a etapa 3, respectivamente, quando o teste é atualizado junto com a spec.
- P27. O agente desta etapa roda no host (Cursor). O contêiner é o runtime da API, dos testes, do Git e do Node.
- P28. A composição do grupo ainda tem vagas em `docs/grupo.md`. Enquanto isso, o Q&A individual continua sendo premissa da entrega, não uma tarefa adiada para a véspera.

## A confirmar com o professor

Estes pontos estão em aberto. Nenhuma atividade assume um deles como decidido.

- O PDF descreve 60 pontos de artefatos e 20 de apresentação. Os outros 20 pontos do curso não estão nesse arquivo.
- O bônus fala em +5 pontos nos artefatos e em teto de 100, enquanto a escala publicada dos artefatos é 0 a 60.
- A data civil da Aula 5, que dispara o prazo da tag, não está no PDF.
