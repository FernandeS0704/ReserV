import pytest

from src.consultas import consultar_disponibilidade
from src.reservas import cancelar_reserva, realizar_reserva
from src.salas import cadastrar_sala


def test_todas_as_salas_disponiveis_quando_nao_ha_reservas():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 30, "Bloco B")

    disponiveis = consultar_disponibilidade("20/11/2026", "19:00-20:00")

    assert disponiveis == [sala1, sala2]


def test_nenhuma_sala_disponivel_quando_nao_ha_salas_cadastradas():
    assert consultar_disponibilidade("20/11/2026", "19:00-20:00") == []


def test_sala_reservada_no_horario_nao_aparece_como_disponivel():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 30, "Bloco B")
    realizar_reserva(sala1["id"], "Pedro", "20/11/2026", "19:00-20:00")

    disponiveis = consultar_disponibilidade("20/11/2026", "19:00-20:00")

    assert disponiveis == [sala2]


def test_sala_reservada_em_outro_horario_continua_disponivel():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    realizar_reserva(sala["id"], "Pedro", "20/11/2026", "19:00-20:00")

    disponiveis = consultar_disponibilidade("20/11/2026", "20:00-21:00")

    assert disponiveis == [sala]


def test_sala_reservada_em_outra_data_continua_disponivel():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    realizar_reserva(sala["id"], "Pedro", "20/11/2026", "19:00-20:00")

    disponiveis = consultar_disponibilidade("21/11/2026", "19:00-20:00")

    assert disponiveis == [sala]


def test_reserva_cancelada_nao_ocupa_a_sala():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Pedro", "20/11/2026", "19:00-20:00")
    cancelar_reserva(reserva["id"])

    disponiveis = consultar_disponibilidade("20/11/2026", "19:00-20:00")

    assert disponiveis == [sala]


def test_nenhuma_sala_disponivel_quando_todas_estao_reservadas():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 30, "Bloco B")
    realizar_reserva(sala1["id"], "Pedro", "20/11/2026", "19:00-20:00")
    realizar_reserva(sala2["id"], "Djames", "20/11/2026", "19:00-20:00")

    assert consultar_disponibilidade("20/11/2026", "19:00-20:00") == []


@pytest.mark.parametrize("data_invalida", ["", "   "])
def test_nao_consultar_disponibilidade_sem_data(data_invalida):
    cadastrar_sala("Sala 01", 20, "Bloco A")

    with pytest.raises(ValueError, match="data"):
        consultar_disponibilidade(data_invalida, "19:00-20:00")


@pytest.mark.parametrize("horario_invalido", ["", "   "])
def test_nao_consultar_disponibilidade_sem_horario(horario_invalido):
    cadastrar_sala("Sala 01", 20, "Bloco A")

    with pytest.raises(ValueError, match="horário"):
        consultar_disponibilidade("20/11/2026", horario_invalido)
