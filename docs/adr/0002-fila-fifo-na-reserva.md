# ADR 0002 — Fila FIFO embutida em `reservas`

| Campo | Valor |
| :--- | :--- |
| Status | Aceito |
| Data | 2026-11-22 |

## Contexto

Reservas precisam de fila de espera quando não há exemplares disponíveis, com promoção justa (FIFO) ao cancelar `pronta` ou devolver empréstimo.

## Decisão

- **Não** criar tabela `fila` separada.  
- Estado da fila vive em `reservas`: `status` + `posicao` (`aguardando` com posições 1..N).  
- Uma função síncrona de **promoção/compactação** é usada por cancelamento e devolução (RN07).

## Consequências

- Uma fonte de verdade; menos risco de inconsistência entre tabelas.  
- Compactação deve ser testada (cenários BDD de fila).  
- Consultas de “quem é o próximo” são por `livro_id` + `status='aguardando'` ordenado por `posicao`.
