# Prompt da sessão Vibe (RM3)

| Campo | Valor |
| :--- | :--- |
| Data | 2026-11-22 |
| Workspace | clone `repo/` (Trusted) |
| Branch alvo | `feat/vibe-reservas` |
| Escopo | Reduzido — sócios, livros, reservas FIFO, `/saude` |
| Proibido | `docs/plans/**` (planos 001–004); empréstimos; MCP; LLM; skills |

Este arquivo registra o **prompt usado / a usar** na sessão vibe, para rastreabilidade e métricas (campo “Prompt inicial” da comparação).

## Prompt

```text
Contexto: BiblioAPI (ADLC). Esta é uma fatia VIBE (RM3).

REGRAS OBRIGATÓRIAS:
1) NÃO abra, leia nem siga nada em docs/plans/ (planos 001–004 são de OUTRAS fatias / spec+plano).
2) Siga SPEC.md e as features de sócios/livros/reservas/saude apenas como contrato.
3) NÃO implemente empréstimos, recomendações, MCP, skills nem threat model.
4) Antes de codar: anote hora de início. Ao terminar: hora de fim, nº aproximado de turns/mensagens, retrabalho (quantas correções grandes), e preencha a coluna Vibe em docs/vibe-vs-spec/README.md com o que só dá para medir ao vivo. Diffstat/PR/SHA podem ficar TBD.
5) Git: branch feat/vibe-reservas; commits com Co-Authored-By: Cursor Agent <noreply@cursor.com> e RMx no assunto (ex. feat(RM3): ...); NUNCA push direto na main — abrir PR. Discuta comigo antes de commit se eu pedir; caso contrário proponha e eu autorizo.

ESCOPO REDUZIDO — implementar app/ agora:
- GET /saude
- POST /socios, POST /livros, GET /livros (com exemplares_disponiveis)
- POST /reservas, DELETE /reservas/{reserva_id} (FIFO: pronta/aguardando, cancelar compacta/promove)
- Arquitetura: routes → service.py → SQLite; sqlite3 só em db.py e service.py
- Testes mínimos (pytest); Docker se já funcionar no repo
- README só se necessário para subir

Entregável: código + testes passando + rascunho da coluna Vibe nas métricas + PR feat(RM3): fatia vibe socios/livros/reservas.
Comece pelo relógio (hora início) e pela estrutura mínima de app/, depois endpoints e testes.
```

## Preenchimento pós-sessão

Atualizar `docs/vibe-vs-spec/README.md` (coluna Vibe) e, se o texto do prompt mudar na prática, anotar o diff aqui ou na seção “Notas qualitativas”.
