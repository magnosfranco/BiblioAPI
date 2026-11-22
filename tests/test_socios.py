"""POST /socios — RN01."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_cadastrar_socio(client: TestClient) -> None:
    resp = client.post(
        "/socios",
        json={"nome": "Ana Silva", "email": "ana.silva@biblioteca.example.com"},
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "ana.silva@biblioteca.example.com"
    assert body["nome"] == "Ana Silva"
    assert "id" in body


def test_email_duplicado_case_insensitive(client: TestClient) -> None:
    client.post(
        "/socios",
        json={"nome": "Ana Silva", "email": "ana.silva@biblioteca.example.com"},
    )
    resp = client.post(
        "/socios",
        json={"nome": "Ana Outra", "email": "Ana.Silva@biblioteca.example.com"},
    )
    assert resp.status_code == 409


def test_nome_vazio_422(client: TestClient) -> None:
    resp = client.post(
        "/socios",
        json={"nome": "  ", "email": "vazio@biblioteca.example.com"},
    )
    assert resp.status_code == 422
