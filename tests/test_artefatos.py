"""CI v1 — asserts de artefatos ADLC (RM1) sem exigir app/.

Decisão E1-D1 (Magno da Silva Franco, 2026-11-22): no C1 os .feature são
especificação; estes testes contam/validam artefatos, não executam a API.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_spec_md_exists_and_mentions_rns() -> None:
    spec = REPO_ROOT / "SPEC.md"
    assert spec.is_file(), "SPEC.md é obrigatório (RM1)"
    text = spec.read_text(encoding="utf-8")
    assert "RN01" in text and "RN14" in text
    assert "/socios" in text and "/recomendacoes" in text


def test_prd_exists() -> None:
    assert (REPO_ROOT / "docs" / "PRD.md").is_file()


def test_adrs_minimum() -> None:
    adr_dir = REPO_ROOT / "docs" / "adr"
    assert adr_dir.is_dir()
    adrs = sorted(adr_dir.glob("*.md"))
    assert len(adrs) >= 2, "PDF exige ≥2 ADRs; projeto adota 4"
    names = " ".join(p.name for p in adrs)
    assert "0001" in names and "0002" in names


def test_bdd_features_scenario_count() -> None:
    features = list((REPO_ROOT / "features").glob("*.feature"))
    assert features, "features/*.feature obrigatório (RM1)"
    scenario_re = re.compile(r"^\s*Cenário:", re.MULTILINE)
    total = 0
    for path in features:
        total += len(scenario_re.findall(path.read_text(encoding="utf-8")))
    assert total >= 8, f"PDF exige ≥8 cenários BDD; encontrados {total}"
    assert total >= 16, f"Alvo do projeto ≥16 cenários; encontrados {total}"


def test_app_still_absent_at_c1() -> None:
    """RM1: histórico deve ter SPEC antes de app/; em C1 a pasta ainda não existe."""
    assert not (REPO_ROOT / "app").exists(), (
        "C1 não deve criar app/; implementação vem depois do merge da SPEC na main"
    )


def test_agents_md_is_v2() -> None:
    text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "v2" in text.lower() or "v2" in text
    assert "SPEC.md" in text
