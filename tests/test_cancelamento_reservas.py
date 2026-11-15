import pytest

from src.reservas import cancelar_reserva, realizar_reserva
from src.salas import cadastrar_sala


def criar_reserva():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    return realizar_reserva(sala["id"], "Djames", "15/11/2026", "19:00-20:00")


def test_cancelar_reserva_existente():
    reserva = criar_reserva()

    cancelada = cancelar_reserva(reserva["id"])

    assert cancelada["status"] == "cancelada"


def test_nao_cancelar_reserva_inexistente():
    with pytest.raises(ValueError, match="Reserva"):
        cancelar_reserva(99)


def test_nao_cancelar_reserva_ja_cancelada():
    reserva = criar_reserva()
    cancelar_reserva(reserva["id"])

    with pytest.raises(ValueError, match="cancelada"):
        cancelar_reserva(reserva["id"])
