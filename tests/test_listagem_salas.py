from src.salas import cadastrar_sala, listar_salas


def test_listar_salas_cadastradas():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 30, "Bloco B")

    resultado = listar_salas()

    assert resultado == [sala1, sala2]
    assert resultado[0]["id"] == 1
    assert resultado[1]["nome"] == "Sala 02"


def test_listar_salas_sem_nenhuma_cadastrada():
    assert listar_salas() == []