"""Fixtures HTTP com SQLite isolado por teste."""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Generator[TestClient, None, None]:
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("BIBLIO_DB_PATH", str(db_file))
    # Garante que módulos já importados vejam o path novo
    os.environ["BIBLIO_DB_PATH"] = str(db_file)

    from app import db
    from app.main import app

    db.init_schema()
    with TestClient(app) as test_client:
        yield test_client
