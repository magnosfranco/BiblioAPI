# Vibe × Spec+Plano (RM3)

Comparação metodológica exigida pelo `Projeto.pdf` (RM3).

| Campo | Valor |
| :--- | :--- |
| Fatia **Vibe** | Sócios, livros, reservas FIFO (+ `/saude`) — **sem** `docs/plans/` |
| Fatia **Spec+Plano** | Empréstimos + devolução — plano `001` |
| Preenchimento | Coluna Vibe após sessão vibe; coluna Spec+Plano após plano 001; conclusão ao fechar as duas |

## Métricas (definir antes; medir durante)

| Métrica | Unidade / como medir | Vibe | Spec+Plano |
| :--- | :--- | :--- | :--- |
| Duração da fatia | minutos (relógio) | ~5 min (18:35:29 → 18:40:23, código+testes+métricas; PR/push após autorização) | _a preencher_ |
| Sessões de agente | contagem | 1 | _a preencher_ |
| Turns / mensagens relevantes | contagem aproximada | ~3 (1 prompt humano + 2 ciclos agente) | _a preencher_ |
| Commits na branch/PR | `git rev-list --count` | 3 | _a preencher_ |
| Arquivos tocados | diffstat da PR | 16 | _a preencher_ |
| Linhas + / − | diffstat da PR | +816 / −22 | _a preencher_ |
| Testes adicionados | contagem / nomes (Spec+Plano: BDD emprestimos + pirâmide do plano 001) | 15 pytest HTTP: `test_saude`, `test_socios` (3), `test_livros` (3), `test_reservas` (8); + ajuste `test_artefatos` (app presente) | _a preencher_ |
| Evidência BDD no CI | link do run / relatório | features = contrato; execução via pytest HTTP; CI do PR #6 | _a preencher_ (obrigatório no 001) |
| Retrabalho | ciclos fix→reteste ou reverts | 1 (Docker: `ModuleNotFoundError: app` → `pythonpath=.` + `PYTHONPATH=/app`) | _a preencher_ |
| Desvios do SPEC | lista objetiva | (1) DDL inclui tabela `emprestimos` só para RN10 — sem endpoints de empréstimo; (2) `DELETE /reservas/{id}` responde **204** (SPEC permite 200 ou 204) | _a preencher_ |
| Planos usados? | sim/não + path | **não** | `docs/plans/001-…` |
| PR | número + link | [#6](https://github.com/magnosfranco/BiblioAPI/pull/6) | _a preencher_ |
| SHA merge | short hash | TBD (após merge) | _a preencher_ |

## Notas qualitativas

### Vibe
- Prompt inicial / como a sessão foi aberta: ver [`prompt-sessao-vibe.md`](./prompt-sessao-vibe.md) (texto canônico · 2026-11-22)  
- O que o agente fez bem: seguiu SPEC/features sem abrir `docs/plans/`; montou `routes → service → SQLite`; FIFO (pronta/aguardando, compactar/promover) com testes; `pytest` local e `docker compose run --rm api pytest -q` verdes  
- Falhas / correções humanas: _nenhuma correção humana até o rascunho das métricas; 1 correção técnica Docker pelo próprio agente_  

### Spec+Plano
- O plano 001 ajudou / atrapalhou: _a preencher_  
- O que o agente fez bem: _a preencher_  
- Falhas / correções humanas: _a preencher_  

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
