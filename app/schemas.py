from pydantic import BaseModel, EmailStr, Field, field_validator


def _texto_obrigatorio(valor: str) -> str:
    limpo = valor.strip()
    if not limpo:
        raise ValueError("informe um texto")
    return limpo


class SocioIn(BaseModel):
    nome: str = Field(min_length=1, max_length=120)
    email: EmailStr

    @field_validator("nome")
    @classmethod
    def limpa_nome(cls, valor: str) -> str:
        return _texto_obrigatorio(valor)

    @field_validator("email")
    @classmethod
    def normaliza_email(cls, valor: str) -> str:
        return valor.strip().lower()


class SocioOut(BaseModel):
    id: int
    nome: str
    email: str


class LivroIn(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    autor: str = Field(min_length=1, max_length=200)
    exemplares: int = Field(ge=1, le=50)

    @field_validator("titulo", "autor")
    @classmethod
    def limpa_texto(cls, valor: str) -> str:
        return _texto_obrigatorio(valor)


class ReservaResumo(BaseModel):
    id: int
    socio_id: int
    status: str
    posicao: int | None


class LivroOut(BaseModel):
    id: int
    titulo: str
    autor: str
    exemplares: int
    exemplares_disponiveis: int
    reservas_ativas: list[ReservaResumo]


class ReservaIn(BaseModel):
    socio_id: int = Field(gt=0)
    livro_id: int = Field(gt=0)


class ReservaOut(BaseModel):
    id: int
    socio_id: int
    livro_id: int
    status: str
    posicao: int | None
