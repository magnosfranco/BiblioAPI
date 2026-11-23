# Relatório — golden set de recomendações (plano 004 / RM10)

Runner: `evals/run_llm_eval.py`. Ollama real não é chamado.

Casos: 12. Aprovados: 12.

| Caso | Origem | livros | Gate |
| :--- | :--- | :--- | :--- |
| `G01-ollama-escolhe` | ollama | 2 | ok |
| `G02-timeout-fallback` | fallback_deterministico | 2, 1 | ok |
| `G03-desempate-id` | fallback_deterministico | 1, 2 | ok |
| `G04-alucinacao-parcial` | ollama | 1 | ok |
| `G05-so-alucinacao` | fallback_deterministico | 1, 2 | ok |
| `G06-json-invalido` | fallback_deterministico | 1 | ok |
| `G07-ja-lido` | ollama | 2 | ok |
| `G08-esgotado` | fallback_deterministico | 2 | ok |
| `G09-catalogo-vazio` | fallback_deterministico | — | ok |
| `G10-limite` | fallback_deterministico | 1 | ok |
| `G11-cold-start` | fallback_deterministico | 1, 2 | ok |
| `G12-tudo-emprestado` | fallback_deterministico | — | ok |
