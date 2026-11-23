"""Golden set do plano 004. Não chama Ollama de verdade."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
GOLDEN = Path(__file__).resolve().parent / "golden_set_recomendacoes.json"
RELATORIO = Path(__file__).resolve().parent / "relatorio_recomendacoes.md"


def _cliente(caso: dict[str, Any], livros_ids: list[int], chamadas: list[int]):
    from app.ollama_client import OllamaIndisponivel

    spec = caso["ollama"]

    def _chamar(payload: dict[str, Any]):
        chamadas.append(1)
        return payload

    modo = spec["modo"]
    if modo == "falha":

        def _falha(_prompt: str) -> dict[str, Any]:
            chamadas.append(1)
            raise OllamaIndisponivel("timeout")

        return _falha
    if modo == "lixo":
        return lambda _prompt: _chamar({"foo": 1})
    if modo == "ok":

        def _ok(_prompt: str) -> dict[str, Any]:
            itens = []
            motivos = spec.get("motivos") or []
            for i, indice in enumerate(spec["livros"]):
                motivo = motivos[i] if i < len(motivos) else "recomendação"
                itens.append({"livro_id": livros_ids[indice], "motivo": motivo})
            return _chamar({"itens": itens})

        return _ok
    if modo == "bruto":

        def _bruto(_prompt: str) -> dict[str, Any]:
            itens = []
            for entrada in spec["ids"]:
                if isinstance(entrada, dict):
                    livro_id = livros_ids[entrada["livro"]]
                else:
                    livro_id = int(entrada)
                itens.append({"livro_id": livro_id, "motivo": "bruto"})
            return _chamar({"itens": itens})

        return _bruto
    raise ValueError(f"modo de ollama desconhecido: {modo}")


def _montar(caso: dict[str, Any]) -> tuple[int, list[int], list[int]]:
    from app import db, service

    db.init_schema()
    socio = service.criar_socio("Ana Silva", "ana.silva@biblioteca.example.com")
    livros_ids: list[int] = []
    for livro in caso["livros"]:
        criado = service.criar_livro(livro["titulo"], livro["autor"], livro["exemplares"])
        livros_ids.append(int(criado["id"]))

    auxiliar = service.criar_socio("Bruno Auxiliar", "bruno.auxiliar@biblioteca.example.com")
    for item in caso.get("historico") or []:
        for _ in range(int(item["n"])):
            emprestimo = service.emprestar(auxiliar["id"], livros_ids[item["livro"]])
            service.devolver(int(emprestimo["id"]))
    for indice in caso.get("lidos") or []:
        emprestimo = service.emprestar(socio["id"], livros_ids[indice])
        service.devolver(int(emprestimo["id"]))
    for indice in caso.get("esgotar") or []:
        livro_id = livros_ids[indice]
        exemplares = int(caso["livros"][indice]["exemplares"])
        for n in range(exemplares):
            outro = service.criar_socio(
                f"Leitor {caso['id']} {n}",
                f"leitor.{caso['id']}.{n}@biblioteca.example.com",
            )
            service.emprestar(outro["id"], livro_id)
    return int(socio["id"]), livros_ids, []


def avaliar_caso(caso: dict[str, Any], pasta: Path) -> dict[str, Any]:
    os.environ["BIBLIO_DB_PATH"] = str(pasta / f"{caso['id']}.db")
    from app import service

    socio_id, livros_ids, chamadas = _montar(caso)
    resultado = service.recomendar(
        socio_id,
        int(caso["limite"]),
        cliente=_cliente(caso, livros_ids, chamadas),
    )
    espera = caso["espera"]
    esperados = [livros_ids[i] for i in espera["livros"]]
    obtidos = [item["livro_id"] for item in resultado["itens"]]
    ok = resultado["origem"] == espera["origem"] and obtidos == esperados
    if ok and "motivo_0" in espera:
        ok = bool(resultado["itens"]) and resultado["itens"][0]["motivo"] == espera["motivo_0"]
    if ok and espera.get("nao_chama_modelo"):
        ok = chamadas == []
    candidatos_ids = set(livros_ids)
    lidos = set(caso.get("lidos") or [])
    sem_alucinacao = all(livro_id in candidatos_ids for livro_id in obtidos)
    sem_lidos = all(livros_ids.index(livro_id) not in lidos for livro_id in obtidos) if livros_ids else True
    ok = ok and sem_alucinacao and sem_lidos
    return {
        "id": caso["id"],
        "descricao": caso["descricao"],
        "ok": ok,
        "origem": resultado["origem"],
        "livros": obtidos,
    }


def avaliar() -> list[dict[str, Any]]:
    casos = json.loads(GOLDEN.read_text(encoding="utf-8"))["casos"]
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp)
        return [avaliar_caso(caso, pasta) for caso in casos]


def render(resultados: list[dict[str, Any]]) -> str:
    linhas = [
        "# Relatório — golden set de recomendações (plano 004 / RM10)",
        "",
        "Runner: `evals/run_llm_eval.py`. Ollama real não é chamado.",
        "",
        f"Casos: {len(resultados)}. Aprovados: {sum(1 for item in resultados if item['ok'])}.",
        "",
        "| Caso | Origem | livros | Gate |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for item in resultados:
        marca = "ok" if item["ok"] else "falhou"
        livros = ", ".join(str(n) for n in item["livros"]) or "—"
        linhas.append(f"| `{item['id']}` | {item['origem']} | {livros} | {marca} |")
    linhas.append("")
    return "\n".join(linhas)


def main() -> None:
    resultados = avaliar()
    texto = render(resultados)
    RELATORIO.write_text(texto, encoding="utf-8")
    if not all(item["ok"] for item in resultados):
        raise SystemExit(texto)
    print(texto)


if __name__ == "__main__":
    main()
