import pytest

from src import armazenamento
from src.reservas import realizar_reserva
from src.salas import cadastrar_sala


def test_realizar_reserva_com_sala_existente():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    reserva = realizar_reserva(
        sala_id=sala["id"],
        responsavel="Djames",
        data="15/11/2026",
        horario="19:00-20:00",
    )

    assert reserva["sala_id"] == sala["id"]
    assert reserva["responsavel"] == "Djames"
    assert reserva["data"] == "15/11/2026"
    assert reserva["horario"] == "19:00-20:00"
    assert reserva["status"] == "ativa"
    assert reserva in armazenamento.reservas


def test_nao_realizar_reserva_para_sala_inexistente():
    with pytest.raises(ValueError, match="Sala"):
        realizar_reserva(99, "Djames", "15/11/2026", "19:00-20:00")


@pytest.mark.parametrize("campo", ["responsavel", "data", "horario"])
def test_nao_realizar_reserva_com_campo_obrigatorio_vazio(campo):
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    dados = {
        "responsavel": "Djames",
        "data": "15/11/2026",
        "horario": "19:00-20:00",
    }
    dados[campo] = "   "

    with pytest.raises(ValueError, match="obrigat"):
        realizar_reserva(sala["id"], **dados)

    assert armazenamento.reservas == []


def test_nao_permitir_reservas_conflitantes():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    realizar_reserva(sala["id"], "Djames", "15/11/2026", "19:00-20:00")

    with pytest.raises(ValueError, match="reservado"):
        realizar_reserva(sala["id"], "Outra pessoa", "15/11/2026", "19:00-20:00")
