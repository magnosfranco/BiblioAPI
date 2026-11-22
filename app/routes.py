"""Rotas HTTP — só adaptam DTO ↔ service (sem SQL)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app import service
from app.schemas import (
    EmprestimoCreate,
    EmprestimoOut,
    LivroCreate,
    LivroOut,
    ReservaCreate,
    ReservaOut,
    SaudeOut,
    SocioCreate,
    SocioOut,
)

router = APIRouter()


@router.get("/saude", response_model=SaudeOut)
def saude() -> SaudeOut:
    return SaudeOut(status="ok")


@router.post("/socios", response_model=SocioOut, status_code=201)
def post_socio(body: SocioCreate) -> SocioOut:
    try:
        data = service.criar_socio(body.nome, body.email)
    except service.ConflictError as exc:
        raise HTTPException(status_code=409, detail=exc.message) from exc
    return SocioOut(**data)


@router.post("/livros", response_model=LivroOut, status_code=201)
def post_livro(body: LivroCreate) -> LivroOut:
    data = service.criar_livro(body.titulo, body.autor, body.exemplares)
    return LivroOut(**data)


@router.get("/livros", response_model=list[LivroOut])
def get_livros() -> list[LivroOut]:
    return [LivroOut(**item) for item in service.listar_livros()]


@router.post("/reservas", response_model=ReservaOut, status_code=201)
def post_reserva(body: ReservaCreate) -> ReservaOut:
    try:
        data = service.criar_reserva(body.socio_id, body.livro_id)
    except service.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.message) from exc
    except service.ConflictError as exc:
        raise HTTPException(status_code=409, detail=exc.message) from exc
    return ReservaOut(**data)


@router.delete("/reservas/{reserva_id}", status_code=204)
def delete_reserva(reserva_id: int) -> None:
    try:
        service.cancelar_reserva(reserva_id)
    except service.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.message) from exc
    except service.ConflictError as exc:
        raise HTTPException(status_code=409, detail=exc.message) from exc


@router.post("/emprestimos", response_model=EmprestimoOut, status_code=201)
def post_emprestimo(body: EmprestimoCreate) -> EmprestimoOut:
    try:
        data = service.emprestar(body.socio_id, body.livro_id)
    except service.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.message) from exc
    except service.ConflictError as exc:
        raise HTTPException(status_code=409, detail=exc.message) from exc
    return EmprestimoOut(**data)


@router.post("/emprestimos/{emprestimo_id}/devolucao", response_model=EmprestimoOut)
def post_devolucao(emprestimo_id: int) -> EmprestimoOut:
    try:
        data = service.devolver(emprestimo_id)
    except service.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.message) from exc
    except service.ConflictError as exc:
        raise HTTPException(status_code=409, detail=exc.message) from exc
    return EmprestimoOut(**data)
