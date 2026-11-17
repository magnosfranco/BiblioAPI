# Etapa 1 — após a Aula 1

Status: concluída em 16 nov 2026.

Janela sugerida: 4 h. RMs: RM1, RM2 e RM3.

## Objetivo

Deixar o contrato no Git antes do código, as regras do agente verificáveis e uma feature funcionando em modo vibe.

## O que foi feito

- Ambiente Docker com Python 3.11.18, Git 2.39.5 e Node.js 18.20.4. API e testes sobem em quatro comandos, dentro do limite de cinco.
- `SPEC.md` com oito endpoints de negócio, regras RN1 a RN12 e o mapa dos cenários.
- 16 cenários BDD: 5 de catálogo, 9 de reservas, 2 de empréstimos ainda sem código.
- ADR 0001 (FastAPI, SQLite, oito endpoints) e ADR 0002 (fila FIFO na reserva).
- `AGENTS.md` nas regras R01 a R08, em três commits.
- Feature em vibe: sócios, catálogo, reserva, fila e cancelamento com promoção.
- 25 testes passando, dos quais 14 espelham os cenários de catálogo e reserva.
- `docs/vibe-vs-spec/` com a cópia do código, as métricas e a conclusão da coluna vibe.

## Ordem no Git

| Commit | Papel |
| --- | --- |
| `054cedf` | repositório e Docker |
| `91bd063` | spec e cenários |
| `4bf582d` | ADRs |
| `4822a80` | AGENTS.md, regras de layout e dados |
| `7763ed7` | AGENTS.md, FIFO e reserva única |
| `4280aa3` | AGENTS.md, escopo vibe, e teste dos artefatos |
| `207bb07` | código da fila em `app/` |
| `de924a6` | métricas e cópia em `docs/vibe-vs-spec/` |

O primeiro commit de `app/` é `207bb07`, depois da spec.

## Métricas da passagem vibe

| Medida | Valor |
| --- | --- |
| Arquivos Python em `app/` | 8 |
| Linhas em `app/` | 418, das quais 173 em `app/service.py` |
| Linhas em `tests/` | 298 |
| Testes | 25 passando |
| Endpoints no ar | `POST /socios`, `POST /livros`, `GET /livros`, `POST /reservas`, `DELETE /reservas/{reserva_id}`, `GET /saude` |

## O que esta etapa deixou aberto de propósito

- Empréstimo, devolução e recomendação continuam só na spec.
- A comparação vibe × spec tem uma coluna. A outra abre com o plano da etapa 2.
- O grupo tem um integrante registrado e vagas em `docs/grupo.md`.
- Não há issue, plano, PR, CI, skill, MCP, threat model nem golden set. Cada um tem etapa própria.

## Como a etapa foi conferida

`docker compose run --rm api pytest -q` encerrou com 25 testes passando. Com a API no ar, uma reserva pronta e uma em espera foram criadas; ao cancelar a pronta, a espera foi promovida e o exemplar continuou ocupado.
