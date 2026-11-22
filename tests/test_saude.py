"""GET /saude."""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_saude_ok(client: TestClient) -> None:
    resp = client.get("/saude")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
