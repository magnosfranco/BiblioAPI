# SPEC — BiblioAPI

| Campo | Valor |
| :--- | :--- |
| Versão | 1.0 |
| Data | 2026-11-22 |
| Status | Contrato para implementação (RM1) |
| Relacionados | `docs/PRD.md`, `docs/adr/`, `features/` |

## 1. Visão e escopo

Ver `docs/PRD.md`. Este documento é o **contrato executável**: endpoints, dados, regras de negócio (RN01–RN14) e invariantes de arquitetura.

## 2. Arquitetura

### 2.1 Camada única de serviço

```
HTTP (routes) ──┐
                ├──► app/service.py ──► SQLite
MCP (tools)  ───┘
```

- **Proibido** `repository`/`DAO`.  
- `sqlite3` **somente** em `app/db.py` (conexão/DDL) e `app/service.py` (queries + RNs).  
- Rotas e MCP **só** delegam para `app.service` — sem lógica de negócio nas bordas.  
- MCP não importa rotas FastAPI e não abre SQL próprio; logs MCP nunca em `stdout`.

### 2.2 Componentes

| Componente | Responsabilidade |
| :--- | :--- |
| `app/main.py` | FastAPI, lifespan (`init_schema`), rotas |
| `app/routes.py` | HTTP ↔ DTO; status codes |
| `app/schemas.py` | Pydantic |
| `app/service.py` | RNs + SQL |
| `app/db.py` | Path, conexão, DDL |
| `mcp_server/` | Tools → `app.service` (etapa MCP) |

## 3. Modelo de dados

### 3.1 `socios`

| Campo | Tipo | Restrições |
| :--- | :--- | :--- |
| `id` | INTEGER PK | autoincrement |
| `nome` | TEXT | not null, trim, não vazio |
| `email` | TEXT | not null, único case-insensitive (lower+trim) |
| `criado_em` | TEXT ISO-8601 | default now |

### 3.2 `livros`

| Campo | Tipo | Restrições |
| :--- | :--- | :--- |
| `id` | INTEGER PK | autoincrement |
| `titulo` | TEXT | not null |
| `autor` | TEXT | not null |
| `exemplares` | INTEGER | 1..50 |
| `criado_em` | TEXT ISO-8601 | default now |

`exemplares_disponiveis` é **derivado** (não coluna):  
`exemplares - count(reservas.status='pronta') - count(emprestimos.status='aberto')` por `livro_id`.

### 3.3 `reservas`

| Campo | Tipo | Restrições |
| :--- | :--- | :--- |
| `id` | INTEGER PK | autoincrement |
| `socio_id` | INTEGER FK | not null |
| `livro_id` | INTEGER FK | not null |
| `status` | TEXT | `pronta` \| `aguardando` \| `atendida` \| `cancelada` |
| `posicao` | INTEGER NULL | null se não `aguardando`; 1..N se `aguardando` |
| `criado_em` | TEXT ISO-8601 | default now |

Máximo **1 reserva ativa** (`pronta` ou `aguardando`) por `(socio_id, livro_id)`.

### 3.4 `emprestimos`

| Campo | Tipo | Restrições |
| :--- | :--- | :--- |
| `id` | INTEGER PK | autoincrement |
| `socio_id` | INTEGER FK | not null |
| `livro_id` | INTEGER FK | not null |
| `reserva_id` | INTEGER FK NULL | preenchido se consumiu reserva `pronta`; `NULL` se empréstimo direto (sem reserva) |
| `status` | TEXT | `aberto` \| `devolvido` |
| `emprestado_em` | TEXT ISO-8601 | default now |
| `devolvido_em` | TEXT ISO-8601 NULL | na devolução |

Máximo **1 empréstimo `aberto`** por `(socio_id, livro_id)`.

## 4. Contrato da API

Base: `http://localhost:8000` · OpenAPI: `/docs`, `/openapi.json`.

### 4.1 Endpoints

