# Vibe × Spec+Plano (RM3)

Comparação metodológica exigida pelo `Projeto.pdf` (RM3).

| Campo | Valor |
| :--- | :--- |
| Fatia **Vibe** | Sócios, livros, reservas FIFO (+ `/saude`) — **sem** `docs/plans/` |
| Fatia **Spec+Plano** | Empréstimos + devolução — plano `001` |
| Preenchimento | Coluna Vibe após sessão vibe; coluna Spec+Plano após plano 001; conclusão ao fechar as duas |
| Status Spec+Plano (2026-11-22) | **Commit autorizado (~19:17 UTC−3)** — contraparte pós-vibe; dívidas 1–4, 6–7 pagas na branch; PR/CI a seguir |

## Registro de tempos (relógio · UTC−3)

| Fatia / marco | Início | Fim | Duração | Notas |
| :--- | :--- | :--- | :--- | :--- |
| **Vibe** — agent work (código+testes+rascunho métricas) | 18:35:29 | 18:40:23 | **~5 min** | Sessão dedicada; commits/PR depois da autorização |
| **Vibe** — PR #6 merge | — | — | (fora do agent clock) | SHA `5394d4e` |
| **Pós-vibe** — revisão × planos (métricas + dívida) | ~19:01 | 19:04 | **~3 min** | Entrega da revisão no chat; base do backlog 001 |
| **Spec+Plano** — autorização Magno (“pode fazer”) | 19:04 | 19:04 | — | Inclui registrar dívida no comparativo |
| **Spec+Plano** — impl. plano 001 (código+BDD+CI local) | 19:04 | ~19:09 | **~5 min** | Branch `feat/plano-001-emprestimos`; Issue #9; pytest 64/64 |
| **Spec+Plano** — doc. tempos / status pendente | ~19:10 | ~19:16 | **~6 min** | `registro-tempos.md` + README |
| **Spec+Plano** — autorização commit Magno | ~19:16 | ~19:16 | — | Chat ADLC |
| **Spec+Plano** — commit + push + PR + CI run | ~19:17 | ~19:18 | **~1–2 min** (push/PR; CI ~33 s) | PR #10 · [CI #45076907694](https://github.com/magnosfranco/BiblioAPI/actions/runs/45076907694) success |

**Totais parciais (só agent clock até agora):** Vibe **~5 min** · Spec+Plano (revisão+impl) **~8 min** (3+5) · commit/PR **não incluídos**.

Detalhamento espelhado: [`registro-tempos.md`](./registro-tempos.md).

## Métricas (definir antes; medir durante)

