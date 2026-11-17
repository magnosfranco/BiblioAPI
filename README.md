# BiblioAPI

API de biblioteca da disciplina IA na Engenharia de Software (ADLC): catálogo, reservas e fila de espera. Empréstimos e recomendação estão na spec e entram nas próximas etapas.

O ambiente padrão é o contêiner. Ele traz Python 3.11, Git e Node.js 18 ou superior. A ferramenta de agente roda no host. O Norton deste notebook inspeciona o HTTPS, e `docker/certs/` contém a raiz local que a imagem também confia, para o `pip` alcançar o PyPI.

## Rodar

Na raiz do repositório:

```bash
docker compose build
docker compose run --rm api pytest -q -o cache_dir=/tmp/pytest-cache
docker compose up api
```

Com a API no ar, a documentação interativa fica em <http://localhost:8000/docs> e o healthcheck em <http://localhost:8000/saude>. Para encerrar:

```bash
docker compose down
```

São quatro comandos. O banco SQLite fica num volume do Compose, não na pasta do projeto.

## O que esta etapa contém

A etapa após a Aula 1 deixa três evidências no histórico, nesta ordem: spec e cenários BDD, ADRs, e `AGENTS.md` evoluindo em mais de um commit. O código de `app/` vem depois. A fatia implementada em modo vibe é sócios, catálogo e reservas. Não há plano em `docs/plans/` para essa fatia. Empréstimos esperam esse plano.

| Caminho | Função |
| --- | --- |
| `SPEC.md` | contrato e regras |
| `features/` | cenários BDD |
| `docs/adr/` | decisões já aceitas |
| `AGENTS.md` | regras do agente |
| `docs/grupo.md` | papéis desta etapa |
| `docs/vibe-vs-spec/` | código, métricas e conclusão da passagem em vibe |
| `app/` | API da fatia em vibe |
| `tests/` | cenários automatizados e checagens dos artefatos |
| `docs/planejamento/` | requisitos, cronograma, atividades e premissas |

## Conferir o ambiente dentro da imagem

```bash
docker compose run --rm api python --version
docker compose run --rm api git --version
docker compose run --rm api node --version
```

Esses comandos só conferem a imagem. Não fazem parte dos quatro que sobem a API e os testes.
