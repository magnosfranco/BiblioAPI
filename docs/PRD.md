# PRD — BiblioAPI

| Campo | Valor |
| :--- | :--- |
| Produto | BiblioAPI |
| Versão | 1.0 (Inception / Gate G1) |
| Data | 2026-11-22 |
| Domínio | Biblioteca comunitária (envelope isonômico do curso) |

## 1. Problema

Uma biblioteca comunitária precisa de um balcão digital mínimo para cadastrar sócios e livros, gerenciar **fila FIFO de reservas**, converter reserva pronta em **empréstimo**, processar **devolução** e oferecer **recomendação de livros** com LLM local e fallback determinístico.

## 2. Atores

| Ator | Interesse |
| :--- | :--- |
| Atendente / sistema balcão | Opera sócios, catálogo, reservas, empréstimos e devoluções via HTTP |
| Sócio (indireto) | Recebe recomendação; respeita a fila |
| Agente de código (Cursor) | Implementa sob SPEC, ADRs, planos e hooks |
| Avaliador (professor) | Verifica RM1–RM12 no GitHub, tag `entrega-final`, demo |

## 3. Objetivos

1. API HTTP com 8 endpoints de negócio + `GET /saude`, SQLite e OpenAPI.  
2. Pelo menos uma função com LLM (recomendações) e fallback determinístico.  
3. Rastreabilidade ADLC: SPEC/BDD/ADRs **antes** do código; PRs; CI; evals; relatório.

## 4. Escopo

### Em escopo

| Fatia | Capacidade | Método |
| :--- | :--- | :--- |
| Operacional | Health check | `GET /saude` |
| Vibe | Sócios, livros, reservas FIFO (criar/cancelar) | Sem plano prévio em `docs/plans/` |
| Spec + Plano | Empréstimos e devolução | Plano `001` aprovado (etapa posterior) |
| LLM + Eval | Recomendações | Plano `004` + golden set (etapa posterior) |

### Explicitamente fora de escopo

Multas · pagamentos · login/autenticação · múltiplas unidades · renovação automática · endpoint próprio de histórico/fila · categoria/tag de livro · UI obrigatória · dados pessoais reais.

## 5. Critérios de sucesso (produto + ADLC)

- Contrato em `SPEC.md` + ≥8 cenários BDD + ≥2 ADRs commitados **antes** de `app/`.  
- README sobe o sistema em ≤ 5 comandos.  
- CI com testes, secret scan e auditoria de dependências.  
- Tag `entrega-final` com evidências objetivas no repositório.

## 6. Gate G1

Este PRD é o artefato de Inception. Aprovação humana implícita ao mergear a PR C1 que o contém.
