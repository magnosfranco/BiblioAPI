# Evidência — modelo local de recomendações (Ollama)

| Campo | Valor |
| :--- | :--- |
| Data | 2026-11-23 (UTC−3) |
| Onde rodou | Host Windows desta máquina. Sem API paga. Sem nuvem. |
| Cliente | `POST /api/chat` em `http://127.0.0.1:11434`, `format=json`, `temperature=0` |
| Ollama | 0.40.17 |
| Base | `data/biblio.db` depois de `python scripts/popular_base.py`: 4 sócios sintéticos, 8 livros, 19 empréstimos |
| Chamada | `POST /recomendacoes` com `limite` 3, pelos sócios Ana, Bruno e Clara |
| Timeout do projeto | 15 s (`OLLAMA_TIMEOUT`). Nesta medição o limite foi 60 s, para o modelo lento poder terminar e o tempo aparecer na tabela |

O golden set do CI **não** entra nestes números. Ele usa um cliente falso e não abre o Ollama.

## Hardware local

| Peça | O que foi lido na máquina |
| :--- | :--- |
| CPU | Intel Core Ultra 7 255HX, 20 núcleos, clock base 2,4 GHz |
| RAM | 31,4 GB visíveis ao Windows |
| GPU usada pelo Ollama | NVIDIA GeForce RTX 5070 Laptop, 8151 MiB (`nvidia-smi`) |
| GPU integrada | Intel Graphics (não é o alvo da inferência) |
| Sistema | Windows |

## Modelos comparados

| Modelo | Tamanho no disco | Papel |
| :--- | :--- | :--- |
| `llama3.1:8b` | 4,9 GB | Padrão escolhido no código (`OLLAMA_MODEL`) |
| `qwen3.5:4b` | 3,3 GB | Instalado em seguida, para ver se valia trocar |

`qwen2.5:7b`, que era o exemplo antigo da apostila, **não** está instalado.

## Tempos na rota real

Três sócios, mesma base, limite 3. O relógio inclui a ida ao Ollama e a filtragem de ids.

| Sócio | `llama3.1:8b` | `qwen3.5:4b` (raciocínio ligado, padrão do modelo) |
| :--- | :--- | :--- |
| Ana Silva | 4,5 s · `ollama` · Capitães da Areia | 14,0 s · `ollama` · Capitães da Areia |
| Bruno Lima | 1,1 s · `ollama` · Memórias Póstumas de Brás Cubas, Macunaíma | 12,8 s · `ollama` · os mesmos dois |
| Clara Nunes | 1,0 s · `ollama` · Memórias Póstumas, Capitães da Areia, Macunaíma | 20,9 s · `ollama` · Memórias Póstumas, Vidas Secas, Capitães da Areia |

Os dois modelos ficaram dentro do catálogo. Nenhum devolveu id inventado nessas seis chamadas.

Uma chamada curta só ao `qwen3.5:4b`, pedindo um JSON mínimo, separou a causa da demora:

| Modo | Tempo | Texto de raciocínio | JSON |
| :--- | :--- | :--- | :--- |
| Padrão (pensa antes) | 32,4 s | 10 422 caracteres | válido |
| `think: false` | 0,4 s | 0 | válido |

Com o raciocínio desligado, a rota completa ficou rápida, mas piorou o acerto:

| Sócio | Tempo | Origem |
| :--- | :--- | :--- |
| Ana | 0,4 s | `fallback_deterministico` (o modelo não entregou um id aproveitável) |
| Bruno | 1,3 s | `ollama` |
| Clara | 1,7 s | `ollama` |

Antes desta base populada, a primeira chamada ao `llama3.1:8b` (modelo ainda carregando, timeout largo) levou **5,5 s** e voltou `ollama`. Com o modelo já na memória, a mesma rota em timeout de 2 s levou **1,0 s** e também voltou `ollama`. Por isso o timeout do projeto saiu de 2 s para 15 s: a carga fria do Llama passou de 2 s.

## Motivo da escolha

Fica **`llama3.1:8b`**.

- Nas três chamadas da base de exemplo a origem foi `ollama`, dentro de 15 s.
- O `qwen3.5:4b` no modo padrão também acertou os livros, mas a Clara levou 20,9 s. Com o timeout de 15 s a API teria respondido o fallback e a IA não apareceria.
- Desligar o raciocínio deixa o Qwen tão rápido quanto o Llama, e numa das três chamadas a origem deixou de ser o modelo.
- O Qwen ocupa menos disco (3,3 GB contra 4,9 GB). Isso não compensa perder a resposta do modelo dentro do timeout.

O cliente da BiblioAPI não envia `think: false`. Trocar o padrão para o Qwen exigiria esse parâmetro e uma nova medição. Até lá, o modelo da configuração é o Llama.
