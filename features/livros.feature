# language: pt
Funcionalidade: Catálogo de livros
  Como atendente
  Quero cadastrar e listar livros
  Para controlar exemplares disponíveis

  Cenário: Cadastrar livro com exemplares válidos
    Quando cadastrar o livro "Dom Casmurro" do autor "Machado de Assis" com 3 exemplares
    Então a resposta deve ter status 201
    E o livro deve ter 3 exemplares

  Cenário: Rejeitar exemplares fora do intervalo 1..50
    Quando cadastrar o livro "Inválido" do autor "X" com 0 exemplares
    Então a resposta deve ter status 422

  Cenário: Listar livros com exemplares_disponiveis derivados
    Dado que existe livro "Dom Casmurro" com 2 exemplares
    Quando listar os livros
    Então a resposta deve ter status 200
    E cada livro listado deve incluir exemplares_disponiveis
