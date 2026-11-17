import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse

import app.models  # noqa: F401  (registra as tabelas no metadata)
from app.db import Base, make_engine, make_session_factory
from app.errors import DomainError
from app.routes import router


def create_app(database_url: str | None = None) -> FastAPI:
    url = database_url or os.getenv("BIBLIO_DATABASE_URL", "sqlite:///./data/biblio.db")
    engine = make_engine(url)
    Base.metadata.create_all(engine)
    app = FastAPI(
        title="BiblioAPI",
        version="0.1.0",
        description=(
            "Catálogo, reservas e fila de espera. "
            "Empréstimos e recomendações entram nas próximas etapas."
        ),
    )
    app.state.engine = engine
    app.state.session_factory = make_session_factory(engine)

    @app.exception_handler(DomainError)
    def responder_erro_de_dominio(_request, exc: DomainError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    app.include_router(router)
    return app


app = create_app()
