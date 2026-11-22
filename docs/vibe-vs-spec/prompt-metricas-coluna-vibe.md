# Prompt — popular/validar coluna Vibe (RM3)

| Campo | Valor |
| :--- | :--- |
| Data | 2026-11-22 |
| Aplicado após | PR [#6](https://github.com/magnosfranco/BiblioAPI/pull/6) (fatia vibe) |
| Resultado | Coluna Vibe fechada na PR [#7](https://github.com/magnosfranco/BiblioAPI/pull/7) · merge `64bf5c4` |

Usado para conferir Git/PR/CI e completar células que o rascunho da sessão vibe deixou frágeis (SHA, link do run, notas). **Não** preenche Spec+Plano nem a conclusão final.

## Prompt

```text
Objetivo: completar/validar a coluna Vibe em docs/vibe-vs-spec/README.md (RM3).
NÃO implemente código novo. NÃO leia docs/plans/ para inventar a coluna Spec+Plano.

Fontes obrigatórias:
- PR https://github.com/magnosfranco/BiblioAPI/pull/6
- git diff --stat origin/main...origin/feat/vibe-reservas
- git rev-list --count origin/main..origin/feat/vibe-reservas
- docs/vibe-vs-spec/README.md (rascunho atual)
- docs/vibe-vs-spec/prompt-sessao-vibe.md
- Link do CI verde do PR #6

Tarefas:
1) Conferir cada célula da coluna Vibe; corrigir se divergir do Git/PR/CI.
2) Preencher o que ainda estiver frágil:
   - SHA merge: TBD até mergear; após merge, short hash da main
   - Evidência BDD no CI: colar URL do run Actions que passou
   - Notas qualitativas Vibe: confirmar prompt, o que foi bem, falhas/retrabalho (já há 1 fix Docker)
3) NÃO preencher coluna Spec+Plano nem a Conclusão final.
4) Se Magno fornecer hora início/fim ou contagem de turns diferente do rascunho, usar os valores dele (métricas ao vivo prevalecem).
5) Entregar: diff só em docs/vibe-vs-spec/README.md + resumo do que mudou. Commit só se autorizado: docs(RM3): finalize vibe column metrics for PR6
```
