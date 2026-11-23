"""BDD de POST /recomendacoes — Ollama mockado, sem rede."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from app.ollama_client import OllamaIndisponivel

FEATURE = Path(__file__).resolve().parents[1] / "features" / "recomendacoes.feature"
scenarios(str(FEATURE))


@pytest.fixture
def ctx() -> dict[str, Any]:
    return {}


@given(parsers.parse('que existe sócio "{email}"'))
def existe_socio(client: TestClient, ctx: dict[str, Any], email: str) -> None:
    ctx["socio_id"] = client.post(
        "/socios",
        json={"nome": "Ana Silva", "email": email},
    ).json()["id"]


@given("que o Ollama responde JSON válido de recomendações")
def ollama_valido(client: TestClient, ctx: dict[str, Any], monkeypatch: pytest.MonkeyPatch) -> None:
    livro_id = client.post(
        "/livros",
        json={"titulo": "Dom Casmurro", "autor": "Machado de Assis", "exemplares": 2},
    ).json()["id"]

    def falso(_prompt: str) -> dict[str, Any]:
        return {"itens": [{"livro_id": livro_id, "motivo": "clássico"}]}

    monkeypatch.setattr("app.service.consultar_ollama", falso)


@given("que o Ollama está indisponível ou em timeout")
def ollama_fora(client: TestClient, ctx: dict[str, Any], monkeypatch: pytest.MonkeyPatch) -> None:
    client.post(
        "/livros",
        json={"titulo": "Capitães da Areia", "autor": "Jorge Amado", "exemplares": 2},
    )

    def falso(_prompt: str) -> dict[str, Any]:
        raise OllamaIndisponivel("timeout")

    monkeypatch.setattr("app.service.consultar_ollama", falso)


@when("solicitar recomendações com limite 3")
def solicitar(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["resposta"] = client.post(
        "/recomendacoes",
        json={"socio_id": ctx["socio_id"], "limite": 3},
    )


@when("solicitar recomendações para sócio inexistente")
def solicitar_inexistente(client: TestClient, ctx: dict[str, Any]) -> None:
    ctx["resposta"] = client.post("/recomendacoes", json={"socio_id": 999999, "limite": 3})


@then(parsers.parse("a resposta deve ter status {code:d}"))
def status_http(ctx: dict[str, Any], code: int) -> None:
    assert ctx["resposta"].status_code == code


@then(parsers.parse('a origem deve ser "{origem}"'))
def origem_igual(ctx: dict[str, Any], origem: str) -> None:
    assert ctx["resposta"].json()["origem"] == origem


def test_limite_zero_rejeitado(client: TestClient) -> None:
    socio_id = client.post(
        "/socios",
        json={"nome": "Ana", "email": "ana.limite@biblioteca.example.com"},
    ).json()["id"]
    resposta = client.post("/recomendacoes", json={"socio_id": socio_id, "limite": 0})
    assert resposta.status_code == 422
