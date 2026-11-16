import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_spec_lista_os_oito_endpoints_e_a_saude():
    texto = (ROOT / "SPEC.md").read_text(encoding="utf-8")
    for caminho in (
        "/socios",
        "/livros",
        "/reservas",
        "/emprestimos",
        "/recomendacoes",
        "/saude",
    ):
        assert caminho in texto


def test_pelo_menos_8_cenarios_bdd():
    arquivos = sorted((ROOT / "features").glob("*.feature"))
    assert len(arquivos) >= 3
    texto = "\n".join(arquivo.read_text(encoding="utf-8") for arquivo in arquivos)
    assert texto.count("# language: pt") == len(arquivos)
    assert len(re.findall(r"(?m)^\s*Cenário:", texto)) >= 8


def test_pelo_menos_2_adrs():
    adrs = sorted((ROOT / "docs" / "adr").glob("*.md"))
    assert len(adrs) >= 2


def test_agents_declara_as_oito_regras():
    texto = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for regra in ("R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08"):
        assert regra in texto


def test_r01_codigo_de_producao_fica_em_app():
    assert list(ROOT.glob("*.py")) == []


def test_r02_gitignore_cobre_segredo_e_banco():
    texto = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in texto
    assert "data/" in texto


def test_r07_pytest_aponta_para_tests():
    texto = (ROOT / "pytest.ini").read_text(encoding="utf-8")
    assert "testpaths = tests" in texto


def test_r08_emails_de_exemplo_sao_sinteticos():
    textos = []
    for pasta in (ROOT / "features", ROOT / "tests"):
        for arquivo in pasta.rglob("*"):
            if arquivo.suffix in {".feature", ".py"}:
                textos.append(arquivo.read_text(encoding="utf-8"))
    emails = re.findall(r"[\w.+-]+@[\w.-]+", "\n".join(textos))
    assert emails
    assert all(email.endswith("@biblioteca.example.com") for email in emails)
