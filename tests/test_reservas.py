def cadastrar_socio(client, nome, email):
    resposta = client.post("/socios", json={"nome": nome, "email": email})
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


def cadastrar_livro(client, titulo, autor, exemplares):
    resposta = client.post(
        "/livros",
        json={"titulo": titulo, "autor": autor, "exemplares": exemplares},
    )
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


def reservar(client, socio_id, livro_id):
    return client.post("/reservas", json={"socio_id": socio_id, "livro_id": livro_id})


def catalogo(client, livro_id):
    resposta = client.get("/livros")
    assert resposta.status_code == 200
    return next(item for item in resposta.json() if item["id"] == livro_id)


def da_pessoa(livro, socio_id):
    return next(item for item in livro["reservas_ativas"] if item["socio_id"] == socio_id)


def test_cadastrar_socio(client):
    socio = cadastrar_socio(client, "Ana", "ana@biblioteca.example.com")
    assert socio["nome"] == "Ana"
    assert socio["email"] == "ana@biblioteca.example.com"
    assert socio["id"] >= 1


def test_recusar_email_duplicado(client):
    cadastrar_socio(client, "Ana", "ana@biblioteca.example.com")
    resposta = client.post(
        "/socios",
        json={"nome": "Ana Costa", "email": "Ana@biblioteca.example.com"},
    )
    assert resposta.status_code == 409
    assert resposta.json()["detail"] == "Já existe um sócio com esse email"


def test_cadastrar_livro_com_exemplares(client):
    livro = cadastrar_livro(client, "Dom Casmurro", "Machado de Assis", 2)
    assert livro["titulo"] == "Dom Casmurro"
    assert livro["exemplares"] == 2
    assert livro["exemplares_disponiveis"] == 2
    assert livro["reservas_ativas"] == []


def test_recusar_livro_sem_exemplar(client):
    resposta = client.post(
        "/livros",
        json={"titulo": "Sem exemplar", "autor": "Autora", "exemplares": 0},
    )
    assert resposta.status_code == 422


def test_listar_catalogo_com_exemplares_disponiveis(client):
    socio = cadastrar_socio(client, "Ana", "ana@biblioteca.example.com")
    livro = cadastrar_livro(client, "Dom Casmurro", "Machado de Assis", 2)
    criado = reservar(client, socio["id"], livro["id"])
    assert criado.status_code == 201

    visto = catalogo(client, livro["id"])
    assert visto["exemplares_disponiveis"] == 1
    assert da_pessoa(visto, socio["id"])["status"] == "pronta"


def test_reserva_fica_pronta_quando_ha_exemplar(client):
    socio = cadastrar_socio(client, "Ana", "ana@biblioteca.example.com")
    livro = cadastrar_livro(client, "Dom Casmurro", "Machado de Assis", 1)
    resposta = reservar(client, socio["id"], livro["id"])
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["status"] == "pronta"
    assert corpo["posicao"] is None
    assert catalogo(client, livro["id"])["exemplares_disponiveis"] == 0


def test_reserva_entra_na_fila_quando_nao_ha_exemplar(client):
    ana = cadastrar_socio(client, "Ana", "ana@biblioteca.example.com")
    bruno = cadastrar_socio(client, "Bruno", "bruno@biblioteca.example.com")
    livro = cadastrar_livro(client, "Dom Casmurro", "Machado de Assis", 1)
    assert reservar(client, ana["id"], livro["id"]).status_code == 201

    resposta = reservar(client, bruno["id"], livro["id"])
    assert resposta.status_code == 201
    assert resposta.json()["status"] == "aguardando"
    assert resposta.json()["posicao"] == 1


def test_fila_conserva_a_ordem_de_chegada(client):
    ana = cadastrar_socio(client, "Ana", "ana@biblioteca.example.com")
    bruno = cadastrar_socio(client, "Bruno", "bruno@biblioteca.example.com")
    carla = cadastrar_socio(client, "Carla", "carla@biblioteca.example.com")
    livro = cadastrar_livro(client, "Dom Casmurro", "Machado de Assis", 1)
    assert reservar(client, ana["id"], livro["id"]).status_code == 201

    primeiro = reservar(client, bruno["id"], livro["id"])
    segundo = reservar(client, carla["id"], livro["id"])
    assert primeiro.json()["posicao"] == 1
    assert segundo.json()["posicao"] == 2

    visto = catalogo(client, livro["id"])
    assert da_pessoa(visto, bruno["id"])["posicao"] == 1
    assert da_pessoa(visto, carla["id"])["posicao"] == 2


