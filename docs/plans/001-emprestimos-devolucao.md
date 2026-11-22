# Plano 001 — Empréstimos e devolução (Spec + Plano)

| Campo | Valor |
| :--- | :--- |
| Issue | [#9](https://github.com/magnosfranco/BiblioAPI/issues/9) |
| Branch sugerida | `feat/plano-001-emprestimos` |
| Fatia | Spec + Plano (RM3) |
| SPEC | `SPEC.md` · RN07, RN09–RN12 (RN11 detalhada) |
| ADR | 0001 (camada única), 0002 (fila/promoção) |
| BDD | `features/emprestimos.feature` (todos os cenários via **pytest-bdd**) |

## Decisão humana

| Item | Status |
| :--- | :--- |
| Decisão humana: aceita | **aceita** |
| Aprovador | Magno da Silva Franco |
| Data | 2026-11-22 |

> Não há linhas `pendente` neste plano.

## 1. Objetivo

Implementar `POST /emprestimos` e `POST /emprestimos/{emprestimo_id}/devolucao` conforme `SPEC.md`, com **estratégia de testes fechada** (abaixo), evidência BDD no CI (B10/B11) e métricas Spec+Plano em `docs/vibe-vs-spec/`.

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
| `POST /emprestimos` | Fluxo RN11 completo (ver §5) |
| `POST /emprestimos/{id}/devolucao` | `devolvido` + **mesma** promoção RN07; 404; 409 se já devolvido |

- Schemas/respostas mínimas do SPEC  
- Estratégia de testes §5 (obrigatória)  
- Coluna Spec+Plano em `docs/vibe-vs-spec/README.md`  
- CI: cobertura `app` com `--cov-fail-under=70` (CI v2) se ainda não estiver na `main` após a vibe; **não reduzir**

### Não inclui

- Reimplementar sócios/livros/reservas (vibe)  
- MCP, recomendações/LLM, skill, threat model, UI  
- Segunda implementação da promoção de fila

## 4. Tarefas de implementação

1. `emprestar` / `devolver` em `app/service.py` reutilizando `promover_proxima` / `compactar_fila` (RN07).  
2. Rotas só delegam; status HTTP conforme SPEC.  
3. Implementar §5 (pirâmide + BDD + CI + evidência).  
4. Preencher métricas Spec+Plano (incl. “Testes adicionados”).  
5. PR `feat(RM3,RM7,RM11): …`, spec-reviewer + resposta humana, merge commit.

## 5. Estratégia de testes (obrigatória)

### 5.1 Pirâmide

| Camada | O quê | Obrigatório |
| :--- | :--- | :--- |
| **Service (unit)** | Ramos RN11/RN12 em `app/service.py` com DB SQLite **temporário por teste** | Sim |
| **API (`TestClient`)** | Status codes + corpo mínimo OpenAPI dos dois endpoints | Sim |
| **BDD (`pytest-bdd`)** | **Todos** os cenários de `features/emprestimos.feature` executáveis | Sim (B10/B11) — **não** “equivalentes opcionais” |
| **Regressão RN10** | `GET /livros` / `exemplares_disponiveis` após emprestar e após devolver | Sim |
| **Design RN07** | Provar que devolução e cancelamento vibe usam a **mesma** função de promoção (ex.: mesmo símbolo/`__code__` ou módulo único testado) | Sim |
| **Concorrência** | Dois empréstimos disputando o último exemplar (threads ou sequencial sob lock); no máx. um `201` | Sim (transação/`BEGIN IMMEDIATE` ou equivalente) |
| **OpenAPI smoke** | Paths `/emprestimos` e `/emprestimos/{id}/devolucao` presentes em `/openapi.json` | Sim |
| **Fronteira sqlite3** | Guardrail / teste de artefato já existente continua verde | Sim |

### 5.2 Fixtures

- Banco **isolado por teste** (arquivo temp ou `:memory:` com schema init).  
- Factories mínimas: sócio, livro, reserva (`pronta`/`aguardando`), empréstimo.  
- E-mails apenas `@biblioteca.example.com`.

### 5.3 Matriz BDD ↔ RN (checklist)

| Cenário (Gherkin) | RN |
| :--- | :--- |
| Consome reserva `pronta` (+ `reserva_id`) | RN11-(4) |
| `pronta` mesmo com `exemplares_disponiveis == 0` | RN11-(4) |
| Bloqueio se só `aguardando` | RN11-(3) |
| Empréstimo direto (`reserva_id` null) | RN11-(5) |
| Negado sem `pronta` e sem disponibilidade | RN11-(6) |
| Segundo empréstimo `aberto` do par | RN11-(2) |
| Sócio inexistente → 404 | RN11-(1) / RN09 |
| Livro inexistente → 404 | RN11-(1) / RN09 |
| Devolução promove posição 1 | RN12 + RN07 |
| Já devolvido → 409 | RN12 |
| Empréstimo inexistente → 404 | RN12 |
| Após emprestar, `exemplares_disponiveis` diminui | RN10 |
| Após devolver, `exemplares_disponiveis` aumenta (e/ou promoção) | RN10 / RN12 |

### 5.4 CI e evidência (RM7 + B11)

| Item | Exigência |
| :--- | :--- |
| Job `test` | `pytest` incluindo BDD da fatia emprestimos |
| Cobertura | `--cov=app --cov-fail-under=70` (ligar CI v2 nesta PR se a vibe ainda não tiver ligado) |
| Evidência BDD | Log da Action com cenários passando **ou** artefato/relatório versionado/anexado (ex. JUnit/`docs/evidencias/` com link do run) |
| Secret scan / audit | Permanecem (gitleaks + pip-audit) |

### 5.5 Fora do escopo de teste deste plano

- Prompt injection / threat model (RM9)  
- Golden set LLM (plano 004)  
- MCP (planos 002/003)

## 6. Critérios de aceite

- [x] Endpoints + respostas mínimas no OpenAPI (smoke §5.1)  
- [x] Matriz §5.3 100% verde via pytest-bdd  
- [x] Testes service + API + RN07 única + concorrência + RN10  
- [x] CI com cov≥70% e evidência de execução BDD *(evidência = run da Action após abrir a PR)*  
- [x] Sem `sqlite3` fora de `db.py`/`service.py`  
- [ ] Issue linkada; PR revisada; merge commit; métricas Spec+Plano preenchidas  

## 7. Riscos

| Risco | Mitigação |
| :--- | :--- |
| Vibe ainda não na main | Não mergear implementação antes da vibe |
| Empréstimo direto furar fila | Só se `exemplares_disponiveis > 0`; `aguardando` próprio → 409 |
| Duplicar promoção | Teste de design RN07 (§5.1) |
| Flaky DB | Fixture isolada por teste (§5.2) |
| Drift SPEC × código | Matriz BDD obrigatória (§5.3) |
