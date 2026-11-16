from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_saude(client):
    resposta = client.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_r03_todo_caminho_de_negocio_esta_na_spec(client):
    spec = (ROOT / "SPEC.md").read_text(encoding="utf-8")
    caminhos = client.get("/openapi.json").json()["paths"]
    for caminho in caminhos:
        if caminho == "/saude":
            continue
        base = caminho.split("{", 1)[0].rstrip("/")
        assert base in spec


def test_r06_openapi_nao_expoe_emprestimos_nem_recomendacoes(client):
    caminhos = set(client.get("/openapi.json").json()["paths"])
    assert "/socios" in caminhos
    assert "/livros" in caminhos
    assert "/reservas" in caminhos
    assert "/reservas/{reserva_id}" in caminhos
    assert "/emprestimos" not in caminhos
    assert not any(caminho.startswith("/emprestimos") for caminho in caminhos)
    assert "/recomendacoes" not in caminhos
