# language: pt
Funcionalidade: Catálogo e sócios
  O balcão cadastra quem pode reservar e quais livros existem.
  O catálogo informa quantos exemplares ainda podem ser reservados.

  Cenário: Cadastrar sócio
    Dado que não existe o email "ana@biblioteca.example.com"
    Quando cadastro o sócio "Ana" com esse email
    Então a API cria o sócio e devolve o email normalizado

  Cenário: Recusar email duplicado
    Dado o sócio "Ana" cadastrado com "ana@biblioteca.example.com"
    Quando cadastro outro sócio com o email "Ana@biblioteca.example.com"
    Então a API recusa o cadastro por conflito

  Cenário: Cadastrar livro com exemplares
    Quando cadastro "Dom Casmurro" de "Machado de Assis" com 2 exemplares
    Então o livro entra no catálogo com 2 exemplares disponíveis

  Cenário: Recusar livro sem exemplar
    Quando cadastro um livro com 0 exemplares
    Então a API recusa o corpo da requisição

  Cenário: Listar catálogo com exemplares disponíveis
    Dado um livro com 2 exemplares e uma reserva pronta
    Quando consulto o catálogo
    Então esse livro mostra 1 exemplar disponível
