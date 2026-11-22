"""CI v1 — asserts de artefatos ADLC (RM1) + presença de app/ pós-fatia vibe.

Decisão E1-D1 (Magno da Silva Franco, 2026-11-22): no C1 os .feature são
especificação; a contagem de Cenário: permanece. RM3 cria app/.
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


def test_app_present_pos_c1() -> None:
    """Pós-SPEC na main: fatia vibe/RM3 cria app/ com camada única."""
    app_dir = REPO_ROOT / "app"
    assert app_dir.is_dir(), "app/ deve existir após implementação da fatia vibe"
    for nome in ("main.py", "routes.py", "service.py", "db.py", "schemas.py"):
        assert (app_dir / nome).is_file(), f"faltando app/{nome}"


def test_mcp_server_present_pos_plano_002() -> None:
    """Plano 002: mcp_server/ com tools sobre service."""
    mcp_dir = REPO_ROOT / "mcp_server"
    assert mcp_dir.is_dir()
    assert (mcp_dir / "server.py").is_file()


def test_agents_md_is_v2() -> None:
    text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "v2" in text.lower() or "v2" in text
    assert "SPEC.md" in text