def _fila_de_tres(client):
    pessoas = [
        cadastrar_socio(client, nome, email)
        for nome, email in (
            ("Ana", "ana@biblioteca.example.com"),
            ("Bruno", "bruno@biblioteca.example.com"),
            ("Carla", "carla@biblioteca.example.com"),
            ("Davi", "davi@biblioteca.example.com"),
        )
    ]
    livro = cadastrar_livro(client, "Dom Casmurro", "Machado de Assis", 1)
    reservas = [reservar(client, pessoa["id"], livro["id"]) for pessoa in pessoas]
    assert all(resposta.status_code == 201 for resposta in reservas)
    return pessoas, livro, [resposta.json() for resposta in reservas]


def test_cancelar_quem_esta_no_meio_reordena_as_posicoes(client):
    pessoas, livro, reservas = _fila_de_tres(client)
    ana, bruno, carla, davi = pessoas
    cancelamento = client.delete(f"/reservas/{reservas[2]['id']}")
    assert cancelamento.status_code == 200
    assert cancelamento.json()["status"] == "cancelada"

    visto = catalogo(client, livro["id"])
    assert visto["exemplares_disponiveis"] == 0
    assert da_pessoa(visto, ana["id"])["status"] == "pronta"
    assert da_pessoa(visto, bruno["id"])["posicao"] == 1
    assert da_pessoa(visto, davi["id"])["posicao"] == 2
    assert all(item["socio_id"] != carla["id"] for item in visto["reservas_ativas"])


def test_cancelar_a_reserva_pronta_promove_o_primeiro(client):
    pessoas, livro, reservas = _fila_de_tres(client)
    ana, bruno, carla, davi = pessoas
    cancelamento = client.delete(f"/reservas/{reservas[0]['id']}")
    assert cancelamento.status_code == 200
    assert cancelamento.json()["socio_id"] == ana["id"]
    assert cancelamento.json()["status"] == "cancelada"

    visto = catalogo(client, livro["id"])
    assert visto["exemplares_disponiveis"] == 0
    promovido = da_pessoa(visto, bruno["id"])
    assert promovido["status"] == "pronta"
    assert promovido["posicao"] is None
    assert da_pessoa(visto, carla["id"])["posicao"] == 1
    assert da_pessoa(visto, davi["id"])["posicao"] == 2


def test_socio_nao_mantem_duas_reservas_ativas_do_mesmo_livro(client):
    ana = cadastrar_socio(client, "Ana", "ana@biblioteca.example.com")
    livro = cadastrar_livro(client, "Dom Casmurro", "Machado de Assis", 1)
    primeira = reservar(client, ana["id"], livro["id"])
    assert primeira.status_code == 201

    conflito = reservar(client, ana["id"], livro["id"])
    assert conflito.status_code == 409

    cancelamento = client.delete(f"/reservas/{primeira.json()['id']}")
    assert cancelamento.status_code == 200
    nova = reservar(client, ana["id"], livro["id"])
    assert nova.status_code == 201
    assert nova.json()["status"] == "pronta"


def test_reserva_de_livro_inexistente_retorna_nao_encontrado(client):
    ana = cadastrar_socio(client, "Ana", "ana@biblioteca.example.com")
    resposta = reservar(client, ana["id"], 9999)
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Livro não encontrado"


def test_reserva_de_socio_inexistente_retorna_nao_encontrado(client):
    livro = cadastrar_livro(client, "Dom Casmurro", "Machado de Assis", 1)
    resposta = reservar(client, 9999, livro["id"])
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Sócio não encontrado"


def test_cancelar_reserva_inexistente_retorna_nao_encontrado(client):
    resposta = client.delete("/reservas/9999")
    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Reserva não encontrada"
