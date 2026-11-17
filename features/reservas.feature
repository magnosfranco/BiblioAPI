# language: pt
Funcionalidade: Reservas e fila de espera
  Quem chega com exemplar disponível fica com a reserva pronta.
  Quem chega sem exemplar entra no fim da fila daquele livro.
  Cancelar uma reserva pronta entrega o exemplar a quem espera há mais tempo.

  Cenário: Reserva fica pronta quando há exemplar disponível
    Dado um sócio e um livro com 1 exemplar disponível
    Quando esse sócio reserva o livro
    Então a reserva fica com status "pronta"
    E a reserva não tem posição de fila
    E o catálogo mostra 0 exemplares disponíveis

  Cenário: Reserva entra na fila quando não há exemplar
    Dado um livro cujo único exemplar já está em uma reserva pronta
    Quando outro sócio reserva esse livro
    Então a nova reserva fica com status "aguardando"
    E a posição dessa reserva é 1

  Cenário: A fila conserva a ordem de chegada
    Dado um livro sem exemplar disponível
    Quando dois sócios reservam esse livro, um depois do outro
    Então o primeiro fica na posição 1 e o segundo na posição 2

  Cenário: Cancelar quem está no meio da fila reordena as posições
    Dado uma reserva pronta e três reservas aguardando, nas posições 1, 2 e 3
    Quando cancelo a reserva da posição 2
    Então as duas que restam ficam nas posições 1 e 2, na mesma ordem
    E a reserva pronta continua pronta

  Cenário: Cancelar a reserva pronta promove o primeiro da fila
    Dado uma reserva pronta e três reservas aguardando
    Quando cancelo a reserva pronta
    Então quem estava na posição 1 fica com status "pronta" e sem posição
    E quem estava na posição 2 passa para a posição 1
    E quem estava na posição 3 passa para a posição 2

  Cenário: Sócio não mantém duas reservas ativas do mesmo livro
    Dado um sócio com uma reserva ativa de um livro
    Quando esse sócio reserva o mesmo livro outra vez
    Então a API responde conflito
    Quando a reserva ativa é cancelada e o sócio reserva de novo
    Então a nova reserva é aceita

  Cenário: Reserva de livro inexistente retorna não encontrado
    Dado um sócio cadastrado
    Quando ele reserva um livro que não existe
    Então a API responde não encontrado

  Cenário: Reserva de sócio inexistente retorna não encontrado
    Dado um livro cadastrado
    Quando um sócio que não existe reserva esse livro
    Então a API responde não encontrado

  Cenário: Cancelar reserva inexistente retorna não encontrado
    Quando cancelo uma reserva que não existe
    Então a API responde não encontrado
