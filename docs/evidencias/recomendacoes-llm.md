# Evidência — recomendações LLM (plano 004 / RM10)

| Campo | Valor |
| :--- | :--- |
| Data | 2026-11-23 |
| Issue | [#16](https://github.com/magnosfranco/BiblioAPI/issues/16) |
| Branch | `feat/plano-004-recomendacoes` |
| ADR | `docs/adr/0004-llm-local-e-fallback.md` |
| SPEC | RN13, RN14 |

## O que entrou

- `POST /recomendacoes` com `origem` `ollama` ou `fallback_deterministico`.
- Cliente em `app/ollama_client.py`: `POST /api/chat`, `format=json`, timeout padrão 2s (`OLLAMA_TIMEOUT`). URL em `OLLAMA_BASE_URL` (o Compose já aponta para `host.docker.internal:11434`).
- Ids fora do catálogo disponível, ou de livro que o sócio já emprestou, são descartados. Se não sobra nenhum, vale o fallback.
- Fallback: mais empréstimos históricos primeiro; empate no menor `livro_id`.
- Golden set com 12 casos em `evals/golden_set_recomendacoes.json`. Relatório em `evals/relatorio_recomendacoes.md`. O runner não chama a rede.

## Fora deste plano

Skill `auditar-biblioapi` e threat model (RM9) ficam para um PR seguinte. O Estágio B do guardrail continua desligado.

## Como provar

`pytest tests/test_recomendacoes_bdd.py tests/test_golden_set.py tests/test_ollama_client.py -q`
