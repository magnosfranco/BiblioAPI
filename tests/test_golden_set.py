"""O CI executa o golden set sem Ollama no runner."""

from __future__ import annotations

from pathlib import Path

from evals.run_llm_eval import RELATORIO, avaliar, render

REPO = Path(__file__).resolve().parents[1]


def test_golden_set_doze_casos_e_relatorio() -> None:
    resultados = avaliar()
    assert len(resultados) >= 10
    assert all(item["ok"] for item in resultados), resultados
    texto = render(resultados)
    assert RELATORIO.is_file()
    assert RELATORIO.read_text(encoding="utf-8") == texto
    assert "falhou" not in texto
