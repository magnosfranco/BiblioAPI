# language: pt
Funcionalidade: Saúde da API
  Como operador
  Quero verificar se a API está no ar
  Para monitoramento e demo

  Cenário: Health check retorna ok
    Quando consultar GET /saude
    Então a resposta deve ter status 200
    E o corpo deve conter status "ok"