| Métrica | Unidade / como medir | Vibe | Spec+Plano |
| :--- | :--- | :--- | :--- |
| Duração da fatia | minutos (relógio) | **~5 min** (18:35:29 → 18:40:23 — código+testes+rascunho; commits/PR após autorização) | **~8 min** até agora (19:01–19:09 = revisão 3 min + impl 5 min); **+ tempo de commit/PR pendente** |
| Sessões de agente | contagem | 1 | 1 (mesma conversa ADLC pós-vibe; branch `feat/plano-001-emprestimos`) |
| Turns / mensagens relevantes | contagem aproximada | ~3 na implementação (1 prompt + 2 ciclos agente); +1 turn de autorização commit/PR | revisão → “pode fazer” → impl → doc tempos; **+autorização commit/PR pendente** |
| Commits na branch/PR | `git rev-list --count` | 3 (`origin/main..` da PR #6) | 2 (`origin/main..` da PR [#10](https://github.com/magnosfranco/BiblioAPI/pull/10) após métricas) |
| Arquivos tocados | diffstat da PR | 16 | 13 |
| Linhas + / − | diffstat da PR | +816 / −22 | +904 / −33 (feat `aaec566`) + docs métricas |
| Testes adicionados | contagem / nomes (Spec+Plano: BDD emprestimos + pirâmide do plano 001) | 15 pytest HTTP: `test_saude` (1), `test_socios` (3), `test_livros` (3), `test_reservas` (8); + ajuste `test_artefatos` (app presente) | 34: service (11) + API (7) + BDD (13 `emprestimos.feature`) + extra RN07/concorrência/OpenAPI (3) |
| Evidência BDD no CI | link do run / relatório | [CI run #45073962932](https://github.com/magnosfranco/BiblioAPI/actions/runs/45073962932) (success · PR #6); `.feature` = contrato; comportamento via pytest HTTP no job `test` | [CI run #45076907694](https://github.com/magnosfranco/BiblioAPI/actions/runs/45076907694) (success · PR #10 · CI v2 cov≥70 + pytest-bdd) |
| Retrabalho | ciclos fix→reteste ou reverts | 1 (Docker: `ModuleNotFoundError: app` → `pythonpath=.` + `PYTHONPATH=/app`) | 2 (pytest-bdd 8×pytest 9 → bump `pytest-bdd>=9.0.1`; step BDD disponiveis=1 reaproveitava livro com 2 exemplares) |
| Desvios do SPEC | lista objetiva | (1) DDL inclui tabela `emprestimos` só para RN10 — sem endpoints de empréstimo; (2) `DELETE /reservas/{id}` responde **204** (SPEC permite 200 ou 204) | (1) resolvido — endpoints `/emprestimos` + devolução; (2) mantido 204; índices UNIQUE parciais (não exigidos literalmente no SPEC, reforço RN08/RN11) |
| Planos usados? | sim/não + path | **não** | **sim** — `docs/plans/001-emprestimos-devolucao.md` + Issue [#9](https://github.com/magnosfranco/BiblioAPI/issues/9) |
| PR | número + link | [#6](https://github.com/magnosfranco/BiblioAPI/pull/6) (MERGED) | [#10](https://github.com/magnosfranco/BiblioAPI/pull/10) (aberta) |
| SHA merge | short hash | `5394d4e` | _após merge_ |

## Notas qualitativas

### Vibe
- Prompt inicial / como a sessão foi aberta: confirmado — [`prompt-sessao-vibe.md`](./prompt-sessao-vibe.md) (texto canônico · 2026-11-22); sessão aberta com o prompt VIBE RM3 sem `docs/plans/`
- Prompt de fechamento das métricas: [`prompt-metricas-coluna-vibe.md`](./prompt-metricas-coluna-vibe.md) (PR #7)  
- O que o agente fez bem: seguiu SPEC/features do escopo; arquitetura `routes → service → SQLite`; FIFO (pronta/aguardando, compactar/promover); testes locais + Docker verdes; branch `feat/vibe-reservas` + PR #6 com CI success  
- Falhas / correções humanas: nenhuma correção humana na implementação; 1 retrabalho técnico pelo agente (import `app` no Docker); Magno só autorizou commits/PR  

### Revisão pós-vibe × planos (2026-11-22)

Comparação do código mergeado (`5394d4e`) com `docs/plans/001` e SPEC, **antes** da implementação Spec+Plano. Fonte: revisão Magno+agente no chat ADLC.

**Alinhamento (pré-reqs do plano 001):** `/saude`, sócios, livros, reservas (+ DELETE), FIFO RN03–RN08/RN10, `promover_ou_compactar` única (RN07), sem leitura de `docs/plans/`, camada única + `sqlite3` só em `db`/`service`. Planos 002–004 fora do escopo da vibe (correto).

**Métricas extras (além da tabela):**

| Item | Valor |
| :--- | :--- |
| Cobertura local `app/` (pós-vibe) | ~95% (`pytest --cov=app`) |
| Locais não cobertos | `service` ~51, 118–119, 127, 185, 249; `routes` 63–64 (409 no DELETE) |
| Tamanho `service.py` | ~270 linhas |
| Commits / velocidade vibe | 3 commits · ~5 min agent work |

**Dívidas técnicas priorizadas para o plano 001:**

| # | Dívida | Impacto no 001 | Tratamento no 001 | Status |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Sem `BEGIN IMMEDIATE` / transação atômica no check+insert | Corrida em empréstimo/reserva; §5 exige teste de concorrência | `BEGIN IMMEDIATE` em sócios/livros/reservas/emprestar/devolver; `isolation_level=None` | **Paga** |
| 2 | Sem índice único de reserva ativa `(socio_id, livro_id)` | Duplicata sob carga | `idx_reservas_ativa_unica` + `idx_emprestimos_aberto_unico` | **Paga** |
| 3 | Uma conexão por operação sem transação multi-step | Dificulta `emprestar`/`devolver` atômicos | Uma `conn` + commit único por caso de uso | **Paga** |
| 4 | DDL `emprestimos` sem API (desvio já na coluna Vibe) | 001 só pluga endpoints | `POST /emprestimos` + `POST …/devolucao` | **Paga** |
| 5 | `ValueError` em `criar_livro` pode virar 500 se service for chamado fora do schema | Baixo (Pydantic cobre HTTP) | Aceito — schema HTTP cobre | **Aceita** |
| 6 | Testes só HTTP — sem pytest-bdd; RN07 só indireto | 001 exige pirâmide + BDD + design test | BDD 13 cenários + teste símbolo RN07 | **Paga** |
| 7 | CI ainda v1 (sem `cov-fail-under`) | Exigência §5.4 | CI v2 `--cov-fail-under=70` | **Paga** |
| 8 | Branches pouco testadas (IntegrityError e-mail; cancelar não-ativa; etc.) | Lacunas de cobertura | Parcial — cov app ~95%; IntegrityError paths ainda existem | **Parcial** |
| 9 | DELETE 409 quase sem cobertura (`routes` 63–64) | Lacuna HTTP | Não bloqueante; permanece | **Aberta** |
| 10 | Schema de e-mail só exige `@`, não domínio fixture | Guardrail no agente; API aceita outros | Fixtures `@biblioteca.example.com` nos testes 001 | **Aceita** |

**Veredito da revisão:** vibe adequada ao escopo reduzido e aos pré-reqs do 001; não “copiou” o plano (correto). Maior dívida estrutural = concorrência/transação + CI cov + BDD executável — **paga** nesta fatia Spec+Plano (itens 1–4, 6–7).

### Spec+Plano
- Papel na narrativa RM3: **implementação que ficava pendente após o vibe coding** (empréstimos + pagar dívidas estruturais da vibe); ver [`registro-tempos.md`](./registro-tempos.md)  
- Status (2026-11-22 ~19:17 UTC−3): código+testes locais OK · **commit autorizado** · PR/CI a seguir  
- O plano 001 ajudou / atrapalhou: **ajudou** — matriz RN11/RN12 + pirâmide §5; Issue #9 (RM11)  
- O que o agente fez bem: endpoints RN11/RN12; reuso `promover_ou_compactar`; índices + `BEGIN IMMEDIATE`; pytest-bdd 13/13; CI v2; dívida+tempos no comparativo  
- Falhas / correções humanas: bump `pytest-bdd` 8→9.0.1; ajuste step BDD disponibilidade; Magno autoriza commits/PR  

## Conclusão (preencher só no fim das duas fatias)

- Qual método foi mais previsível? _a preencher_  
- Qual gerou menos retrabalho? _a preencher_  
- O que manteríamos no próximo ADLC? _a preencher_  

## Decisão de estrutura

| Campo | Valor |
| :--- | :--- |
| Aprovado por | Magno da Silva Franco |
| Data | 2026-11-22 |
| Nota | Esqueleto e métricas definidos **antes** das execuções; valores medidos nas etapas vibe e plano 001 |
