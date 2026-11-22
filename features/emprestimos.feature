# language: pt
Funcionalidade: Empréstimos e devolução
  Como atendente
  Quero emprestar e devolver livros
  Para consumir reservas prontas e liberar a fila

  Cenário: Empréstimo consome reserva pronta do próprio sócio
    Dado que o sócio possui reserva "pronta" para o livro
    Quando criar empréstimo do sócio para o livro
    Então a resposta deve ter status 201
    E a reserva deve ficar "atendida"
    E o empréstimo deve ficar "aberto"

  Cenário: Empréstimo bloqueado se sócio só tem reserva aguardando
    Dado que o sócio possui apenas reserva "aguardando" para o livro
    Quando criar empréstimo do sócio para o livro
    Então a resposta deve ter status 409

  Cenário: Rejeitar segundo empréstimo aberto do mesmo par
    Dado que já existe empréstimo "aberto" do sócio para o livro
    Quando criar novamente empréstimo do mesmo sócio para o mesmo livro
    Então a resposta deve ter status 409

  Cenário: Devolução marca empréstimo como devolvido e promove fila
    Dado empréstimo "aberto" e reserva "aguardando" posição 1 no mesmo livro
    Quando devolver o empréstimo
    Então o empréstimo deve ficar "devolvido"
    E a reserva da posição 1 deve ficar "pronta"

  Cenário: Devolver empréstimo já devolvido retorna conflito
    Dado empréstimo com status "devolvido"
    Quando devolver o empréstimo novamente
    Então a resposta deve ter status 409
