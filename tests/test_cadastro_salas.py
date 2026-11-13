"""Testes da funcionalidade 1: cadastrar sala (TDD)."""
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