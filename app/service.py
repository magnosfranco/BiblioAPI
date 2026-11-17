from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.errors import DomainError
from app.models import Livro, Reserva, Socio
from app.schemas import (
    LivroIn,
    LivroOut,
    ReservaIn,
    ReservaOut,
    ReservaResumo,
    SocioIn,
    SocioOut,
)

STATUS_ATIVOS = ("pronta", "aguardando")


def criar_socio(session: Session, dados: SocioIn) -> SocioOut:
    existente = session.scalar(select(Socio).where(Socio.email == dados.email))
    if existente is not None:
        raise DomainError(409, "Já existe um sócio com esse email")
    socio = Socio(nome=dados.nome, email=dados.email)
    session.add(socio)
    session.flush()
    return SocioOut(id=socio.id, nome=socio.nome, email=socio.email)


def criar_livro(session: Session, dados: LivroIn) -> LivroOut:
    livro = Livro(titulo=dados.titulo, autor=dados.autor, exemplares=dados.exemplares)
    session.add(livro)
    session.flush()
    return montar_livro(session, livro)


def listar_livros(session: Session) -> list[LivroOut]:
    livros = session.scalars(select(Livro).order_by(Livro.id)).all()
    return [montar_livro(session, livro) for livro in livros]


def reservar(session: Session, dados: ReservaIn) -> ReservaOut:
    if session.get(Socio, dados.socio_id) is None:
        raise DomainError(404, "Sócio não encontrado")
    livro = session.get(Livro, dados.livro_id)
    if livro is None:
        raise DomainError(404, "Livro não encontrado")
    ativa = session.scalar(
        select(Reserva).where(
            Reserva.socio_id == dados.socio_id,
            Reserva.livro_id == dados.livro_id,
            Reserva.status.in_(STATUS_ATIVOS),
        )
    )
    if ativa is not None:
        raise DomainError(409, "Já existe uma reserva ativa desse sócio para esse livro")

    if exemplares_disponiveis(session, livro) > 0:
        reserva = Reserva(
            socio_id=dados.socio_id,
            livro_id=dados.livro_id,
            status="pronta",
            posicao=None,
        )
    else:
        ultima = session.scalar(
            select(func.max(Reserva.posicao)).where(
                Reserva.livro_id == dados.livro_id,
                Reserva.status == "aguardando",
            )
        )
        reserva = Reserva(
            socio_id=dados.socio_id,
            livro_id=dados.livro_id,
            status="aguardando",
            posicao=(ultima or 0) + 1,
        )
    session.add(reserva)
    session.flush()
    return para_reserva(reserva)


def cancelar_reserva(session: Session, reserva_id: int) -> ReservaOut:
    reserva = session.get(Reserva, reserva_id)
    if reserva is None:
        raise DomainError(404, "Reserva não encontrada")
    if reserva.status == "cancelada":
        raise DomainError(409, "A reserva já está cancelada")

    era_pronta = reserva.status == "pronta"
    livro_id = reserva.livro_id
    reserva.status = "cancelada"
    reserva.posicao = None
    session.flush()
    if era_pronta:
        promover_proxima(session, livro_id)
    compactar_fila(session, livro_id)
    session.flush()
    return para_reserva(reserva)


def montar_livro(session: Session, livro: Livro) -> LivroOut:
    ativas = session.scalars(
        select(Reserva).where(
            Reserva.livro_id == livro.id,
            Reserva.status.in_(STATUS_ATIVOS),
        )
    ).all()
    prontas = sorted((r for r in ativas if r.status == "pronta"), key=lambda r: r.id)
    fila = sorted(
        (r for r in ativas if r.status == "aguardando"),
        key=lambda r: (r.posicao or 0, r.id),
    )
    return LivroOut(
        id=livro.id,
        titulo=livro.titulo,
        autor=livro.autor,
        exemplares=livro.exemplares,
        exemplares_disponiveis=exemplares_disponiveis(session, livro),
        reservas_ativas=[para_resumo(r) for r in [*prontas, *fila]],
    )


def exemplares_disponiveis(session: Session, livro: Livro) -> int:
    prontas = session.scalar(
        select(func.count())
        .select_from(Reserva)
        .where(Reserva.livro_id == livro.id, Reserva.status == "pronta")
    )
    # Empréstimos abertos entram nesta conta na etapa com plano.
    emprestimos_abertos = 0
    return livro.exemplares - int(prontas or 0) - emprestimos_abertos


def promover_proxima(session: Session, livro_id: int) -> None:
    proxima = session.scalars(
        select(Reserva)
        .where(Reserva.livro_id == livro_id, Reserva.status == "aguardando")
        .order_by(Reserva.posicao.asc(), Reserva.id.asc())
    ).first()
    if proxima is None:
        return
    proxima.status = "pronta"
    proxima.posicao = None
    session.flush()


def compactar_fila(session: Session, livro_id: int) -> None:
    fila = session.scalars(
        select(Reserva)
        .where(Reserva.livro_id == livro_id, Reserva.status == "aguardando")
        .order_by(Reserva.posicao.asc(), Reserva.id.asc())
    ).all()
    for indice, reserva in enumerate(fila, start=1):
        reserva.posicao = indice


def para_reserva(reserva: Reserva) -> ReservaOut:
    return ReservaOut(
        id=reserva.id,
        socio_id=reserva.socio_id,
        livro_id=reserva.livro_id,
        status=reserva.status,
        posicao=reserva.posicao,
    )


def para_resumo(reserva: Reserva) -> ReservaResumo:
    return ReservaResumo(
        id=reserva.id,
        socio_id=reserva.socio_id,
        status=reserva.status,
        posicao=reserva.posicao,
    )