| Método | Path | Fatia | Sucesso | Erros principais |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/saude` | Ops | `200 {"status":"ok"}` | — |
| `POST` | `/socios` | Vibe | `201` | `409` e-mail duplicado; `422` |
| `POST` | `/livros` | Vibe | `201` | `422` exemplares fora de 1..50 |
| `GET` | `/livros` | Vibe | `200` lista com `exemplares_disponiveis` | — |
| `POST` | `/reservas` | Vibe | `201` | `404`; `409` reserva ativa duplicada |
| `DELETE` | `/reservas/{reserva_id}` | Vibe | `200` ou `204` | `404`; efeitos de fila |
| `POST` | `/emprestimos` | Spec | `201` corpo do empréstimo | `404` sócio/livro; `409` (aberto, aguardando, sem disponibilidade) |
| `POST` | `/emprestimos/{id}/devolucao` | Spec | `200` corpo do empréstimo | `404` empréstimo; `409` já devolvido |
| `POST` | `/recomendacoes` | LLM | `200` + `origem` | `404`; timeout → fallback |

### 4.2 Payloads (resumo)

**POST `/socios`**
```json
{ "nome": "Ana Silva", "email": "ana.silva@biblioteca.example.com" }
```

**POST `/livros`**
```json
{ "titulo": "Dom Casmurro", "autor": "Machado de Assis", "exemplares": 3 }
```

**POST `/reservas`** / **POST `/emprestimos`**
```json
{ "socio_id": 1, "livro_id": 1 }
```

**Resposta `201`/`200` de empréstimo (mínimo)**
```json
{
  "id": 1,
  "socio_id": 1,
  "livro_id": 1,
  "reserva_id": 10,
  "status": "aberto",
  "emprestado_em": "2026-11-22T12:00:00+00:00",
  "devolvido_em": null
}
```
Na devolução: `status` = `"devolvido"` e `devolvido_em` preenchido. `reserva_id` pode ser `null` no empréstimo direto.

**POST `/recomendacoes`**
```json
{ "socio_id": 1, "limite": 3 }
```

Resposta de recomendações (exemplo):
```json
{
  "socio_id": 1,
  "itens": [{ "livro_id": 2, "titulo": "...", "autor": "...", "motivo": "..." }],
  "origem": "ollama"
}
```
`origem`: `"ollama"` | `"fallback_deterministico"`.

### 4.3 Erros HTTP

| HTTP | Quando |
| :--- | :--- |
| `404` | Entidade inexistente |
| `409` | Conflito de regra |
| `422` | Validação / limites |
| `503` | Evitar — preferir fallback se Ollama falhar |

## 5. Regras de negócio (RN01–RN14)

| ID | Regra |
| :--- | :--- |
| **RN01** | E-mail do sócio único (trim + case-insensitive). Fixtures: `@biblioteca.example.com`. |
| **RN02** | `exemplares` ∈ [1, 50]. |
| **RN03** | Se `exemplares_disponiveis > 0` na criação, reserva nasce `pronta` (`posicao = null`). |
| **RN04** | Senão, nasce `aguardando` com `posicao = max(posicao)+1` do livro. |
| **RN05** | Cancelar `aguardando` compacta posições restantes para `1..N`. |
| **RN06** | Cancelar `pronta` promove síncronamente posição 1 → `pronta` e renumerar. |
| **RN07** | Função única de promoção/compactação usada por cancelamento e devolução. |
| **RN08** | Máx. 1 reserva ativa (`pronta`\|`aguardando`) por `(socio_id, livro_id)`. |
| **RN09** | Sócio/livro inexistente → `404`. |
| **RN10** | `exemplares_disponiveis = exemplares − #pronta − #emprestimos_abertos`. |
| **RN11** | Empréstimo (`POST /emprestimos`), em ordem: (1) sócio/livro inexistente → `404`; (2) já existe empréstimo `aberto` do par → `409`; (3) se o sócio tem reserva `aguardando` do livro → `409` (não fura fila); (4) se tem reserva `pronta` do próprio sócio → consome (`atendida`), `reserva_id` preenchido, cria `aberto` **mesmo se** `exemplares_disponiveis == 0` (a `pronta` já reserva o exemplar); (5) se **não** tem reserva ativa e `exemplares_disponiveis > 0` → empréstimo **direto** (`reserva_id = null`); (6) caso contrário → `409`. Máx. 1 `aberto` por `(socio_id, livro_id)`. |
| **RN12** | Devolução → `devolvido` + **a mesma** promoção/compactação síncrona da RN07 (não duplicar lógica). Empréstimo inexistente → `404`; já `devolvido` → `409`. |
| **RN13** | `/recomendacoes` usa Ollama (`format=json`, timeout curto), cruza histórico, valida IDs. |
| **RN14** | Falha/timeout Ollama → fallback por popularidade (empréstimos desc, `livro_id` asc); `origem: "fallback_deterministico"`. |

## 6. Estados

**Reserva:** `pronta` ↔ `aguardando` (promoção) → `atendida` | `cancelada`.  
**Empréstimo:** `aberto` → `devolvido`.

## 7. BDD e ADRs

- Cenários Gherkin em `features/` (≥8 obrigatório; alvo ≥16).  
- Decisões em `docs/adr/0001`–`0004`.  
- Implementação de `app/` **somente após** este SPEC (e ADRs/features) estar na `main`.

### 7.1 Papel do BDD no C1 (especificação)

**Decisão aprovada — Magno da Silva Franco · 2026-11-22** (alinhada ao RM1 do `Projeto.pdf`: cenários BDD **escritos ANTES do código**).

| Momento | Papel de `features/*.feature` | O que o CI testa |
| :--- | :--- | :--- |
| **C1 (agora)** | **Especificação** do comportamento (contrato Gherkin) | Artefatos: existência de SPEC/ADRs + contagem ≥8 (alvo ≥16) de `Cenário:`; guardrail; **não** executa steps contra API |
| **Após `app/`** | Mesmos cenários passam a ter steps `pytest-bdd` executáveis | Comportamento HTTP/serviço + evidência de run no CI |

Não há pasta `app/` no C1 por desenho científico (RM1).
