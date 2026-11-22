"""POST/GET /livros — RN02/RN10."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_cadastrar_livro(client: TestClient) -> None:
    resp = client.post(
        "/livros",
        json={"titulo": "Dom Casmurro", "autor": "Machado de Assis", "exemplares": 3},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["exemplares"] == 3
    assert body["exemplares_disponiveis"] == 3


def test_exemplares_fora_intervalo_422(client: TestClient) -> None:
    resp = client.post(
        "/livros",
        json={"titulo": "Inválido", "autor": "X", "exemplares": 0},
    )
    assert resp.status_code == 422


def test_listar_com_exemplares_disponiveis(client: TestClient) -> None:
    client.post(
        "/livros",
        json={"titulo": "Dom Casmurro", "autor": "Machado de Assis", "exemplares": 2},
    )
    resp = client.get("/livros")
    assert resp.status_code == 200
    lista = resp.json()
    assert len(lista) == 1
    assert "exemplares_disponiveis" in lista[0]
    assert lista[0]["exemplares_disponiveis"] == 2
