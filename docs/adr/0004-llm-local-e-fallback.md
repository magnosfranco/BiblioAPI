# ADR 0004 — LLM local (Ollama) + fallback determinístico

| Campo | Valor |
| :--- | :--- |
| Status | Aceito |
| Data | 2026-11-22 |

## Contexto

O envelope isonômico exige ≥1 função com LLM e fallback determinístico. O grupo usa host Windows com Ollama local.

## Decisão

- `POST /recomendacoes` chama **Ollama** no host (`host.docker.internal:11434`), `format=json`, timeout curto.  
- Em falha/timeout/resposta inválida: **fallback** por popularidade histórica (contagem de empréstimos desc, desempate `livro_id` asc).  
- Resposta sempre inclui `origem`: `"ollama"` | `"fallback_deterministico"`.  
- Sem API paga obrigatória; evals/golden set reproduzíveis.

## Consequências

- CI não depende de modelo no runner (mocks / fallback).  
- Threat model e testes de prompt injection cobrem esta superfície (RM9, plano 006).  
- Implementação no plano 004 + `evals/`.
