# Plano 001 — Empréstimos e devolução (Spec + Plano)

| Campo | Valor |
| :--- | :--- |
| Issue | Criar Issue GitHub antes da PR de implementação (RM11) |
| Branch sugerida | `feat/plano-001-emprestimos` |
| Fatia | Spec + Plano (RM3) |
| SPEC | `SPEC.md` · RN07, RN09–RN12 (RN11 detalhada) |
| ADR | 0001 (camada única), 0002 (fila/promoção) |
| BDD | `features/emprestimos.feature` |

## Decisão humana

| Item | Status |
| :--- | :--- |
| Decisão humana: aceita | **aceita** |
| Aprovador | Magno da Silva Franco |
| Data | 2026-11-22 |

> Não há linhas `pendente` neste plano.

## 1. Objetivo

Implementar `POST /emprestimos` e `POST /emprestimos/{emprestimo_id}/devolucao` conforme `SPEC.md`, com testes (pytest / BDD da fatia) e registro de métricas Spec+Plano em `docs/vibe-vs-spec/`.

## 2. Pré-requisitos (fora do escopo deste plano)

Este plano **não** implementa a fatia vibe. Assume na `main` (após sessão vibe):

- `POST /socios`, `POST /livros`, `GET /livros`
- `POST /reservas`, `DELETE /reservas/{reserva_id}`
- `GET /saude`
- SQLite + fila FIFO (RN03–RN08, RN10) e função única de promoção/compactação (RN07) já usada no cancelamento

**Ordem ADLC:** planos versionados → vibe (sessão nova, sem ler planos) → executar este plano 001.

## 3. Escopo

### Inclui

| Endpoint | Comportamento (RN11 / RN12) |
| :--- | :--- |
| `POST /emprestimos` | Fluxo RN11 completo: 404 → 409 aberto → 409 aguardando → consome `pronta` → ou empréstimo direto se `exemplares_disponiveis > 0` → senão 409 |
| `POST /emprestimos/{id}/devolucao` | `devolvido` + **mesma** promoção RN07; 404 se id inexistente; 409 se já devolvido |

- Schemas/respostas mínimas do SPEC (`id`, `socio_id`, `livro_id`, `reserva_id`, `status`, timestamps)  
- Testes alinhados a `features/emprestimos.feature`  
- Atualizar coluna Spec+Plano em `docs/vibe-vs-spec/README.md`  
- Manter cov CI se já estiver ≥70% na `main` (não reduzir)

### Não inclui

- Reimplementar sócios/livros/reservas (vibe)  
- MCP, recomendações/LLM, skill, threat model, UI  
- Segunda implementação da promoção de fila

## 4. Tarefas de implementação

1. `emprestar` / `devolver` em `app/service.py` reutilizando `promover_proxima` / `compactar_fila` (RN07).  
2. Rotas só delegam; status HTTP conforme SPEC.  
3. Cobrir todos os ramos da RN11 (incluindo empréstimo direto e 404).  
4. Cobrir RN12 (sucesso, 404, 409).  
5. Ligar steps BDD da fatia ou testes equivalentes rastreáveis aos cenários.  
6. Preencher métricas Spec+Plano no vibe-vs-spec.  
7. PR com RMx no assunto (ex. `feat(RM3,RM11): …`), spec-reviewer + resposta humana, merge commit.

## 5. Critérios de aceite

- [ ] Ambos os endpoints no OpenAPI e respostas mínimas do SPEC  
- [ ] RN11: pronta, aguardando→409, segundo aberto→409, direto com disponibilidade, 404 sócio/livro, sem disponibilidade→409  
- [ ] RN12: devolução promove posição 1; 404; já devolvido→409  
- [ ] Uma única implementação de promoção (cancelamento vibe + devolução)  
- [ ] Sem `sqlite3` fora de `db.py`/`service.py`  
- [ ] Issue linkada; PR revisada; merge commit; métricas Spec+Plano preenchidas  

## 6. Riscos

| Risco | Mitigação |
| :--- | :--- |
| Vibe ainda não na main | Não mergear implementação deste plano antes da vibe |
| Empréstimo direto furar fila | Só permitido se `exemplares_disponiveis > 0` (implica ausência de disputa por exemplar livre); `aguardando` do próprio sócio sempre 409 |
| Duplicar promoção | Reusar a mesma função da vibe (aceite explícito) |
| Drift SPEC × código | BDD/cenários como checklist de PR |
