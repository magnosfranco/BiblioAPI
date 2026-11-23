"""Regras de negócio + SQL (sqlite3 permitido só aqui e em db.py)."""

from __future__ import annotations

import sqlite3
from typing import Any

from app import db
from app.ollama_client import OllamaIndisponivel, completar_json


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
        conn.execute("BEGIN IMMEDIATE")
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
    except ConflictError:
        conn.rollback()
        raise
    finally:
        conn.close()


def obter_socio_por_email(email: str) -> dict[str, Any] | None:
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT id, nome, email, criado_em FROM socios WHERE lower(trim(email)) = lower(?)",
            (email.strip(),),
        ).fetchone()
        return _row_to_dict(row) if row is not None else None
    finally:
        conn.close()


def criar_livro(titulo: str, autor: str, exemplares: int) -> dict[str, Any]:
    """RN02: exemplares ∈ [1, 50] (também validado no schema)."""
    if exemplares < 1 or exemplares > 50:
        raise ValueError("exemplares deve estar entre 1 e 50")
    conn = _get_conn()
    try:
        conn.execute("BEGIN IMMEDIATE")
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
        conn.execute("BEGIN IMMEDIATE")
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

        try:
            cur = conn.execute(
                """
                INSERT INTO reservas (socio_id, livro_id, status, posicao)
                VALUES (?, ?, ?, ?)
                """,
                (socio_id, livro_id, status, posicao),
            )
        except sqlite3.IntegrityError as exc:
            conn.rollback()
            raise ConflictError("já existe reserva ativa para este sócio e livro") from exc
        conn.commit()
        row = conn.execute(
            """
            SELECT id, socio_id, livro_id, status, posicao, criado_em
            FROM reservas WHERE id = ?
            """,
            (cur.lastrowid,),
        ).fetchone()
        return _row_to_dict(row)
    except (NotFoundError, ConflictError):
        conn.rollback()
        raise
    finally:
        conn.close()


def cancelar_reserva(reserva_id: int) -> None:
    """RN05/RN06/RN07 — cancelar ativa e compactar/promover."""
    conn = _get_conn()
    try:
        conn.execute("BEGIN IMMEDIATE")
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
    except (NotFoundError, ConflictError):
        conn.rollback()
        raise
    finally:
        conn.close()


def _fetch_emprestimo(conn: sqlite3.Connection, emprestimo_id: int) -> dict[str, Any]:
    row = conn.execute(
        """
        SELECT id, socio_id, livro_id, reserva_id, status, emprestado_em, devolvido_em
        FROM emprestimos WHERE id = ?
        """,
        (emprestimo_id,),
    ).fetchone()
    if row is None:
        raise NotFoundError("empréstimo não encontrado")
    return _row_to_dict(row)


def emprestar(socio_id: int, livro_id: int) -> dict[str, Any]:
    """RN11 — ordem: 404 → aberto → aguardando → pronta → direto → 409."""
    conn = _get_conn()
    try:
        conn.execute("BEGIN IMMEDIATE")
        socio = conn.execute("SELECT id FROM socios WHERE id = ?", (socio_id,)).fetchone()
        if socio is None:
            raise NotFoundError("sócio não encontrado")
        livro = conn.execute("SELECT id FROM livros WHERE id = ?", (livro_id,)).fetchone()
        if livro is None:
            raise NotFoundError("livro não encontrado")

        aberto = conn.execute(
            """
            SELECT id FROM emprestimos
            WHERE socio_id = ? AND livro_id = ? AND status = 'aberto'
            """,
            (socio_id, livro_id),
        ).fetchone()
        if aberto is not None:
            raise ConflictError("já existe empréstimo aberto para este sócio e livro")

        reserva = conn.execute(
            """
            SELECT id, status FROM reservas
            WHERE socio_id = ? AND livro_id = ?
              AND status IN ('pronta', 'aguardando')
            """,
            (socio_id, livro_id),
        ).fetchone()

        reserva_id: int | None = None
        if reserva is not None:
            if reserva["status"] == "aguardando":
                raise ConflictError("sócio possui reserva aguardando; não fura a fila")
            # RN11-(4): consome pronta mesmo se exemplares_disponiveis == 0
            reserva_id = int(reserva["id"])
            conn.execute(
                "UPDATE reservas SET status = 'atendida', posicao = NULL WHERE id = ?",
                (reserva_id,),
            )
        else:
            disponiveis = exemplares_disponiveis(conn, livro_id)
            if disponiveis <= 0:
                raise ConflictError("sem exemplar disponível e sem reserva pronta")

        try:
            cur = conn.execute(
                """
                INSERT INTO emprestimos (socio_id, livro_id, reserva_id, status)
                VALUES (?, ?, ?, 'aberto')
                """,
                (socio_id, livro_id, reserva_id),
            )
        except sqlite3.IntegrityError as exc:
            conn.rollback()
            raise ConflictError("já existe empréstimo aberto para este sócio e livro") from exc

        conn.commit()
        return _fetch_emprestimo(conn, int(cur.lastrowid))
    except (NotFoundError, ConflictError):
        conn.rollback()
        raise
    finally:
        conn.close()


def consultar_ollama(prompt: str) -> dict[str, Any]:
    """Ponto único de I/O do modelo. Testes substituem esta função."""
    return completar_json(prompt)


