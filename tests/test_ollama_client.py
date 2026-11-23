"""Cliente Ollama sem rede: sucesso, JSON inválido e timeout."""

from __future__ import annotations

import httpx
import pytest

from app.ollama_client import OllamaIndisponivel, completar_json


class _Resposta:
    def __init__(self, payload: dict) -> None:
        self._payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self._payload


def test_completar_json_aceita_content_string(monkeypatch: pytest.MonkeyPatch) -> None:
    def falso(*_args, **kwargs):
        assert kwargs["json"]["format"] == "json"
        assert kwargs["timeout"] == 2.0
        return _Resposta({"message": {"content": '{"itens": []}'}})

    monkeypatch.setattr("app.ollama_client.httpx.post", falso)
    assert completar_json("oi") == {"itens": []}


def test_completar_json_aceita_content_objeto(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.ollama_client.httpx.post",
        lambda *_a, **_k: _Resposta({"message": {"content": {"itens": [{"livro_id": 1}]}}}),
    )
    assert completar_json("oi")["itens"][0]["livro_id"] == 1


def test_completar_json_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    def falso(*_args, **_kwargs):
        raise httpx.ConnectError("recusou")

    monkeypatch.setattr("app.ollama_client.httpx.post", falso)
    with pytest.raises(OllamaIndisponivel):
        completar_json("oi")


def test_completar_json_http_500(monkeypatch: pytest.MonkeyPatch) -> None:
    pedido = httpx.Request("POST", "http://127.0.0.1:11434/api/chat")
    monkeypatch.setattr(
        "app.ollama_client.httpx.post",
        lambda *_a, **_k: httpx.Response(500, request=pedido),
    )
    with pytest.raises(OllamaIndisponivel):
        completar_json("oi")


def test_completar_json_lista_nao_objeto(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.ollama_client.httpx.post",
        lambda *_a, **_k: _Resposta({"message": {"content": "[1]"}}),
    )
    with pytest.raises(OllamaIndisponivel):
        completar_json("oi")


def test_completar_json_texto_quebrado(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "app.ollama_client.httpx.post",
        lambda *_a, **_k: _Resposta({"message": {"content": "nao-json"}}),
    )
    with pytest.raises(OllamaIndisponivel):
        completar_json("oi")
