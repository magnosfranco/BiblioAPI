"""Cliente HTTP do Ollama. Sem SQL e sem regra de negócio."""

from __future__ import annotations

import json
import os
from typing import Any

import httpx

DEFAULT_TIMEOUT_S = 2.0


class OllamaIndisponivel(Exception):
    """Timeout, HTTP, JSON inválido ou corpo que não é um objeto."""


def completar_json(prompt: str) -> dict[str, Any]:
    """POST /api/chat com format=json e timeout curto (RN13)."""
    base = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
    timeout = float(os.environ.get("OLLAMA_TIMEOUT", str(DEFAULT_TIMEOUT_S)))
    payload = {
        "model": model,
        "stream": False,
        "format": "json",
        "messages": [{"role": "user", "content": prompt}],
        "options": {"temperature": 0},
    }
    try:
        response = httpx.post(f"{base}/api/chat", json=payload, timeout=timeout)
        response.raise_for_status()
        body = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise OllamaIndisponivel("Ollama indisponível ou resposta inválida") from exc

    content = (body.get("message") or {}).get("content")
    if isinstance(content, dict):
        return content
    if not isinstance(content, str) or not content.strip():
        raise OllamaIndisponivel("Ollama não devolveu JSON")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError as exc:
        raise OllamaIndisponivel("JSON do Ollama não parseia") from exc
    if not isinstance(parsed, dict):
        raise OllamaIndisponivel("JSON do Ollama não é objeto")
    return parsed
