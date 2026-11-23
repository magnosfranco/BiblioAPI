"""O seed de exemplo é idempotente e não chama o Ollama."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.popular_base import popular


@pytest.fixture()
def base_limpa(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BIBLIO_DB_PATH", str(tmp_path / "seed.db"))


def test_popular_duas_vezes_nao_duplica(base_limpa: None) -> None:
    primeiro = popular()
    segundo = popular()
    assert primeiro["ja_existia"] is False
    assert primeiro["livros_novos"] == 8
    assert primeiro["emprestimos"] > 0
    assert segundo["ja_existia"] is True
    assert segundo["livros_novos"] == 0
    assert segundo["emprestimos"] == 0
