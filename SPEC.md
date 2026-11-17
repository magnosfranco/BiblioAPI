# SPEC — BiblioAPI

Especificação de produto escrita antes do código de `app/`. O domínio é uma biblioteca pequena: catálogo, reservas com fila de espera e, nas etapas seguintes, empréstimos e recomendação.

## 1. Problema

O balcão precisa saber se ainda há exemplar de um livro, reservar esse exemplar para um sócio e, quando não há, manter a ordem de chegada de quem está esperando. A versão desta etapa entrega essa fila. Empréstimo, devolução e recomendação ficam especificados aqui e entram depois, cada um no modo de trabalho previsto na seção 4.

## 2. Atores

Não há autenticação nesta versão. A API é interna de demonstração e trata quem chama como o balcão da biblioteca. O sócio é o titular da reserva e, mais adiante, do empréstimo.

## 3. Escopo

Entram no produto:

- cadastro de sócio e de livro
- consulta do catálogo com exemplares disponíveis e reservas ativas
- reserva que ocupa um exemplar ou entra no fim da fila
- cancelamento com reordenação e promoção
- empréstimo e devolução
- recomendação de livros a partir do histórico, com fallback determinístico

Ficam de fora: multa, pagamento, login, várias unidades, renovação automática e o domínio TriageDesk.

## 4. Modo de construção

| Fatia | Modo | Quando |
| --- | --- | --- |
| Sócios, catálogo, reservas e fila | vibe: a spec e os cenários existem antes; não há arquivo em `docs/plans/` | após a Aula 1 |
| Empréstimos e devoluções | spec + plano em `docs/plans/` antes do código | após a Aula 2 |
| `POST /recomendacoes` | funcionalidade com LLM, golden set e fallback determinístico | após a Aula 3 |

A comparação das duas primeiras fatias fica em `docs/vibe-vs-spec/`.

## 5. Regras de negócio

- RN1. O email do sócio é único. A comparação ignora maiúsculas e espaços nas pontas.
- RN2. Um livro nasce com pelo menos 1 exemplar e no máximo 50.
- RN3. Se há exemplar disponível, a reserva nasce `pronta`, sem posição de fila, e passa a ocupar um exemplar.
- RN4. Se não há exemplar disponível, a reserva nasce `aguardando` na última posição da fila daquele livro.
- RN5. A fila é FIFO: a posição 1 é quem chegou primeiro entre os que ainda aguardam.
- RN6. Cancelar quem está no meio da fila remove essa reserva e renumera as posições restantes a partir de 1, sem furar a ordem relativa.
- RN7. Cancelar uma reserva `pronta` libera o exemplar. Se existe fila, a reserva de menor posição vira `pronta` e sai da fila. As demais são renumeradas.
- RN8. Um sócio só pode ter uma reserva ativa (`pronta` ou `aguardando`) do mesmo livro. Depois de cancelar, pode reservar de novo.
- RN9. Sócio ou livro inexistente não cria reserva. Reserva inexistente não é cancelada.
- RN10. Exemplares disponíveis = exemplares do livro − reservas `pronta` − empréstimos abertos. Nesta etapa não existe empréstimo, então a terceira parcela é zero.
- RN11. Um empréstimo só é criado se houver exemplar disponível. Se o sócio já tem reserva `pronta` daquele livro, o empréstimo consome essa reserva. Se não há exemplar, a API recusa.
- RN12. A devolução encerra o empréstimo e aplica a mesma promoção da RN7.

RN11 e RN12 pertencem à fatia com plano. A fatia em vibe deixa o gancho da RN10 explícito e não publica os endpoints de empréstimo.

## 6. Vocabulário de status

`pronta`, `aguardando`, `cancelada`. Reserva `pronta` tem `posicao` nula. Reserva `aguardando` tem `posicao` inteira começando em 1.

## 7. Endpoints de negócio

São oito, para caber no envelope do curso. `GET /saude` é operacional e não entra nessa conta.

