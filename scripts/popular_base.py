"""Catálogo e sócios sintéticos para o Ollama local. Idempotente.

Uso, na pasta repo/:
    python scripts/popular_base.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _service():
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    from app import service

    return service

SOCIOS = (
    ("Ana Silva", "ana.silva@biblioteca.example.com"),
    ("Bruno Lima", "bruno.lima@biblioteca.example.com"),
    ("Clara Nunes", "clara.nunes@biblioteca.example.com"),
    ("Diego Alves", "diego.alves@biblioteca.example.com"),
)

# exemplares, vezes emprestado e devolvido (popularidade), se fica um aberto.
CATALOGO = (
    {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "exemplares": 3, "devolvidos": 4, "aberto": False, "lido_por": "ana.silva@biblioteca.example.com"},
    {"titulo": "Memórias Póstumas de Brás Cubas", "autor": "Machado de Assis", "exemplares": 2, "devolvidos": 1, "aberto": False, "lido_por": None},
    {"titulo": "A Hora da Estrela", "autor": "Clarice Lispector", "exemplares": 2, "devolvidos": 3, "aberto": False, "lido_por": None},
    {"titulo": "Grande Sertão: Veredas", "autor": "Guimarães Rosa", "exemplares": 2, "devolvidos": 5, "aberto": False, "lido_por": None},
    {"titulo": "Vidas Secas", "autor": "Graciliano Ramos", "exemplares": 2, "devolvidos": 2, "aberto": False, "lido_por": None},
    {"titulo": "Capitães da Areia", "autor": "Jorge Amado", "exemplares": 3, "devolvidos": 2, "aberto": False, "lido_por": "bruno.lima@biblioteca.example.com"},
    {"titulo": "O Cortiço", "autor": "Aluísio Azevedo", "exemplares": 1, "devolvidos": 0, "aberto": True, "lido_por": None},
    {"titulo": "Macunaíma", "autor": "Mário de Andrade", "exemplares": 2, "devolvidos": 1, "aberto": False, "lido_por": None},
)


def _socio(nome: str, email: str) -> dict:
    service = _service()
    try:
        return service.criar_socio(nome, email)
    except service.ConflictError:
        encontrado = service.obter_socio_por_email(email)
        if encontrado is None:
            raise
        return encontrado


def popular() -> dict[str, int | bool]:
    service = _service()
    from app import db

    db.init_schema()
    socios = {email: _socio(nome, email) for nome, email in SOCIOS}
    existentes = {livro["titulo"]: livro for livro in service.listar_livros()}
    novos = 0
    emprestimos = 0
    leitores = [socio for email, socio in socios.items()]
    for item in CATALOGO:
        livro = existentes.get(item["titulo"])
        if livro is None:
            livro = service.criar_livro(item["titulo"], item["autor"], item["exemplares"])
            novos += 1
        else:
            continue
        livro_id = int(livro["id"])
        for n in range(item["devolvidos"]):
            socio = leitores[n % len(leitores)]
            if item["lido_por"] and n == 0:
                socio = socios[item["lido_por"]]
            feito = service.emprestar(int(socio["id"]), livro_id)
            service.devolver(int(feito["id"]))
            emprestimos += 1
        if item["aberto"]:
            service.emprestar(int(socios["diego.alves@biblioteca.example.com"]["id"]), livro_id)
            emprestimos += 1
        elif item["lido_por"] and item["devolvidos"] == 0:
            feito = service.emprestar(int(socios[item["lido_por"]]["id"]), livro_id)
            service.devolver(int(feito["id"]))
            emprestimos += 1
    return {
        "ja_existia": novos == 0,
        "socios": len(socios),
        "livros_novos": novos,
        "emprestimos": emprestimos,
    }


def main() -> None:
    resumo = popular()
    if resumo["ja_existia"]:
        print("Base já tinha o catálogo de exemplo. Nada novo foi gravado.")
        return
    print(
        f"Base populada: {resumo['socios']} sócios, "
        f"{resumo['livros_novos']} livros, {resumo['emprestimos']} empréstimos."
    )


if __name__ == "__main__":
    main()
