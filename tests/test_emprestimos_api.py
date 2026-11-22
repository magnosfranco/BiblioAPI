"""API TestClient — status codes e corpo mínimo OpenAPI."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _socio(client: TestClient, email: str, nome: str = "Sócio") -> int:
    return client.post("/socios", json={"nome": nome, "email": email}).json()["id"]


def _livro(client: TestClient, exemplares: int = 1) -> int:
    return client.post(
        "/livros",
        json={"titulo": "Dom Casmurro", "autor": "Machado de Assis", "exemplares": exemplares},
    ).json()["id"]


def test_post_emprestimo_201_direto(client: TestClient) -> None:
    socio_id = _socio(client, "ana.silva@biblioteca.example.com")
    livro_id = _livro(client, 1)
    resp = client.post("/emprestimos", json={"socio_id": socio_id, "livro_id": livro_id})
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "aberto"
    assert body["reserva_id"] is None
    assert body["devolvido_em"] is None
    assert "emprestado_em" in body


def test_post_emprestimo_consome_pronta(client: TestClient) -> None:
    socio_id = _socio(client, "ana.silva@biblioteca.example.com")
    livro_id = _livro(client, 1)
    reserva = client.post("/reservas", json={"socio_id": socio_id, "livro_id": livro_id}).json()
    resp = client.post("/emprestimos", json={"socio_id": socio_id, "livro_id": livro_id})
    assert resp.status_code == 201
    assert resp.json()["reserva_id"] == reserva["id"]


def test_post_emprestimo_409_aguardando(client: TestClient) -> None:
    s1 = _socio(client, "ana.silva@biblioteca.example.com", "Ana")
    s2 = _socio(client, "bruno@biblioteca.example.com", "Bruno")
    livro_id = _livro(client, 1)
    client.post("/reservas", json={"socio_id": s1, "livro_id": livro_id})
    client.post("/reservas", json={"socio_id": s2, "livro_id": livro_id})
    resp = client.post("/emprestimos", json={"socio_id": s2, "livro_id": livro_id})
    assert resp.status_code == 409


def test_post_emprestimo_404(client: TestClient) -> None:
    assert client.post("/emprestimos", json={"socio_id": 1, "livro_id": 1}).status_code == 404


def test_devolucao_200_e_409(client: TestClient) -> None:
    socio_id = _socio(client, "ana.silva@biblioteca.example.com")
    livro_id = _livro(client, 1)
    emp_id = client.post("/emprestimos", json={"socio_id": socio_id, "livro_id": livro_id}).json()["id"]
    resp = client.post(f"/emprestimos/{emp_id}/devolucao")
    assert resp.status_code == 200
    assert resp.json()["status"] == "devolvido"
    assert resp.json()["devolvido_em"] is not None
    assert client.post(f"/emprestimos/{emp_id}/devolucao").status_code == 409


def test_devolucao_404(client: TestClient) -> None:
    assert client.post("/emprestimos/9999/devolucao").status_code == 404


def test_rn10_apos_emprestar_e_devolver(client: TestClient) -> None:
    socio_id = _socio(client, "ana.silva@biblioteca.example.com")
    livro_id = _livro(client, 1)
    before = client.get("/livros").json()[0]["exemplares_disponiveis"]
    assert before == 1
    emp_id = client.post("/emprestimos", json={"socio_id": socio_id, "livro_id": livro_id}).json()["id"]
    mid = next(x for x in client.get("/livros").json() if x["id"] == livro_id)
    assert mid["exemplares_disponiveis"] == 0
    client.post(f"/emprestimos/{emp_id}/devolucao")
    after = next(x for x in client.get("/livros").json() if x["id"] == livro_id)
    assert after["exemplares_disponiveis"] == 1
