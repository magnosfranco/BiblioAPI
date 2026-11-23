"""RM5 — o eval de disparo melhora da v1 para a v2 e bate com o SKILL.md."""

from __future__ import annotations

from evals.run_skill_eval import RELATORIO, avaliar, render


def test_f1_sobe_e_relatorio_bate() -> None:
    resultado = avaliar()
    assert resultado["n"] >= 10
    assert resultado["v1"]["fp"] > 0
    assert resultado["v2"]["fp"] == 0
    assert resultado["v2"]["fn"] == 0
    assert resultado["v2"]["f1"] > resultado["v1"]["f1"]
    assert RELATORIO.read_text(encoding="utf-8") == render(resultado)
