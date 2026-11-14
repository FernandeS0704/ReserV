import pytest

from src import armazenamento
from src.salas import cadastrar_sala


def test_cadastrar_sala_com_dados_validos():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    assert sala["nome"] == "Sala 01"
    assert sala["capacidade"] == 20
    assert sala["localizacao"] == "Bloco A"
    assert isinstance(sala["id"], int)

    assert len(armazenamento.salas) == 1
    assert sala in armazenamento.salas


@pytest.mark.parametrize("nome_invalido", ["", "   "])
def test_nao_cadastra_sala_com_nome_vazio(nome_invalido):
    with pytest.raises(ValueError, match="nome"):
        cadastrar_sala(nome_invalido, 20, "Bloco A")

    assert armazenamento.salas == []


@pytest.mark.parametrize("localizacao_invalida", ["", "   "])
def test_nao_cadastra_sala_com_localizacao_vazia(localizacao_invalida):
    with pytest.raises(ValueError, match="localização"):
        cadastrar_sala("Sala 01", 20, localizacao_invalida)

    assert armazenamento.salas == []


@pytest.mark.parametrize("capacidade_invalida", [0, -1, "abc", 2.5])
def test_nao_cadastra_sala_com_capacidade_invalida(capacidade_invalida):
    with pytest.raises(ValueError, match="capacidade"):
        cadastrar_sala("Sala 01", capacidade_invalida, "Bloco A")

    assert armazenamento.salas == []

def test_cadastrar_varias_salas():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 30, "Bloco B")
    sala3 = cadastrar_sala("Laboratório", 15, "Bloco C")

    assert armazenamento.salas == [sala1, sala2, sala3]

    ids = [sala["id"] for sala in armazenamento.salas]
    assert ids == [1, 2, 3]


def test_id_nao_e_reaproveitado_apos_remocao():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    cadastrar_sala("Sala 02", 30, "Bloco B")

    armazenamento.salas.remove(sala1)

    sala3 = cadastrar_sala("Sala 03", 10, "Bloco C")

    assert sala3["id"] == 3