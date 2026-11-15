from datetime import datetime, timedelta

import pytest

from src.reservas import cancelar_reserva, realizar_reserva
from src.salas import cadastrar_sala, excluir_sala


def test_reserva_futura_no_formato_br_impede_excluir_sala():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    data_futura = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    realizar_reserva(sala["id"], "Djames", data_futura, "19:00-20:00")

    with pytest.raises(ValueError, match="reservas futuras"):
        excluir_sala(sala["id"])


def test_reserva_cancelada_nao_impede_excluir_sala():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    data_futura = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
    reserva = realizar_reserva(sala["id"], "Djames", data_futura, "19:00-20:00")
    cancelar_reserva(reserva["id"])

    assert excluir_sala(sala["id"]) is True
