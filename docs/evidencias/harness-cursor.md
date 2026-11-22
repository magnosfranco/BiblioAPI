# Comprovação — Harness Cursor (rules, hooks, agents, skills, MCP)

> Evidência de configuração e uso do Agent Harness do Cursor (RM2, RM5, RM6, RM8 e narrativa ADLC).  
> **Atualizado C1** — 2026-11-22 (AGENTS v2 + SPEC/ADRs/features).

---

## 1. Objetivo

Demonstrar que o agente não opera “só no chat”: há **regras, hooks, subagentes e skills** versionados, com rastreabilidade no Git + Actions.

## 2. Raiz correta do workspace

| Correto | Incorreto |
| :--- | :--- |
| Abrir **`repo/`** (clone de `magnosfranco/BiblioAPI`) como pasta do projeto no Cursor | Abrir só a pasta pai e esperar que `repo/.cursor/*` carregue |

## 3. Mapa do harness → arquivos → RM

| Peça | Caminho | RM |
| :--- | :--- | :--- |
| Regras ADLC | `.cursor/rules/adlc-core.mdc` | RM2 |
| Contexto canônico | `AGENTS.md` + `CLAUDE.md` | RM2 |
| Guardrail | `.cursor/hooks.json` → `scripts/guardrail_check.py` | RM6 |
| Subagente revisão | `.cursor/agents/spec-reviewer.md` | RM8 |
| Subagente docs | `.cursor/agents/doc-architect.md` | RM1/11/12 |
| Skills (a partir E6) | `.agents/skills/auditar-biblioapi/SKILL.md` | RM5 |
| MCP próprio + filesystem (Planos 002/003) | `.cursor/mcp.json` (`biblioapi-service` + `biblio-filesystem`) | RM4 |
| CI v1 | `.github/workflows/ci.yml` (ruff, pytest+artefatos, pip-audit, gitleaks) | RM7 |
| SPEC / BDD / ADRs | `SPEC.md`, `features/`, `docs/adr/` | RM1 |
| AGENTS v2 | `AGENTS.md` (2º commit evolutivo) | RM2 |

## 4. Checklist de configuração (humano)

### Workspace

- [ ] Pasta aberta = clone BiblioAPI
- [ ] Workspace **Trusted**
- [ ] Material interno de estudo **fora** do working tree Git

### Hooks / guardrail

- [ ] `.cursor/hooks.json` → `python scripts/guardrail_check.py`
- [ ] `pytest tests/test_guardrail.py` verde (local ou CI)

### Subagentes / skills / MCP

- [ ] Agents em `.cursor/agents/`
- [ ] Skill `auditar-biblioapi` na Etapa 6
- [ ] Aprovar MCP na 1ª conexão (sem segredos no JSON) — ver `docs/evidencias/mcp-filesystem.md`

## 5. Evolução

| Momento | Harness |
| :--- | :--- |
| **PR0 / C0** | Rules + AGENTS v1 + hooks A + 2 agents + CI v0 |
| **C1** | AGENTS v2 + SPEC/BDD/ADRs + CI v1 (test_artefatos) |
| **PR2** | Guardrail Estágio B |
| **E6** | Skill + eval |
| **ADLC-REPORT** | Ferramentas/modelos por fase |

## 6. Registro de verificação

| Integrante | Data | Workspace OK? | Trusted? | Hooks OK? | pytest guardrail | Obs. |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Magno da Silva Franco | 2026-11-22 | ☐ | ☐ | ☐ | 9/9 local (pré-PR0) | Preencher prints na demo |

## 7. Decisões de governança (resumo)

- Rito: **sempre PR**; nunca push direto na `main` (aprovado 2026-11-22).  
- Secret scan CI: **gitleaks**.  
- Cert Norton: versionar apenas `.crt` público.
