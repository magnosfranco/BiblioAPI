"""Conexão SQLite e DDL (sqlite3 permitido só aqui e em service.py)."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parents[1] / "data" / "biblio.db"


def get_db_path() -> Path:
    raw = os.environ.get("BIBLIO_DB_PATH")
    if raw:
        return Path(raw)
    return DEFAULT_DB_PATH


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_schema(conn: sqlite3.Connection | None = None) -> None:
    owns = conn is None
    if owns:
        conn = connect()
    assert conn is not None
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS socios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                criado_em TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now'))
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_socios_email_lower
                ON socios (lower(trim(email)));

            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                exemplares INTEGER NOT NULL CHECK (exemplares BETWEEN 1 AND 50),
                criado_em TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now'))
            );

            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                socio_id INTEGER NOT NULL REFERENCES socios(id),
                livro_id INTEGER NOT NULL REFERENCES livros(id),
                status TEXT NOT NULL CHECK (
                    status IN ('pronta', 'aguardando', 'atendida', 'cancelada')
                ),
                posicao INTEGER,
                criado_em TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now')),
                CHECK (
                    (status = 'aguardando' AND posicao IS NOT NULL AND posicao >= 1)
                    OR (status <> 'aguardando' AND posicao IS NULL)
                )
            );

            CREATE TABLE IF NOT EXISTS emprestimos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                socio_id INTEGER NOT NULL REFERENCES socios(id),
                livro_id INTEGER NOT NULL REFERENCES livros(id),
                reserva_id INTEGER REFERENCES reservas(id),
                status TEXT NOT NULL CHECK (status IN ('aberto', 'devolvido')),
                emprestado_em TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now')),
                devolvido_em TEXT
            );
            """
        )
        conn.commit()
    finally:
        if owns:
            conn.close()
