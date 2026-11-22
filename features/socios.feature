# language: pt
Funcionalidade: Cadastro de sócios
  Como atendente do balcão
  Quero cadastrar sócios
  Para operar reservas e empréstimos

  Cenário: Cadastrar sócio com e-mail sintético válido
    Quando cadastrar o sócio "Ana Silva" com e-mail "ana.silva@biblioteca.example.com"
    Então a resposta deve ter status 201
    E o sócio deve ter e-mail "ana.silva@biblioteca.example.com"

  Cenário: Rejeitar e-mail duplicado case-insensitive
    Dado que existe sócio com e-mail "ana.silva@biblioteca.example.com"
    Quando cadastrar o sócio "Ana Outra" com e-mail "Ana.Silva@biblioteca.example.com"
    Então a resposta deve ter status 409

  Cenário: Rejeitar nome vazio
    Quando cadastrar o sócio "" com e-mail "vazio@biblioteca.example.com"
    Então a resposta deve ter status 422
