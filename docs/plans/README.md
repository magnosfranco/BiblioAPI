# Planos aprovados (RM11)

| Plano | Tema | Metodologia | Executar após |
| :--- | :--- | :--- | :--- |
| `001-emprestimos-devolucao.md` | Empréstimos / devolução | Spec + Plano (RM3) | Fatia **vibe** na main |
| `002-mcp-proprio.md` | MCP próprio | Spec + Plano | Plano 001 (API estável) |
| `003-mcp-filesystem.md` | MCP filesystem | Spec + Plano | Config Cursor |
| `004-recomendacoes-llm.md` | Recomendações LLM | Spec + Plano | Empréstimos + catálogo |

## Decisão de ordem (Magno da Silva Franco · 2026-11-22)

1. **Agora:** versionar estes planos (aprovados).  
2. **Não** ativar Estágio B do guardrail ainda (senão a vibe deixa de ser válida).  
3. **Sessão nova:** fatia vibe (sócios/livros/reservas) **sem** usar estes planos.  
4. **Depois:** implementar o plano **001** (feature com plano de fato).  

Commit sugerido (GIT-D1): `docs(RM11,RM3): add approved plans 001-004 and vibe-vs-spec metrics scaffold`.

Também versionar `docs/vibe-vs-spec/README.md` (métricas RM3 definidas antes das execuções).  

Todos os planos abaixo trazem `Decisão humana: aceita` e **nenhuma** linha `pendente`.