def _candidatos(conn: sqlite3.Connection, socio_id: int) -> list[dict[str, Any]]:
    """Livros disponíveis que o sócio ainda não emprestou, por popularidade."""
    lidos = {
        int(row["livro_id"])
        for row in conn.execute(
            "SELECT DISTINCT livro_id FROM emprestimos WHERE socio_id = ?",
            (socio_id,),
        )
    }
    popularidade = {
        int(row["livro_id"]): int(row["n"])
        for row in conn.execute(
            "SELECT livro_id, COUNT(*) AS n FROM emprestimos GROUP BY livro_id"
        )
    }
    candidatos: list[dict[str, Any]] = []
    for livro in conn.execute("SELECT id, titulo, autor FROM livros"):
        livro_id = int(livro["id"])
        if livro_id in lidos or exemplares_disponiveis(conn, livro_id) <= 0:
            continue
        candidatos.append(
            {
                "id": livro_id,
                "titulo": livro["titulo"],
                "autor": livro["autor"],
                "popularidade": popularidade.get(livro_id, 0),
            }
        )
    candidatos.sort(key=lambda item: (-item["popularidade"], item["id"]))
    return candidatos


def _prompt_recomendacao(candidatos: list[dict[str, Any]], limite: int) -> str:
    linhas = "\n".join(
        f"- id={item['id']} | {item['titulo']} | {item['autor']}" for item in candidatos
    )
    return (
        "Recomende livros apenas com ids do catálogo entre as marcas.\n"
        f"No máximo {limite} itens.\n"
        'Responda só JSON: {"itens":[{"livro_id":1,"motivo":"..."}]}.\n'
        "<catalogo>\n"
        f"{linhas}\n"
        "</catalogo>"
    )


def _itens_do_modelo(
    payload: dict[str, Any],
    candidatos: list[dict[str, Any]],
    limite: int,
) -> list[dict[str, Any]]:
    bruto = payload.get("itens")
    if not isinstance(bruto, list):
        raise OllamaIndisponivel("JSON sem lista itens")
    por_id = {item["id"]: item for item in candidatos}
    vistos: set[int] = set()
    itens: list[dict[str, Any]] = []
    for entrada in bruto:
        if not isinstance(entrada, dict) or "livro_id" not in entrada:
            continue
        try:
            livro_id = int(entrada["livro_id"])
        except (TypeError, ValueError):
            continue
        if livro_id not in por_id or livro_id in vistos:
            continue
        vistos.add(livro_id)
        motivo = entrada.get("motivo")
        if not isinstance(motivo, str) or not motivo.strip():
            motivo = "recomendação do modelo"
        livro = por_id[livro_id]
        itens.append(
            {
                "livro_id": livro_id,
                "titulo": livro["titulo"],
                "autor": livro["autor"],
                "motivo": motivo.strip()[:200],
            }
        )
        if len(itens) >= limite:
            break
    if not itens:
        raise OllamaIndisponivel("nenhum livro_id válido")
    return itens


def _itens_fallback(candidatos: list[dict[str, Any]], limite: int) -> list[dict[str, Any]]:
    return [
        {
            "livro_id": item["id"],
            "titulo": item["titulo"],
            "autor": item["autor"],
            "motivo": "popularidade histórica",
        }
        for item in candidatos[:limite]
    ]


def recomendar(
    socio_id: int,
    limite: int = 3,
    *,
    cliente: Any = None,
) -> dict[str, Any]:
    """RN13–RN14. cliente substitui o Ollama (testes e golden set)."""
    if limite < 1:
        raise ConflictError("limite inválido")
    conn = _get_conn()
    try:
        socio = conn.execute("SELECT id FROM socios WHERE id = ?", (socio_id,)).fetchone()
        if socio is None:
            raise NotFoundError("sócio não encontrado")
        candidatos = _candidatos(conn, socio_id)
    finally:
        conn.close()

    if not candidatos:
        return {"socio_id": socio_id, "itens": [], "origem": "fallback_deterministico"}

    consultar = cliente or consultar_ollama
    try:
        payload = consultar(_prompt_recomendacao(candidatos, limite))
        itens = _itens_do_modelo(payload, candidatos, limite)
        origem = "ollama"
    except OllamaIndisponivel:
        itens = _itens_fallback(candidatos, limite)
        origem = "fallback_deterministico"
    return {"socio_id": socio_id, "itens": itens, "origem": origem}


def devolver(emprestimo_id: int) -> dict[str, Any]:
    """RN12 — marca devolvido e aplica a mesma promoção RN07."""
    conn = _get_conn()
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute(
            "SELECT id, livro_id, status FROM emprestimos WHERE id = ?",
            (emprestimo_id,),
        ).fetchone()
        if row is None:
            raise NotFoundError("empréstimo não encontrado")
        if row["status"] == "devolvido":
            raise ConflictError("empréstimo já devolvido")

        conn.execute(
            """
            UPDATE emprestimos
            SET status = 'devolvido',
                devolvido_em = strftime('%Y-%m-%dT%H:%M:%f+00:00', 'now')
            WHERE id = ?
            """,
            (emprestimo_id,),
        )
        promover_ou_compactar(conn, int(row["livro_id"]))
        conn.commit()
        return _fetch_emprestimo(conn, emprestimo_id)
    except (NotFoundError, ConflictError):
        conn.rollback()
        raise
    finally:
        conn.close()
