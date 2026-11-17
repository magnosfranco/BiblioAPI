# ADR 0002 — Fila FIFO persistida na própria reserva

- Status: aceita
- Data: 2026-11-16

## Contexto

Quando não há exemplar, os sócios precisam ser atendidos na ordem de chegada. O atendimento acontece no mesmo processo da API, no momento em que uma reserva `pronta` é cancelada ou, na etapa seguinte, quando um exemplar é devolvido. Não há produtores externos nem pico que justifique uma fila independente.

## Decisão

A fila de um livro é o conjunto de reservas com status `aguardando`, ordenado pelo inteiro `posicao`. Posição 1 é a mais antiga ainda ativa. A reserva nasce na posição `max(posicao) + 1`. Cancelar alguém do meio renumera as posições restantes a partir de 1, preservando a ordem relativa. Cancelar uma reserva `pronta` promove, na mesma transação, a menor posição para `pronta` e zera a posição dela antes de renumerar o resto.

Não há broker, tabela de fila separada nem processamento em background.

## Consequências

A ordem fica visível no mesmo registro que o resto da reserva e cabe num teste de API, sem infraestrutura extra. A promoção é síncrona: se a requisição de cancelamento confirma, a próxima pessoa já está `pronta`. Dois balcões concorrentes não são o caso desta versão; o SQLite serializa as escritas locais. Se a devolução entrar na próxima etapa, ela reutiliza a mesma promoção em vez de inventar outra fila.

## Alternativas recusadas

Uma tabela `fila` separada da reserva duplicaria o estado e abriria divergência entre “está na fila” e “tem reserva”. Um serviço de mensagens cumpriria FIFO com mais peças do que o escopo pede, e a rubrica não observa esse componente.
