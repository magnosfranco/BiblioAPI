from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_session
from app.schemas import LivroIn, LivroOut, ReservaIn, ReservaOut, SocioIn, SocioOut
from app.service import cancelar_reserva, criar_livro, criar_socio, listar_livros, reservar

router = APIRouter()


@router.get("/saude", tags=["operacao"])
def saude() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/socios", status_code=201, response_model=SocioOut, tags=["catalogo"])
def post_socio(dados: SocioIn, session: Session = Depends(get_session)) -> SocioOut:
    return criar_socio(session, dados)


@router.post("/livros", status_code=201, response_model=LivroOut, tags=["catalogo"])
def post_livro(dados: LivroIn, session: Session = Depends(get_session)) -> LivroOut:
    return criar_livro(session, dados)


@router.get("/livros", response_model=list[LivroOut], tags=["catalogo"])
def get_livros(session: Session = Depends(get_session)) -> list[LivroOut]:
    return listar_livros(session)


@router.post("/reservas", status_code=201, response_model=ReservaOut, tags=["reservas"])
def post_reserva(dados: ReservaIn, session: Session = Depends(get_session)) -> ReservaOut:
    return reservar(session, dados)


@router.delete(
    "/reservas/{reserva_id}",
    response_model=ReservaOut,
    tags=["reservas"],
)
def delete_reserva(reserva_id: int, session: Session = Depends(get_session)) -> ReservaOut:
    return cancelar_reserva(session, reserva_id)
