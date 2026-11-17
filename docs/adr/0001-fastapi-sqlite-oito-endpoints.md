# ADR 0001 — FastAPI, SQLite e oito endpoints de negócio

- Status: aceita
- Data: 2026-11-16

## Contexto

A BiblioAPI precisa ser uma API HTTP pequena, com persistência e OpenAPI, no mesmo envelope para todos os grupos do curso: de 5 a 8 endpoints de negócio. O ambiente de execução tem de ser reproduzível num notebook limpo, em poucos comandos. Não há requisito de mais de um processo nem de carga concorrente.

## Decisão

A API é escrita em Python 3.11 com FastAPI. O OpenAPI sai do próprio framework em `/openapi.json`. A persistência é SQLite via SQLAlchemy, num arquivo local, criado na subida da aplicação. O ambiente padrão é a imagem Docker deste repositório, com Git e Node.js 18 ou superior além do Python.

Os endpoints de negócio param em oito. `GET /saude` fica de fora dessa conta porque só serve para o healthcheck. Para não gastar um endpoint só para ler a fila, `GET /livros` devolve `exemplares_disponiveis` e `reservas_ativas`.

O código de produção mora em `app/`. Identificadores são inteiros gerados pelo banco.

## Consequências

Qualquer pessoa sobe a API com Docker, sem instalar o banco à parte. SQLite não é o alvo se a biblioteca um dia tiver vários balcões escrevendo ao mesmo tempo; trocar o banco nessa hipótese é outra decisão. A fila e o catálogo compartilham o mesmo recurso de leitura, então a resposta de `GET /livros` cresce junto com as reservas ativas. Isso é aceitável no volume desta disciplina.

## Alternativas recusadas

PostgreSQL num segundo contêiner aumenta o ambiente sem mudar o que a rubrica observa. Um endpoint `GET /reservas/{id}` deixaria o contrato mais fino e empurraria empréstimo ou recomendação para fora do limite de oito rotas.
