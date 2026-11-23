"""DTOs Pydantic (contrato HTTP)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class SocioCreate(BaseModel):
    nome: str
    email: str

    @field_validator("nome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        nome = v.strip()
        if not nome:
            raise ValueError("nome não pode ser vazio")
        return nome

    @field_validator("email")
    @classmethod
    def email_trim(cls, v: str) -> str:
        email = v.strip()
        if not email or "@" not in email:
            raise ValueError("e-mail inválido")
        return email


class SocioOut(BaseModel):
    id: int
    nome: str
    email: str
    criado_em: str


class LivroCreate(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    exemplares: int = Field(ge=1, le=50)

    @field_validator("titulo", "autor")
    @classmethod
    def trim_texto(cls, v: str) -> str:
        texto = v.strip()
        if not texto:
            raise ValueError("campo não pode ser vazio")
        return texto


class LivroOut(BaseModel):
    id: int
    titulo: str
    autor: str
    exemplares: int
    exemplares_disponiveis: int
    criado_em: str


class ReservaCreate(BaseModel):
    socio_id: int
    livro_id: int


class ReservaOut(BaseModel):
    id: int
    socio_id: int
    livro_id: int
    status: Literal["pronta", "aguardando", "atendida", "cancelada"]
    posicao: int | None
    criado_em: str


class SaudeOut(BaseModel):
    status: Literal["ok"]


class EmprestimoCreate(BaseModel):
    socio_id: int
    livro_id: int


class EmprestimoOut(BaseModel):
    id: int
    socio_id: int
    livro_id: int
    reserva_id: int | None
    status: Literal["aberto", "devolvido"]
    emprestado_em: str
    devolvido_em: str | None


class RecomendacaoIn(BaseModel):
    socio_id: int
    limite: int = Field(default=3, ge=1, le=10)


class RecomendacaoItem(BaseModel):
    livro_id: int
    titulo: str
    autor: str
    motivo: str


class RecomendacaoOut(BaseModel):
    socio_id: int
    itens: list[RecomendacaoItem]
    origem: Literal["ollama", "fallback_deterministico"]
