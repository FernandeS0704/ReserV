import pytest

from src import armazenamento
from src.salas import cadastrar_sala, editar_sala


def test_editar_sala_com_sucesso():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    sala_editada = editar_sala(
        sala["id"],
        nome="Sala 01 VIP",
        capacidade=25,
        localizacao="Bloco B",
    )

    assert sala_editada["id"] == sala["id"]
    assert sala_editada["nome"] == "Sala 01 VIP"
    assert sala_editada["capacidade"] == 25
    assert sala_editada["localizacao"] == "Bloco B"

    assert len(armazenamento.salas) == 1
    assert armazenamento.salas[0] == sala_editada


def test_editar_apenas_um_campo_mantem_outros():
    sala = cadastrar_sala("Sala 02", 30, "Bloco C")

    sala_editada = editar_sala(sala["id"], capacidade=35)

    assert sala_editada["id"] == sala["id"]
    assert sala_editada["nome"] == "Sala 02"
    assert sala_editada["capacidade"] == 35
    assert sala_editada["localizacao"] == "Bloco C"


def test_editar_sala_inexistente_lanca_erro():
    with pytest.raises(ValueError, match="Sala não encontrada"):
        editar_sala(999, nome="Nova Sala")


@pytest.mark.parametrize("nome_invalido", ["", "   "])
def test_editar_sala_com_nome_invalido(nome_invalido):
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    with pytest.raises(ValueError, match="nome"):
        editar_sala(sala["id"], nome=nome_invalido)

    assert sala["nome"] == "Sala 01"


@pytest.mark.parametrize("localizacao_invalida", ["", "   "])
def test_editar_sala_com_localizacao_invalida(localizacao_invalida):
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    with pytest.raises(ValueError, match="localização"):
        editar_sala(sala["id"], localizacao=localizacao_invalida)

    assert sala["localizacao"] == "Bloco A"


@pytest.mark.parametrize("capacidade_invalida", [0, -1, "abc", 2.5])
def test_editar_sala_com_capacidade_invalida(capacidade_invalida):
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    with pytest.raises(ValueError, match="capacidade"):
        editar_sala(sala["id"], capacidade=capacidade_invalida)

    assert sala["capacidade"] == 20


def test_editar_sala_com_dados_invalidos_nao_altera_dados_originais():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    with pytest.raises(ValueError):
        editar_sala(sala["id"], nome="Novo Nome", capacidade=-10)

    assert sala["nome"] == "Sala 01"
    assert sala["capacidade"] == 20
