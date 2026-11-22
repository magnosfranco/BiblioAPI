"""Entrypoint FastAPI — lifespan com init_schema."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import db
from app.routes import router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db.init_schema()
    yield


app = FastAPI(title="BiblioAPI", version="0.1.0", lifespan=lifespan)
app.include_router(router)