| Método e caminho | Fatia | Efeito |
| --- | --- | --- |
| `POST /socios` | vibe | Cria sócio. Corpo: `nome`, `email`. Resposta 201: `id`, `nome`, `email` já normalizado. |
| `POST /livros` | vibe | Cria livro. Corpo: `titulo`, `autor`, `exemplares`. Resposta 201 no formato de `GET /livros`. |
| `GET /livros` | vibe | Lista os livros por `id`. Cada item traz `exemplares_disponiveis` e `reservas_ativas`. |
| `POST /reservas` | vibe | Cria reserva. Corpo: `socio_id`, `livro_id`. Resposta 201: `id`, `socio_id`, `livro_id`, `status`, `posicao`. |
| `DELETE /reservas/{reserva_id}` | vibe | Cancela e promove se for o caso. Resposta 200 com a reserva cancelada. |
| `POST /emprestimos` | plano | Cria empréstimo. Corpo: `socio_id`, `livro_id`. |
| `POST /emprestimos/{emprestimo_id}/devolucao` | plano | Devolve o exemplar e promove a fila. |
| `POST /recomendacoes` | LLM | Sugere livros para um `socio_id`. Se o modelo não responder, devolve um ranking determinístico. O contrato fino entra na etapa do LLM. |

`reservas_ativas` lista reservas `pronta` (por `id`) e depois as `aguardando` (por `posicao`). Cada item tem `id`, `socio_id`, `status` e `posicao`. A fila não ganha endpoint próprio: a consulta cabe em `GET /livros`, e assim o produto continua com oito endpoints de negócio.

## 8. Erros

| Situação | HTTP | `detail` |
| --- | --- | --- |
| Corpo inválido, nome vazio ou exemplar fora de 1–50 | 422 | formato do FastAPI |
| Email já cadastrado | 409 | Já existe um sócio com esse email |
| Reserva ativa duplicada para o mesmo par sócio/livro | 409 | Já existe uma reserva ativa desse sócio para esse livro |
| Reserva já cancelada | 409 | A reserva já está cancelada |
| Sócio inexistente | 404 | Sócio não encontrado |
| Livro inexistente | 404 | Livro não encontrado |
| Reserva inexistente | 404 | Reserva não encontrada |

## 9. Persistência e contrato

SQLite, um arquivo local, sem serviço externo. O contrato HTTP é o OpenAPI gerado em `/openapi.json` e a UI em `/docs`. Dados de exemplo usam o domínio `biblioteca.example.com`. Segredos e dados pessoais reais não entram no repositório.

## 10. Cenários BDD

Os arquivos em `features/` são a fonte dos cenários. A coluna de teste aponta o executável desta etapa. Os dois cenários de empréstimo permanecem só na spec até a etapa com plano.

| Cenário | Regra | Teste nesta etapa |
| --- | --- | --- |
| Cadastrar sócio | RN1 | `test_cadastrar_socio` |
| Recusar email duplicado | RN1 | `test_recusar_email_duplicado` |
| Cadastrar livro com exemplares | RN2 | `test_cadastrar_livro_com_exemplares` |
| Recusar livro sem exemplar | RN2 | `test_recusar_livro_sem_exemplar` |
| Listar catálogo com exemplares disponíveis | RN3, RN10 | `test_listar_catalogo_com_exemplares_disponiveis` |
| Reserva fica pronta quando há exemplar disponível | RN3 | `test_reserva_fica_pronta_quando_ha_exemplar` |
| Reserva entra na fila quando não há exemplar | RN4 | `test_reserva_entra_na_fila_quando_nao_ha_exemplar` |
| A fila conserva a ordem de chegada | RN5 | `test_fila_conserva_a_ordem_de_chegada` |
| Cancelar quem está no meio da fila reordena as posições | RN6 | `test_cancelar_quem_esta_no_meio_reordena_as_posicoes` |
| Cancelar a reserva pronta promove o primeiro da fila | RN7 | `test_cancelar_a_reserva_pronta_promove_o_primeiro` |
| Sócio não mantém duas reservas ativas do mesmo livro | RN8 | `test_socio_nao_mantem_duas_reservas_ativas_do_mesmo_livro` |
| Reserva de livro inexistente retorna não encontrado | RN9 | `test_reserva_de_livro_inexistente_retorna_nao_encontrado` |
| Reserva de sócio inexistente retorna não encontrado | RN9 | `test_reserva_de_socio_inexistente_retorna_nao_encontrado` |
| Cancelar reserva inexistente retorna não encontrado | RN9 | `test_cancelar_reserva_inexistente_retorna_nao_encontrado` |
| Empréstimo reduz os exemplares disponíveis | RN11 | etapa spec + plano |
| Devolução promove o primeiro da fila | RN12 | etapa spec + plano |

## 11. Ambiente

Python 3.11, Git e Node.js 18 ou superior dentro da imagem Docker descrita no `README.md`. A ferramenta de agente desta etapa é o Cursor, no host.
