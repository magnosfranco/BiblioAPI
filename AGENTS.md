# AGENTS.md

Regras para agentes que alteram a BiblioAPI. Cada regra tem um jeito objetivo de ser conferida. Este arquivo começa pelo que já dá para exigir antes de existir código em `app/`.

## Contexto

A spec em `SPEC.md` é a referência de produto. Nesta etapa a spec, os cenários e as ADRs entram no Git antes de `app/`. A fatia que será codada em vibe é a fila de reservas: as invariantes abaixo já valem, mesmo sem o módulo existir.

## Regras

### R01 — Código de produção fica em app/

Módulo de produção é arquivo Python da API. Ele mora em `app/`. A raiz do repositório não tem `.py`.

Verificação: `tests/test_artefatos.py::test_r01_codigo_de_producao_fica_em_app`.

### R02 — Segredo e banco local ficam fora do Git

`.env` e `data/` estão no `.gitignore`. Email de exemplo usa o domínio `biblioteca.example.com`.

Verificação: `tests/test_artefatos.py::test_r02_gitignore_cobre_segredo_e_banco`.

### R04 — A fila é FIFO

Quem entra depois recebe posição maior. Cancelar o meio não troca a ordem de quem permanece.

Verificação: `tests/test_reservas.py::test_fila_conserva_a_ordem_de_chegada` e `tests/test_reservas.py::test_cancelar_quem_esta_no_meio_reordena_as_posicoes`.

### R05 — Uma reserva ativa por sócio e livro

Vale para status `pronta` e `aguardando`. Reserva cancelada não bloqueia uma nova.

Verificação: `tests/test_reservas.py::test_socio_nao_mantem_duas_reservas_ativas_do_mesmo_livro`.

### R07 — Teste mora em tests/

A suíte é `pytest`, com `testpaths = tests` no `pytest.ini`.

Verificação: `tests/test_artefatos.py::test_r07_pytest_aponta_para_tests`.

### R08 — Dado de exemplo é sintético

Emails em `features/` e `tests/` usam o sufixo `@biblioteca.example.com`. Não usar CPF, telefone ou cadastro real.

Verificação: `tests/test_artefatos.py::test_r08_emails_de_exemplo_sao_sinteticos`.

## Como alterar este arquivo

Uma mudança de regra é um commit próprio. Não apagar uma regra para fazer um teste passar: ajustar o código ou registrar uma ADR nova se a decisão mudou.
