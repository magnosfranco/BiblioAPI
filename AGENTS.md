# AGENTS.md — BiblioAPI (v3 · Estágio B)

> Regras canônicas para agentes de código. Evolui ao longo do projeto (RM2: v1 no C0, v2 no C1, v3 neste estágio).  
> Versão atual: **v3 — Estágio B** (plano aceito antes de editar `app/` ou `mcp_server/`).

## R01 — Fonte de verdade

1. Requisitos acadêmicos: enunciado do curso (RM1–RM12).  
2. Contrato do produto: **`SPEC.md`**, **`docs/adr/`**, **`features/`**, `docs/PRD.md`.  
3. Este `AGENTS.md` + planos em `docs/plans/` com `Decisão humana: aceita` e sem linha `pendente`.  
4. Nunca inventar endpoints, entidades ou regras fora do SPEC / escopo isonômico.

## R02 — Escopo isonômico fechado

- **Em escopo:** sócios, livros, reservas FIFO, empréstimos/devolução, recomendações (LLM + fallback), health — conforme `SPEC.md`.  
- **Fora de escopo:** multas, pagamentos, login, múltiplas unidades, renovação automática, categorias de livro, UI obrigatória.  
- Endpoints de negócio: 8 (+ `GET /saude` operacional).

## R03 — Arquitetura (camada única)

- Topologia: `routes` / `mcp_server` → `app/service.py` → SQLite (ADR 0001).  
- **Proibido** criar `repository`/`DAO`.  
- Rotas e tools MCP **somente** delegam para `app.service`.  
- MCP não importa rotas FastAPI e não abre SQL próprio (ADR 0003).  
- Logs do MCP nunca em `stdout`.

## R04 — Fronteira `sqlite3` (obrigatória)

| Permitido | Proibido |
| :--- | :--- |
| `app/db.py` (path, conexão, DDL `init_schema`) | `app/routes.py` |
| `app/service.py` (queries + regras de negócio) | `app/main.py` |
| | `mcp_server/` (qualquer arquivo) |
| | Qualquer outro módulo do repositório |

## R05 — Segurança e higiene de dados

- Não versionar segredos (`.env`, tokens `sk-`, `ghp_`, `Bearer`).  
- Dados de teste/fixtures usam e-mails sintéticos `@biblioteca.example.com` (RN01).  
- Não executar comandos destrutivos: `rm -rf`, `git push --force`, `DROP TABLE`, CLI `sqlite3` no shell.  
- O hook `scripts/guardrail_check.py` reforça estas regras.

## R06 — Git e rastreabilidade

- **Nunca** commit/push direto na `main` — **sempre** branch + Pull Request.  
- Merges na `main` com **merge commit** (`--no-ff`).  
- Commits assistidos: `Co-Authored-By: Cursor Agent <noreply@cursor.com>`.  
- **RMx no assunto** (GIT-D1 · Magno · 2026-11-22): ex. `feat(RM3): …`, `docs(RM11,RM3): …`.  
- Integrante autorizado a mergear: Magno da Silva Franco.  
- Não commitir a pasta `INTERNO/`.

## R07 — Docker / TLS Norton

- Build exige `docker/certs/*.crt` (raiz Norton pública).  
- Variáveis: `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, `NODE_EXTRA_CA_CERTS`.  
- Ollama: `OLLAMA_BASE_URL=http://host.docker.internal:11434`, modelo `llama3.1:8b`, timeout 15s (ADR 0004). No host, a URL é `http://127.0.0.1:11434`. Base de exemplo: `python scripts/popular_base.py`.

## R08 — Estágio do harness

- **Estágio A:** guardrail bloqueia segredos, destrutivos e e-mails não sintéticos; não exige plano para editar `app/`. Vale só com `GUARDRAIL_STAGE=A`.  
- **Estágio B (atual):** além do A, edições em `app/` ou `mcp_server/` exigem plano em `docs/plans/` com `Decisão humana: aceita` e sem linha `pendente`.

## R09 — Como o agente deve trabalhar

1. Preferir Plan Mode para artefatos de produto/spec.  
2. **RM1:** não criar `app/` antes de `SPEC.md` + ADRs + `features/` estarem na **`main`**.  
3. Na fatia vibe (sócios/livros/reservas), **não** criar `docs/plans/` antecipadamente.  
4. Empréstimos/devolução e LLM seguem planos aprovados nas etapas seguintes.  
5. Respeitar RN01–RN14 e cenários em `features/`.  
6. Testes: `docker compose run --rm api pytest -q` (ou pytest local quando aplicável).  
7. **RM8:** ao abrir um PR, publicar a revisão do `spec-reviewer` (`gh pr comment`, texto começando por `spec-reviewer (RM8)`) e parar até Magno responder. Regra sempre ativa: `.cursor/rules/revisao-pr-rm8.mdc`.

## Checklist rápido

- [ ] Respeitou R03/R04 e `SPEC.md`  
- [ ] Sem segredos nem e-mails reais  
- [ ] Não adiantou `app/` sem SPEC na main / não adiantou plans na vibe  
- [ ] Co-Authored-By nos commits assistidos  
