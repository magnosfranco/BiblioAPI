# language: pt
Funcionalidade: Empréstimos e devolução
  Como atendente
  Quero emprestar e devolver livros
  Para consumir reservas prontas, permitir empréstimo direto quando há exemplar livre e liberar a fila

  Cenário: Empréstimo consome reserva pronta do próprio sócio
    Dado que o sócio possui reserva "pronta" para o livro
    Quando criar empréstimo do sócio para o livro
    Então a resposta deve ter status 201
    E a reserva deve ficar "atendida"
    E o empréstimo deve ficar "aberto"
    E o empréstimo deve referenciar a reserva consumida

  Cenário: Empréstimo bloqueado se sócio só tem reserva aguardando
    Dado que o sócio possui apenas reserva "aguardando" para o livro
    Quando criar empréstimo do sócio para o livro
    Então a resposta deve ter status 409

  Cenário: Empréstimo direto quando há exemplar disponível e sem reserva ativa
    Dado que o sócio não possui reserva ativa para o livro
    E que exemplares_disponiveis do livro é maior que 0
    Quando criar empréstimo do sócio para o livro
    Então a resposta deve ter status 201
    E o empréstimo deve ficar "aberto"
    E reserva_id do empréstimo deve ser nulo

  Cenário: Empréstimo negado sem reserva pronta e sem exemplar disponível
    Dado que o sócio não possui reserva "pronta" para o livro
    E que exemplares_disponiveis do livro é 0
    Quando criar empréstimo do sócio para o livro
    Então a resposta deve ter status 409

  Cenário: Rejeitar segundo empréstimo aberto do mesmo par
    Dado que já existe empréstimo "aberto" do sócio para o livro
    Quando criar novamente empréstimo do mesmo sócio para o mesmo livro
    Então a resposta deve ter status 409

  Cenário: Sócio inexistente ao emprestar
    Quando criar empréstimo para sócio inexistente
    Então a resposta deve ter status 404

  Cenário: Devolução marca empréstimo como devolvido e promove fila
    Dado empréstimo "aberto" e reserva "aguardando" posição 1 no mesmo livro
    Quando devolver o empréstimo
    Então o empréstimo deve ficar "devolvido"
    E a reserva da posição 1 deve ficar "pronta"

  Cenário: Devolver empréstimo já devolvido retorna conflito
    Dado empréstimo com status "devolvido"
    Quando devolver o empréstimo novamente
    Então a resposta deve ter status 409

  Cenário: Devolver empréstimo inexistente
    Quando devolver empréstimo inexistente
    Então a resposta deve ter status 404
