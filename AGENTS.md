# AGENTS.md — BiblioAPI (v1 · Estágio A)

> Regras canônicas para agentes de código. Evolui ao longo do projeto (RM2: ≥ 3 commits neste arquivo).  
> Versão atual: **v1 — Setup / Estágio A** (não exige plano aprovado para editar `app/`).

## R01 — Fonte de verdade

1. Requisitos acadêmicos: enunciado do curso (RM1–RM12).  
2. Contrato do produto: `SPEC.md` e `docs/adr/` (quando existirem).  
3. Este `AGENTS.md` + planos em `docs/plans/` (Estágio B).  
4. Nunca inventar endpoints, entidades ou regras fora do escopo isonômico.

## R02 — Escopo isonômico fechado

- **Em escopo:** sócios, livros, reservas FIFO, empréstimos/devolução, recomendações (LLM + fallback), health.  
- **Fora de escopo:** multas, pagamentos, login, múltiplas unidades, renovação automática, categorias de livro, UI obrigatória.  
- Endpoints de negócio alvo: 8 (+ `GET /saude` operacional).

## R03 — Arquitetura (camada única)

- Topologia: `routes` / `mcp_server` → `app/service.py` → SQLite.  
- **Proibido** criar `repository`/`DAO`.  
- Rotas e tools MCP **somente** delegam para `app.service` — sem lógica de negócio nas bordas.  
- MCP não importa rotas FastAPI e não abre SQL próprio.  
- Logs do MCP nunca em `stdout` (transporte stdio).

## R04 — Fronteira `sqlite3` (obrigatória)

| Permitido | Proibido |
| :--- | :--- |
| `app/db.py` (path, conexão, DDL `init_schema`) | `app/routes.py` |
| `app/service.py` (queries + regras de negócio) | `app/main.py` |
| | `mcp_server/` (qualquer arquivo) |
| | Qualquer outro módulo do repositório |

Importar ou usar `sqlite3` fora de `app/db.py` e `app/service.py` é violação arquitetural.

## R05 — Segurança e higiene de dados

- Não versionar segredos (`.env`, tokens `sk-`, `ghp_`, `Bearer`).  
- Dados de teste/fixtures usam e-mails sintéticos `@biblioteca.example.com`.  
- Não executar comandos destrutivos: `rm -rf`, `git push --force`, `DROP TABLE`, CLI `sqlite3` direta no shell.  
- O hook `scripts/guardrail_check.py` reforça estas regras de forma determinística.

## R06 — Git e rastreabilidade

- **Nunca** commit/push direto na `main` — **sempre** branch + Pull Request (inclui setup/C0).  
- Merges na `main` com **merge commit** (`--no-ff`) — squash/rebase desabilitados no GitHub.  
- Commits assistidos incluem trailer: `Co-Authored-By: Cursor Agent <noreply@cursor.com>`.  
- PRs pequenos; trilha Issue → (plano, quando aplicável) → branch → PR → revisão → resposta humana → merge.  
- Integrante autorizado a mergear: Magno da Silva Franco.  
- Não commitir a pasta `INTERNO/` (fica fora deste repositório).

## R07 — Docker / TLS Norton

- Build exige `docker/certs/*.crt` (raiz Norton no host Windows do grupo).  
- Variáveis no container: `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, `NODE_EXTRA_CA_CERTS`.  
- Ollama via `OLLAMA_BASE_URL=http://host.docker.internal:11434`.

## R08 — Estágio do harness

- **Estágio A (atual):** guardrail bloqueia segredos, comandos destrutivos e e-mails não sintéticos; **não** bloqueia edição em `app/`.  
- **Estágio B (futuro):** além do A, edições em `app/` ou `mcp_server/` exigem plano em `docs/plans/` com `Decisão humana: aceita` (sem linhas `pendente`).

## R09 — Como o agente deve trabalhar

1. Preferir Plan Mode para artefatos de produto/spec.  
2. Não criar `app/` antes de `SPEC.md` + ADRs + features commitados na `main` (RM1).  
3. Na fatia vibe, não criar planos em `docs/plans/` antecipadamente.  
4. Após Estágio B, implementar só o que o plano aprovado cobre.  
5. Rodar testes no Docker: `docker compose run --rm api pytest -q`.

## Checklist rápido antes de terminar uma tarefa

- [ ] Respeitou R03/R04 (camada única + fronteira sqlite3)  
- [ ] Sem segredos nem e-mails reais  
- [ ] Testes relevantes passando no container  
- [ ] Co-Authored-By nos commits assistidos  
