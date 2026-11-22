# language: pt
Funcionalidade: Reservas e fila FIFO
  Como atendente
  Quero criar e cancelar reservas
  Para respeitar a fila de espera dos sócios

  Cenário: Reserva nasce pronta quando há exemplar disponível
    Dado que existe sócio "ana.silva@biblioteca.example.com"
    E que existe livro "Dom Casmurro" com 1 exemplar disponível
    Quando criar reserva do sócio para o livro
    Então a reserva deve ter status "pronta"
    E a posição da reserva deve ser nula

  Cenário: Reserva nasce aguardando quando não há exemplar disponível
    Dado que existe sócio "ana.silva@biblioteca.example.com"
    E que existe livro "Dom Casmurro" com 0 exemplares disponíveis
    Quando criar reserva do sócio para o livro
    Então a reserva deve ter status "aguardando"
    E a posição da reserva deve ser 1

  Cenário: Segunda reserva aguardando recebe posição 2
    Dado que o livro "Dom Casmurro" já tem uma reserva aguardando na posição 1
    E que existe outro sócio "bruno@biblioteca.example.com"
    Quando criar reserva do segundo sócio para o mesmo livro
    Então a nova reserva deve ter status "aguardando"
    E a posição da nova reserva deve ser 2

  Cenário: Rejeitar segunda reserva ativa do mesmo par sócio-livro
    Dado que o sócio já possui reserva ativa para o livro
    Quando criar novamente reserva do mesmo sócio para o mesmo livro
    Então a resposta deve ter status 409

  Cenário: Cancelar aguardando compacta a fila
    Dado fila aguardando com posições 1 e 2 no mesmo livro
    Quando cancelar a reserva na posição 1
    Então a reserva restante deve passar à posição 1

  Cenário: Cancelar pronta promove o primeiro da fila
    Dado reserva pronta e uma aguardando na posição 1 no mesmo livro
    Quando cancelar a reserva pronta
    Então a reserva que estava na posição 1 deve ficar "pronta"
