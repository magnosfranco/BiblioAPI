# Etapa 2 — após a Aula 2

Status: não iniciada.

Janela sugerida: 5 h. RMs: RM4 e RM11. Também fecha a segunda coluna do RM3.

## Objetivo

Implementar empréstimos e devolução com plano escrito antes do código, publicar um MCP próprio sobre o serviço e usar um MCP externo, com a trilha issue → plano → PR.

## Atividades

A2.1 a A2.8, em [atividades.md](../planejamento/atividades.md). Nenhuma começou.

## Critério de saída

- `docs/plans/` existe antes do commit que cria as rotas de empréstimo.
- Os dois cenários de `features/emprestimos.feature` passam.
- `exemplares_disponiveis` desconta empréstimo aberto, como manda a premissa P25.
- O servidor MCP do projeto expõe pelo menos duas tools do serviço, com teste.
- Um MCP externo tem config versionada e evidência de chamada.
- Há pelo menos um PR pequeno com `Co-Authored-By` e plano ligado.
- `docs/vibe-vs-spec/` compara as duas colunas com métricas e uma conclusão.

## Premissas que esta etapa não reabre

P18 a P26. Em especial: oito endpoints de negócio, fila FIFO já decidida, e recomendação fora desta janela.

Este arquivo passa a descrever o que foi feito quando a etapa fechar. A apresentação correspondente é [etapa-02.html](../apresentacao/etapa-02.html).
