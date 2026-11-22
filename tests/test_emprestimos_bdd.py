"""pytest-bdd — todos os cenários de features/emprestimos.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

FEATURE = Path(__file__).resolve().parents[1] / "features" / "emprestimos.feature"
scenarios(str(FEATURE))


@pytest.fixture()
def ctx() -> dict[str, Any]:
    return {
        "socio_id": None,
        "livro_id": None,
        "reserva_id": None,
        "reserva_fila_id": None,
        "emprestimo_id": None,
        "response": None,
        "livros": None,
        "disponiveis_antes": None,
    }


def _ensure_socio(client: TestClient, ctx: dict[str, Any], email: str = "ana.silva@biblioteca.example.com") -> int:
    if ctx["socio_id"] is None:
        ctx["socio_id"] = client.post(
            "/socios", json={"nome": "Ana Silva", "email": email}
        ).json()["id"]
    return int(ctx["socio_id"])


def _ensure_livro(client: TestClient, ctx: dict[str, Any], exemplares: int = 1) -> int:
    if ctx["livro_id"] is None:
        ctx["livro_id"] = client.post(
            "/livros",
            json={"titulo": "Dom Casmurro", "autor": "Machado de Assis", "exemplares": exemplares},
        ).json()["id"]
    return int(ctx["livro_id"])


@given("que o sócio possui reserva \"pronta\" para o livro")
def socio_com_pronta(client: TestClient, ctx: dict[str, Any]) -> None:
    socio_id = _ensure_socio(client, ctx)
    livro_id = _ensure_livro(client, ctx, exemplares=1)
    resp = client.post("/reservas", json={"socio_id": socio_id, "livro_id": livro_id})
    assert resp.status_code == 201
    assert resp.json()["status"] == "pronta"
    ctx["reserva_id"] = resp.json()["id"]


@given("que exemplares_disponiveis do livro é 0")
def disponiveis_zero(client: TestClient, ctx: dict[str, Any]) -> None:
    socio_id = _ensure_socio(client, ctx)
    livro_id = _ensure_livro(client, ctx, exemplares=1)
    # Se ainda não há consumidor do exemplar, cria reserva de outro sócio ou empréstimo
    livros = client.get("/livros").json()
    atual = next(x for x in livros if x["id"] == livro_id)["exemplares_disponiveis"]
    if atual > 0:
        outro = client.post(
            "/socios",
            json={"nome": "Bruno", "email": "bruno.zero@biblioteca.example.com"},
        ).json()["id"]
        # Consome via reserva pronta do próprio se ainda não tiver; senão empréstimo direto outro
        if ctx.get("reserva_id"):
            # pronta do sócio já zera disponiveis (1 exemplar)
            pass
        else:
            client.post("/emprestimos", json={"socio_id": outro, "livro_id": livro_id})
    livros = client.get("/livros").json()
    assert next(x for x in livros if x["id"] == livro_id)["exemplares_disponiveis"] == 0
    _ = socio_id


@given("que o sócio possui apenas reserva \"aguardando\" para o livro")
def socio_so_aguardando(client: TestClient, ctx: dict[str, Any]) -> None:
    s1 = client.post(
        "/socios", json={"nome": "Carla", "email": "carla.fila@biblioteca.example.com"}
    ).json()["id"]
    livro_id = _ensure_livro(client, ctx, exemplares=1)
    client.post("/reservas", json={"socio_id": s1, "livro_id": livro_id})  # pronta
    socio_id = _ensure_socio(client, ctx, "ana.aguardando@biblioteca.example.com")
    resp = client.post("/reservas", json={"socio_id": socio_id, "livro_id": livro_id})
    assert resp.json()["status"] == "aguardando"
    ctx["reserva_id"] = resp.json()["id"]


@given("que o sócio não possui reserva ativa para o livro")
def socio_sem_reserva_ativa(client: TestClient, ctx: dict[str, Any]) -> None:
    _ensure_socio(client, ctx)
    # Livro é definido pelos steps de disponibilidade seguintes.


@given("que exemplares_disponiveis do livro é maior que 0")
def disponiveis_maior_que_zero(client: TestClient, ctx: dict[str, Any]) -> None:
    if ctx["livro_id"] is None:
        ctx["livro_id"] = client.post(
            "/livros",
            json={"titulo": "Dom Casmurro", "autor": "Machado de Assis", "exemplares": 2},
        ).json()["id"]
    livro_id = int(ctx["livro_id"])
    disp = next(x for x in client.get("/livros").json() if x["id"] == livro_id)[
        "exemplares_disponiveis"
    ]
    assert disp > 0


@given("que o sócio não possui reserva \"pronta\" para o livro")
def socio_sem_pronta(client: TestClient, ctx: dict[str, Any]) -> None:
    _ensure_socio(client, ctx, "ana.sempronta@biblioteca.example.com")
    livro_id = _ensure_livro(client, ctx, exemplares=1)
    # Outro sócio segura a pronta / consome disponibilidade
    outro = client.post(
        "/socios", json={"nome": "Outro", "email": "outro.sempronta@biblioteca.example.com"}
    ).json()["id"]
    client.post("/emprestimos", json={"socio_id": outro, "livro_id": livro_id})


@given("que já existe empréstimo \"aberto\" do sócio para o livro")
def ja_existe_aberto(client: TestClient, ctx: dict[str, Any]) -> None:
    socio_id = _ensure_socio(client, ctx)
    livro_id = _ensure_livro(client, ctx, exemplares=2)
    resp = client.post("/emprestimos", json={"socio_id": socio_id, "livro_id": livro_id})
    assert resp.status_code == 201
    ctx["emprestimo_id"] = resp.json()["id"]


@given(parsers.parse('que existe sócio "{email}"'))
def existe_socio_email(client: TestClient, ctx: dict[str, Any], email: str) -> None:
    ctx["socio_id"] = client.post("/socios", json={"nome": "Ana", "email": email}).json()["id"]


@given("que exemplares_disponiveis do livro é 1")
def disponiveis_um(client: TestClient, ctx: dict[str, Any]) -> None:
    # Sempre cria livro com 1 exemplar disponível (não reaproveita livro com N≠1).
    ctx["livro_id"] = client.post(
        "/livros",
        json={"titulo": "Memórias Póstumas", "autor": "Machado de Assis", "exemplares": 1},
    ).json()["id"]
    assert next(x for x in client.get("/livros").json() if x["id"] == ctx["livro_id"])[
        "exemplares_disponiveis"
    ] == 1


@given('empréstimo "aberto" e reserva "aguardando" posição 1 no mesmo livro')
def aberto_e_aguardando(client: TestClient, ctx: dict[str, Any]) -> None:
    s1 = _ensure_socio(client, ctx, "ana.promo@biblioteca.example.com")
    livro_id = _ensure_livro(client, ctx, exemplares=1)
    emp = client.post("/emprestimos", json={"socio_id": s1, "livro_id": livro_id})
    assert emp.status_code == 201
    ctx["emprestimo_id"] = emp.json()["id"]
    s2 = client.post(
        "/socios", json={"nome": "Bruno", "email": "bruno.promo@biblioteca.example.com"}
    ).json()["id"]
    reserva = client.post("/reservas", json={"socio_id": s2, "livro_id": livro_id}).json()
    assert reserva["status"] == "aguardando"
    assert reserva["posicao"] == 1
    ctx["reserva_fila_id"] = reserva["id"]


@given("empréstimo \"aberto\" sem outros consumidores do exemplar")
def aberto_sem_consumidores(client: TestClient, ctx: dict[str, Any]) -> None:
    socio_id = _ensure_socio(client, ctx, "ana.devol@biblioteca.example.com")
    livro_id = _ensure_livro(client, ctx, exemplares=1)
    ctx["disponiveis_antes"] = next(
        x for x in client.get("/livros").json() if x["id"] == livro_id
    )["exemplares_disponiveis"]
    emp = client.post("/emprestimos", json={"socio_id": socio_id, "livro_id": livro_id})
    ctx["emprestimo_id"] = emp.json()["id"]


@given('empréstimo com status "devolvido"')
def emprestimo_ja_devolvido(client: TestClient, ctx: dict[str, Any]) -> None:
    socio_id = _ensure_socio(client, ctx, "ana.dupdev@biblioteca.example.com")
    livro_id = _ensure_livro(client, ctx, exemplares=1)
    emp_id = client.post("/emprestimos", json={"socio_id": socio_id, "livro_id": livro_id}).json()[
        "id"
    ]
    client.post(f"/emprestimos/{emp_id}/devolucao")
    ctx["emprestimo_id"] = emp_id


@when("criar empréstimo do sócio para o livro")
def criar_emprestimo(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["response"] = client.post(
        "/emprestimos",
        json={"socio_id": ctx["socio_id"], "livro_id": ctx["livro_id"]},
    )
    if ctx["response"].status_code == 201:
        ctx["emprestimo_id"] = ctx["response"].json()["id"]


@when("criar novamente empréstimo do mesmo sócio para o mesmo livro")
def criar_emprestimo_de_novo(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["response"] = client.post(
        "/emprestimos",
        json={"socio_id": ctx["socio_id"], "livro_id": ctx["livro_id"]},
    )


@when("criar empréstimo para sócio inexistente")
def emprestimo_socio_inexistente(client: TestClient, ctx: dict[str, Any]) -> None:
    livro_id = _ensure_livro(client, ctx)
    ctx["response"] = client.post("/emprestimos", json={"socio_id": 99999, "livro_id": livro_id})


@when("criar empréstimo do sócio para livro inexistente")
def emprestimo_livro_inexistente(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["response"] = client.post(
        "/emprestimos", json={"socio_id": ctx["socio_id"], "livro_id": 99999}
    )


@when("listar os livros")
def listar_livros(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["livros"] = client.get("/livros").json()


@when("devolver o empréstimo")
def devolver_emprestimo(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["response"] = client.post(f"/emprestimos/{ctx['emprestimo_id']}/devolucao")


@when("devolver o empréstimo novamente")
def devolver_novamente(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["response"] = client.post(f"/emprestimos/{ctx['emprestimo_id']}/devolucao")


@when("devolver empréstimo inexistente")
def devolver_inexistente(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["response"] = client.post("/emprestimos/99999/devolucao")


@then(parsers.parse("a resposta deve ter status {code:d}"))
def resposta_status(ctx: dict[str, Any], code: int) -> None:
    assert ctx["response"].status_code == code


@then(parsers.parse('a reserva deve ficar "{status}"'))
def reserva_status(client: TestClient, ctx: dict[str, Any], status: str) -> None:
    from app import db as app_db

    conn = app_db.connect()
    try:
        row = conn.execute(
            "SELECT status FROM reservas WHERE id = ?", (ctx["reserva_id"],)
        ).fetchone()
        assert row["status"] == status
    finally:
        conn.close()


@then(parsers.parse('o empréstimo deve ficar "{status}"'))
def emprestimo_status(ctx: dict[str, Any], status: str) -> None:
    body = ctx["response"].json()
    assert body["status"] == status
    if status == "aberto":
        ctx["emprestimo_id"] = body["id"]


@then("o empréstimo deve referenciar a reserva consumida")
def emprestimo_ref_reserva(ctx: dict[str, Any]) -> None:
    assert ctx["response"].json()["reserva_id"] == ctx["reserva_id"]


@then("reserva_id do empréstimo deve ser nulo")
def reserva_id_nulo(ctx: dict[str, Any]) -> None:
    assert ctx["response"].json()["reserva_id"] is None


@then("exemplares_disponiveis do livro deve ser 0")
def disponiveis_deve_ser_zero(ctx: dict[str, Any]) -> None:
    livro = next(x for x in ctx["livros"] if x["id"] == ctx["livro_id"])
    assert livro["exemplares_disponiveis"] == 0


@then('a reserva da posição 1 deve ficar "pronta"')
def reserva_pos1_pronta(client: TestClient, ctx: dict[str, Any]) -> None:
    from app import db as app_db

    conn = app_db.connect()
    try:
        row = conn.execute(
            "SELECT status, posicao FROM reservas WHERE id = ?",
            (ctx["reserva_fila_id"],),
        ).fetchone()
        assert row["status"] == "pronta"
        assert row["posicao"] is None
    finally:
        conn.close()


@then("exemplares_disponiveis do livro deve ter aumentado em 1")
def disponiveis_aumentou(ctx: dict[str, Any]) -> None:
    livro = next(x for x in ctx["livros"] if x["id"] == ctx["livro_id"])
    assert livro["exemplares_disponiveis"] == ctx["disponiveis_antes"]
