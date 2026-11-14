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