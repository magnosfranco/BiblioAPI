# Vibe × spec + plano

Registro da etapa após a Aula 1. A coluna da feature com plano fica aberta até os empréstimos terem um arquivo em `docs/plans/` antes do código.

A passagem em vibe implementou sócios, catálogo e reservas com fila. A spec e os cenários já estavam escritos. O que não existiu foi um plano de implementação: a fila saiu direto de `SPEC.md` e de `features/reservas.feature` para `app/service.py`.

Os arquivos em `codigo/` são a cópia de `app/` nessa passagem. O código que roda continua em `app/`.

## Métricas

Contadas nos arquivos Python desta etapa, em linhas físicas, no momento do commit da feature.

| | Vibe: reservas e fila | Spec + plano: empréstimos |
| --- | --- | --- |
| Plano em `docs/plans/` antes do código | nenhum | ainda não iniciado |
| Cenários BDD | 14 automatizados em `tests/test_reservas.py` | 2 cenários em `features/emprestimos.feature`, sem código |
| Arquivos Python de produção | 8, em `app/` | — |
| Linhas em `app/` | 418 | — |
| Linhas em `tests/` | 298 | — |
| `pytest -q` | 25 testes passando | — |
| Endpoints no ar | `POST /socios`, `POST /livros`, `GET /livros`, `POST /reservas`, `DELETE /reservas/{reserva_id}`, `GET /saude` | `POST /emprestimos` e `POST /emprestimos/{id}/devolucao` seguem só na spec |

`app/service.py` concentra 173 dessas 418 linhas. É onde estão a fila FIFO, a promoção e o cancelamento.

## Conclusão desta passagem

A fila ficou verificável: os 14 cenários de catálogo e reserva passam, inclusive reordenação no meio e promoção de quem está na posição 1. O custo de não ter plano aparece num ponto só. `exemplares_disponiveis` desconta reservas `pronta` e deixa empréstimos abertos fixos em zero, com um comentário no serviço. Quando a devolução passar a liberar exemplar, essa conta muda no mesmo módulo que já promove a fila. A etapa com plano precisa tratar isso como decisão explícita no plano, não como mais um ajuste silencioso.

A comparação fecha quando empréstimos forem implementados com plano aprovado e as duas colunas tiverem código, métricas e uma conclusão única.
