from src.salas import cadastrar_sala, formatar_listagem, listar_salas

def test_listar_salas_cadastradas():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 30, "Bloco B")

    resultado = listar_salas()

    assert resultado == [sala1, sala2]
    assert resultado[0]["id"] == 1
    assert resultado[1]["nome"] == "Sala 02"


def test_listar_salas_sem_nenhuma_cadastrada():
    assert listar_salas() == []

def test_formatar_listagem_sem_salas_informa_que_nao_ha_salas():
    texto = formatar_listagem([])

    assert "não há salas disponíveis" in texto.lower()


def test_formatar_listagem_mostra_todos_os_dados_das_salas():
    cadastrar_sala("Sala 01", 20, "Bloco A")
    cadastrar_sala("Laboratório de Informática", 35, "Bloco B")

    linhas = formatar_listagem(listar_salas()).splitlines()

    for titulo in ["ID", "Nome", "Capacidade", "Localização"]:
        assert titulo in linhas[0]

    assert len(linhas) == 4

    for texto in ["1", "Sala 01", "20", "Bloco A"]:
        assert texto in linhas[2]
    for texto in ["2", "Laboratório de Informática", "35", "Bloco B"]:
        assert texto in linhas[3]


def test_formatar_listagem_alinha_as_colunas():
    cadastrar_sala("Sala 01", 20, "Bloco A")
    cadastrar_sala("Laboratório de Informática", 35, "Bloco B")

    linhas = formatar_listagem(listar_salas()).splitlines()

    posicao = linhas[0].index("Localização")
    assert linhas[2].index("Bloco A") == posicao
    assert linhas[3].index("Bloco B") == posicao