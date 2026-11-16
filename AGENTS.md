# AGENTS.md

Regras para agentes que alteram a BiblioAPI. Cada regra tem um jeito objetivo de ser conferida. Este arquivo começa curto e ganha regra quando a etapa torna a regra necessária.

## Contexto

A spec em `SPEC.md` é a referência de produto. A fatia atual, feita em vibe, é sócios, catálogo e reservas. Empréstimos e recomendação já estão na spec e não devem ser implementados sem a etapa correspondente.

## Regras

### R01 — Código de produção fica em app/

Módulo de produção é arquivo Python da API. Ele mora em `app/`. A raiz do repositório não tem `.py`.

Verificação: `tests/test_artefatos.py::test_r01_codigo_de_producao_fica_em_app`.

### R02 — Segredo e banco local ficam fora do Git

`.env` e `data/` estão no `.gitignore`. Email de exemplo usa o domínio `biblioteca.example.com`.

Verificação: `tests/test_artefatos.py::test_r02_gitignore_cobre_segredo_e_banco`.

### R03 — Endpoint novo precisa estar na spec

Todo caminho publicado em `/openapi.json`, fora `GET /saude`, aparece em `SPEC.md` antes de ser tratado como parte do produto.

Verificação: `tests/test_openapi.py::test_r03_todo_caminho_de_negocio_esta_na_spec`.

### R04 — A fila é FIFO

Quem entra depois recebe posição maior. Cancelar o meio não troca a ordem de quem permanece.

Verificação: `tests/test_reservas.py::test_fila_conserva_a_ordem_de_chegada` e `tests/test_reservas.py::test_cancelar_quem_esta_no_meio_reordena_as_posicoes`.

### R05 — Uma reserva ativa por sócio e livro

Vale para status `pronta` e `aguardando`. Reserva cancelada não bloqueia uma nova.

Verificação: `tests/test_reservas.py::test_socio_nao_mantem_duas_reservas_ativas_do_mesmo_livro`.

### R06 — A passagem vibe não publica empréstimo nem recomendação

`POST /emprestimos` e `POST /recomendacoes` ficam na spec até as etapas spec + plano e LLM. Não adicionar essas rotas no código desta passagem.

Verificação: `tests/test_openapi.py::test_r06_openapi_nao_expoe_emprestimos_nem_recomendacoes`.

### R07 — Teste mora em tests/

A suíte é `pytest`, com `testpaths = tests` no `pytest.ini`.

Verificação: `tests/test_artefatos.py::test_r07_pytest_aponta_para_tests`.

### R08 — Dado de exemplo é sintético

Emails em `features/` e `tests/` usam o sufixo `@biblioteca.example.com`. Não usar CPF, telefone ou cadastro real.

Verificação: `tests/test_artefatos.py::test_r08_emails_de_exemplo_sao_sinteticos`.

## Como alterar este arquivo

Uma mudança de regra é um commit próprio, com a verificação no mesmo commit ou no commit de código imediatamente seguinte, quando a verificação depende de `app/`. Não apagar uma regra para fazer um teste passar: ajustar o código ou registrar uma ADR nova se a decisão mudou.
