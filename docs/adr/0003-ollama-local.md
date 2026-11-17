# ADR 0003 — Ollama local na recomendação, com fallback determinístico

- Status: aceita
- Data: 2026-11-17

## Contexto

A disciplina pede uma funcionalidade com LLM e um fallback determinístico. Modelo local é aceito, e Ollama é o exemplo citado no plano do curso. A BiblioAPI reserva `POST /recomendacoes` para essa função. O notebook do grupo precisa reproduzir a demo sem depender de uma API paga de modelo.

## Decisão

O runtime do modelo é Ollama, na mesma máquina da API. Só o serviço de recomendação chama o Ollama. Se o processo não responder a tempo ou devolver uma resposta inválida, o mesmo serviço calcula um ranking determinístico a partir do SQLite e responde com ele.

O nome do modelo fica na variável `OLLAMA_MODEL`. O identificador concreto entra na etapa 3, quando o contrato fino da rota for escrito. O mapa de onde o Ollama e os MCPs ficam está em `docs/arquitetura.md`.

## Consequências

A demo da recomendação sobe com um processo a mais. O fallback mantém `POST /recomendacoes` útil quando o modelo não está carregado. A conta de exemplares, a fila e os empréstimos não passam pelo Ollama.

## Alternativas recusadas

Um modelo só por API externa deixa a demo presa a chave e a rede. Embutir o modelo dentro do processo da API aumenta a imagem e mistura inferência com as regras da biblioteca. Usar o MCP próprio para chamar o modelo esconderia a recomendação fora da API, e o balcão deixaria de ter o endpoint previsto na spec.
