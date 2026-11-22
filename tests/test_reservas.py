"""POST/DELETE /reservas — FIFO RN03–RN09."""

from __future__ import annotations

from fastapi.testclient import TestClient


def _socio(client: TestClient, email: str, nome: str = "Sócio") -> int:
    return client.post("/socios", json={"nome": nome, "email": email}).json()["id"]


def _livro(client: TestClient, exemplares: int = 1) -> int:
    return client.post(
        "/livros",
        json={
            "titulo": "Dom Casmurro",
            "autor": "Machado de Assis",
            "exemplares": exemplares,
        },
    ).json()["id"]


def test_reserva_pronta_quando_ha_disponivel(client: TestClient) -> None:
    socio_id = _socio(client, "ana.silva@biblioteca.example.com")
    livro_id = _livro(client, exemplares=1)
    resp = client.post("/reservas", json={"socio_id": socio_id, "livro_id": livro_id})
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "pronta"
    assert body["posicao"] is None


def test_reserva_aguardando_quando_sem_disponivel(client: TestClient) -> None:
    socio_a = _socio(client, "ana.silva@biblioteca.example.com", "Ana")
    livro_id = _livro(client, exemplares=1)
    client.post("/reservas", json={"socio_id": socio_a, "livro_id": livro_id})

    socio_b = _socio(client, "bruno@biblioteca.example.com", "Bruno")
    resp = client.post("/reservas", json={"socio_id": socio_b, "livro_id": livro_id})
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "aguardando"
    assert body["posicao"] == 1


def test_segunda_aguardando_posicao_2(client: TestClient) -> None:
    s1 = _socio(client, "ana.silva@biblioteca.example.com", "Ana")
    s2 = _socio(client, "bruno@biblioteca.example.com", "Bruno")
    s3 = _socio(client, "carla@biblioteca.example.com", "Carla")
    livro_id = _livro(client, exemplares=1)
    client.post("/reservas", json={"socio_id": s1, "livro_id": livro_id})  # pronta
    client.post("/reservas", json={"socio_id": s2, "livro_id": livro_id})  # aguardando 1
    resp = client.post("/reservas", json={"socio_id": s3, "livro_id": livro_id})
    assert resp.status_code == 201
    assert resp.json()["status"] == "aguardando"
    assert resp.json()["posicao"] == 2


def test_reserva_ativa_duplicada_409(client: TestClient) -> None:
    socio_id = _socio(client, "ana.silva@biblioteca.example.com")
    livro_id = _livro(client, exemplares=2)
    assert client.post("/reservas", json={"socio_id": socio_id, "livro_id": livro_id}).status_code == 201
    resp = client.post("/reservas", json={"socio_id": socio_id, "livro_id": livro_id})
    assert resp.status_code == 409


def test_cancelar_aguardando_compacta(client: TestClient) -> None:
    s1 = _socio(client, "ana.silva@biblioteca.example.com", "Ana")
    s2 = _socio(client, "bruno@biblioteca.example.com", "Bruno")
    s3 = _socio(client, "carla@biblioteca.example.com", "Carla")
    livro_id = _livro(client, exemplares=1)
    client.post("/reservas", json={"socio_id": s1, "livro_id": livro_id})  # pronta
    r2 = client.post("/reservas", json={"socio_id": s2, "livro_id": livro_id}).json()
    r3 = client.post("/reservas", json={"socio_id": s3, "livro_id": livro_id}).json()
    assert r2["posicao"] == 1 and r3["posicao"] == 2

    resp = client.delete(f"/reservas/{r2['id']}")
    assert resp.status_code == 204

    from app import db as app_db

    conn = app_db.connect()
    try:
        pos_r3 = conn.execute(
            "SELECT posicao, status FROM reservas WHERE id = ?",
            (r3["id"],),
        ).fetchone()
        assert pos_r3["status"] == "aguardando"
        assert pos_r3["posicao"] == 1
    finally:
        conn.close()

    s4 = _socio(client, "diego@biblioteca.example.com", "Diego")
    nova = client.post("/reservas", json={"socio_id": s4, "livro_id": livro_id}).json()
    assert nova["status"] == "aguardando"
    assert nova["posicao"] == 2


def test_cancelar_pronta_promove_primeiro(client: TestClient) -> None:
    s1 = _socio(client, "ana.silva@biblioteca.example.com", "Ana")
    s2 = _socio(client, "bruno@biblioteca.example.com", "Bruno")
    livro_id = _livro(client, exemplares=1)
    r1 = client.post("/reservas", json={"socio_id": s1, "livro_id": livro_id}).json()
    r2 = client.post("/reservas", json={"socio_id": s2, "livro_id": livro_id}).json()
    assert r1["status"] == "pronta"
    assert r2["status"] == "aguardando" and r2["posicao"] == 1

    assert client.delete(f"/reservas/{r1['id']}").status_code == 204

    # Após promoção, s2 está pronta: nova reserva de s1 (sem ativa) deve aguardar
    nova = client.post("/reservas", json={"socio_id": s1, "livro_id": livro_id}).json()
    assert nova["status"] == "aguardando"
    assert nova["posicao"] == 1

    # Disponíveis: 1 exemplar − 1 pronta = 0
    livros = client.get("/livros").json()
    assert livros[0]["exemplares_disponiveis"] == 0


def test_reserva_socio_inexistente_404(client: TestClient) -> None:
    livro_id = _livro(client, exemplares=1)
    resp = client.post("/reservas", json={"socio_id": 9999, "livro_id": livro_id})
    assert resp.status_code == 404


def test_cancelar_inexistente_404(client: TestClient) -> None:
    resp = client.delete("/reservas/9999")
    assert resp.status_code == 404
