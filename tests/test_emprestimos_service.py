"""Camada service — ramos RN11/RN12 com SQLite temporário."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from app import db, service


@pytest.fixture()
def db_ready(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_file = tmp_path / "service.db"
    monkeypatch.setenv("BIBLIO_DB_PATH", str(db_file))
    os.environ["BIBLIO_DB_PATH"] = str(db_file)
    db.init_schema()


def _socio(email: str = "ana.silva@biblioteca.example.com") -> int:
    return int(service.criar_socio("Ana", email)["id"])


def _livro(exemplares: int = 1) -> int:
    return int(service.criar_livro("Dom Casmurro", "Machado de Assis", exemplares)["id"])


def test_emprestar_consome_pronta(db_ready: None) -> None:
    socio_id = _socio()
    livro_id = _livro(1)
    reserva = service.criar_reserva(socio_id, livro_id)
    assert reserva["status"] == "pronta"
    emp = service.emprestar(socio_id, livro_id)
    assert emp["status"] == "aberto"
    assert emp["reserva_id"] == reserva["id"]
    conn = db.connect()
    try:
        st = conn.execute("SELECT status FROM reservas WHERE id = ?", (reserva["id"],)).fetchone()
        assert st["status"] == "atendida"
    finally:
        conn.close()


def test_emprestar_pronta_com_disponiveis_zero(db_ready: None) -> None:
    """RN11-(4): pronta já 'segura' o exemplar → disponiveis pode ser 0."""
    s1 = _socio("ana.silva@biblioteca.example.com")
    s2 = _socio("bruno@biblioteca.example.com")
    livro_id = _livro(1)
    service.criar_reserva(s1, livro_id)  # pronta
    service.criar_reserva(s2, livro_id)  # aguardando
    conn = db.connect()
    try:
        assert service.exemplares_disponiveis(conn, livro_id) == 0
    finally:
        conn.close()
    emp = service.emprestar(s1, livro_id)
    assert emp["status"] == "aberto"
    assert emp["reserva_id"] is not None


def test_emprestar_bloqueia_aguardando(db_ready: None) -> None:
    s1 = _socio("ana.silva@biblioteca.example.com")
    s2 = _socio("bruno@biblioteca.example.com")
    livro_id = _livro(1)
    service.criar_reserva(s1, livro_id)
    service.criar_reserva(s2, livro_id)
    with pytest.raises(service.ConflictError):
        service.emprestar(s2, livro_id)


def test_emprestar_direto(db_ready: None) -> None:
    socio_id = _socio()
    livro_id = _livro(2)
    emp = service.emprestar(socio_id, livro_id)
    assert emp["reserva_id"] is None
    assert emp["status"] == "aberto"


def test_emprestar_sem_pronta_sem_disponivel(db_ready: None) -> None:
    s1 = _socio("ana.silva@biblioteca.example.com")
    s2 = _socio("bruno@biblioteca.example.com")
    livro_id = _livro(1)
    service.emprestar(s1, livro_id)  # direto
    with pytest.raises(service.ConflictError):
        service.emprestar(s2, livro_id)


def test_segundo_aberto_409(db_ready: None) -> None:
    socio_id = _socio()
    livro_id = _livro(2)
    service.emprestar(socio_id, livro_id)
    with pytest.raises(service.ConflictError):
        service.emprestar(socio_id, livro_id)


def test_emprestar_socio_inexistente(db_ready: None) -> None:
    livro_id = _livro()
    with pytest.raises(service.NotFoundError):
        service.emprestar(9999, livro_id)


def test_emprestar_livro_inexistente(db_ready: None) -> None:
    socio_id = _socio()
    with pytest.raises(service.NotFoundError):
        service.emprestar(socio_id, 9999)


def test_devolver_promove_fila(db_ready: None) -> None:
    s1 = _socio("ana.silva@biblioteca.example.com")
    s2 = _socio("bruno@biblioteca.example.com")
    livro_id = _livro(1)
    emp = service.emprestar(s1, livro_id)
    reserva = service.criar_reserva(s2, livro_id)
    assert reserva["status"] == "aguardando"
    out = service.devolver(int(emp["id"]))
    assert out["status"] == "devolvido"
    assert out["devolvido_em"] is not None
    conn = db.connect()
    try:
        st = conn.execute("SELECT status, posicao FROM reservas WHERE id = ?", (reserva["id"],)).fetchone()
        assert st["status"] == "pronta"
        assert st["posicao"] is None
    finally:
        conn.close()


def test_devolver_ja_devolvido(db_ready: None) -> None:
    socio_id = _socio()
    livro_id = _livro()
    emp = service.emprestar(socio_id, livro_id)
    service.devolver(int(emp["id"]))
    with pytest.raises(service.ConflictError):
        service.devolver(int(emp["id"]))


def test_devolver_inexistente(db_ready: None) -> None:
    with pytest.raises(service.NotFoundError):
        service.devolver(9999)
