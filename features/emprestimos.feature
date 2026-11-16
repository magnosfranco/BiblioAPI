# language: pt
Funcionalidade: Empréstimos e devoluções
  Fatia da etapa spec + plano. Estes cenários estão aceitos e ainda
  não são executados pela API. A implementação espera um plano em docs/plans/.

  Cenário: Empréstimo reduz os exemplares disponíveis
    Dado um livro com 2 exemplares disponíveis
    Quando um sócio empresta esse livro
    Então o catálogo passa a mostrar 1 exemplar disponível

  Cenário: Devolução promove o primeiro da fila
    Dado um livro sem exemplar disponível, com o exemplar emprestado e um sócio aguardando
    Quando o exemplar emprestado é devolvido
    Então a reserva que estava na posição 1 fica pronta
