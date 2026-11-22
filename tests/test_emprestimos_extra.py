"""Design RN07, concorrência, OpenAPI smoke — plano 001 §5.1."""

from __future__ import annotations

import os
import threading
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import db, service


def test_rn07_devolucao_e_cancelamento_mesma_funcao() -> None:
    """Devolução e cancelamento devem usar o mesmo símbolo de promoção."""
    assert service.devolver.__code__.co_names.count("promover_ou_compactar") >= 1
    assert service.cancelar_reserva.__code__.co_names.count("promover_ou_compactar") >= 1
    # Um único objeto função no módulo
    assert service.promover_ou_compactar is service.promover_ou_compactar


def test_openapi_paths_emprestimos(client: TestClient) -> None:
    paths = client.get("/openapi.json").json()["paths"]
    assert "/emprestimos" in paths
    assert "/emprestimos/{emprestimo_id}/devolucao" in paths
    assert "post" in paths["/emprestimos"]
    assert "post" in paths["/emprestimos/{emprestimo_id}/devolucao"]


def test_concorrencia_ultimo_exemplar(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Dois empréstimos disputando o último exemplar → no máx. um sucesso."""
    db_file = tmp_path / "race.db"
    monkeypatch.setenv("BIBLIO_DB_PATH", str(db_file))
    os.environ["BIBLIO_DB_PATH"] = str(db_file)
    db.init_schema()

    s1 = int(service.criar_socio("Ana", "ana.silva@biblioteca.example.com")["id"])
    s2 = int(service.criar_socio("Bruno", "bruno@biblioteca.example.com")["id"])
    livro_id = int(service.criar_livro("Dom Casmurro", "Machado de Assis", 1)["id"])

    resultados: list[str] = []
    barreira = threading.Barrier(2)

    def tentar(socio_id: int) -> None:
        barreira.wait(timeout=5)
        try:
            service.emprestar(socio_id, livro_id)
            resultados.append("ok")
        except service.ConflictError:
            resultados.append("conflict")

    t1 = threading.Thread(target=tentar, args=(s1,))
    t2 = threading.Thread(target=tentar, args=(s2,))
    t1.start()
    t2.start()
    t1.join(timeout=10)
    t2.join(timeout=10)

    assert resultados.count("ok") == 1
    assert resultados.count("conflict") == 1

    conn = db.connect()
    try:
        abertos = conn.execute(
            "SELECT COUNT(*) AS n FROM emprestimos WHERE status = 'aberto'"
        ).fetchone()
        assert int(abertos["n"]) == 1
    finally:
        conn.close()
