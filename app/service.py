"""Regras de negócio + SQL (sqlite3 permitido só aqui e em db.py)."""

from __future__ import annotations

import sqlite3
from typing import Any

from app import db


class NotFoundError(Exception):
    def __init__(self, message: str = "não encontrado") -> None:
        self.message = message
        super().__init__(message)


class ConflictError(Exception):
    def __init__(self, message: str = "conflito") -> None:
        self.message = message
        super().__init__(message)


def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)


def _get_conn() -> sqlite3.Connection:
    return db.connect()


def exemplares_disponiveis(conn: sqlite3.Connection, livro_id: int) -> int:
    """RN10: exemplares − #pronta − #emprestimos_abertos."""
    row = conn.execute(
        """
        SELECT
            l.exemplares
            - (
                SELECT COUNT(*) FROM reservas r
                WHERE r.livro_id = l.id AND r.status = 'pronta'
            )
            - (
                SELECT COUNT(*) FROM emprestimos e
                WHERE e.livro_id = l.id AND e.status = 'aberto'
            ) AS disponiveis
        FROM livros l
        WHERE l.id = ?
        """,
        (livro_id,),
    ).fetchone()
    if row is None:
        raise NotFoundError("livro não encontrado")
    return int(row["disponiveis"])


def promover_ou_compactar(conn: sqlite3.Connection, livro_id: int) -> None:
    """RN07: promoção (pos 1 → pronta) + renumeração da fila aguardando."""
    primeiro = conn.execute(
        """
        SELECT id FROM reservas
        WHERE livro_id = ? AND status = 'aguardando'
        ORDER BY posicao ASC
        LIMIT 1
        """,
        (livro_id,),
    ).fetchone()
    if primeiro is not None:
        conn.execute(
            """
            UPDATE reservas
            SET status = 'pronta', posicao = NULL
            WHERE id = ?
            """,
            (primeiro["id"],),
        )
    _compactar_aguardando(conn, livro_id)


def _compactar_aguardando(conn: sqlite3.Connection, livro_id: int) -> None:
    """RN05/RN06: renumerar aguardando para 1..N."""
    rows = conn.execute(
        """
        SELECT id FROM reservas
        WHERE livro_id = ? AND status = 'aguardando'
        ORDER BY posicao ASC, id ASC
        """,
        (livro_id,),
    ).fetchall()
    for idx, row in enumerate(rows, start=1):
        conn.execute(
            "UPDATE reservas SET posicao = ? WHERE id = ?",
            (idx, row["id"]),
        )


def criar_socio(nome: str, email: str) -> dict[str, Any]:
    """RN01: e-mail único (trim + case-insensitive)."""
    nome = nome.strip()
    email = email.strip()
    conn = _get_conn()
    try:
        existente = conn.execute(
            "SELECT id FROM socios WHERE lower(trim(email)) = lower(?)",
            (email,),
        ).fetchone()
        if existente is not None:
            raise ConflictError("e-mail já cadastrado")
        cur = conn.execute(
            "INSERT INTO socios (nome, email) VALUES (?, ?)",
            (nome, email),
        )
        conn.commit()
        row = conn.execute(
            "SELECT id, nome, email, criado_em FROM socios WHERE id = ?",
            (cur.lastrowid,),
        ).fetchone()
        return _row_to_dict(row)
    except sqlite3.IntegrityError as exc:
        conn.rollback()
        raise ConflictError("e-mail já cadastrado") from exc
    finally:
        conn.close()


def criar_livro(titulo: str, autor: str, exemplares: int) -> dict[str, Any]:
    """RN02: exemplares ∈ [1, 50] (também validado no schema)."""
    if exemplares < 1 or exemplares > 50:
        raise ValueError("exemplares deve estar entre 1 e 50")
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO livros (titulo, autor, exemplares) VALUES (?, ?, ?)",
            (titulo.strip(), autor.strip(), exemplares),
        )
        conn.commit()
        livro_id = int(cur.lastrowid)
        row = conn.execute(
            "SELECT id, titulo, autor, exemplares, criado_em FROM livros WHERE id = ?",
            (livro_id,),
        ).fetchone()
        out = _row_to_dict(row)
        out["exemplares_disponiveis"] = exemplares_disponiveis(conn, livro_id)
        return out
    finally:
        conn.close()


def listar_livros() -> list[dict[str, Any]]:
    conn = _get_conn()
    try:
        rows = conn.execute(
            """
            SELECT
                l.id,
                l.titulo,
                l.autor,
                l.exemplares,
                l.criado_em,
                l.exemplares
                - (
                    SELECT COUNT(*) FROM reservas r
                    WHERE r.livro_id = l.id AND r.status = 'pronta'
                )
                - (
                    SELECT COUNT(*) FROM emprestimos e
                    WHERE e.livro_id = l.id AND e.status = 'aberto'
                ) AS exemplares_disponiveis
            FROM livros l
            ORDER BY l.id ASC
            """
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


def criar_reserva(socio_id: int, livro_id: int) -> dict[str, Any]:
    """RN03/RN04/RN08/RN09."""
    conn = _get_conn()
    try:
        socio = conn.execute("SELECT id FROM socios WHERE id = ?", (socio_id,)).fetchone()
        if socio is None:
            raise NotFoundError("sócio não encontrado")
        livro = conn.execute("SELECT id FROM livros WHERE id = ?", (livro_id,)).fetchone()
        if livro is None:
            raise NotFoundError("livro não encontrado")

        ativa = conn.execute(
            """
            SELECT id FROM reservas
            WHERE socio_id = ? AND livro_id = ?
              AND status IN ('pronta', 'aguardando')
            """,
            (socio_id, livro_id),
        ).fetchone()
        if ativa is not None:
            raise ConflictError("já existe reserva ativa para este sócio e livro")

        disponiveis = exemplares_disponiveis(conn, livro_id)
        if disponiveis > 0:
            status = "pronta"
            posicao = None
        else:
            status = "aguardando"
            row_max = conn.execute(
                """
                SELECT COALESCE(MAX(posicao), 0) AS m
                FROM reservas
                WHERE livro_id = ? AND status = 'aguardando'
                """,
                (livro_id,),
            ).fetchone()
            posicao = int(row_max["m"]) + 1

        cur = conn.execute(
            """
            INSERT INTO reservas (socio_id, livro_id, status, posicao)
            VALUES (?, ?, ?, ?)
            """,
            (socio_id, livro_id, status, posicao),
        )
        conn.commit()
        row = conn.execute(
            """
            SELECT id, socio_id, livro_id, status, posicao, criado_em
            FROM reservas WHERE id = ?
            """,
            (cur.lastrowid,),
        ).fetchone()
        return _row_to_dict(row)
    finally:
        conn.close()


def cancelar_reserva(reserva_id: int) -> None:
    """RN05/RN06/RN07 — cancelar ativa e compactar/promover."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT id, livro_id, status FROM reservas WHERE id = ?",
            (reserva_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError("reserva não encontrada")

        status = row["status"]
        livro_id = int(row["livro_id"])

        if status not in ("pronta", "aguardando"):
            raise ConflictError("reserva não está ativa")

        conn.execute(
            """
            UPDATE reservas
            SET status = 'cancelada', posicao = NULL
            WHERE id = ?
            """,
            (reserva_id,),
        )

        if status == "pronta":
            # RN06: promove posição 1 → pronta e renumerar
            promover_ou_compactar(conn, livro_id)
        else:
            # RN05: compacta posições restantes
            _compactar_aguardando(conn, livro_id)

        conn.commit()
    finally:
        conn.close()
