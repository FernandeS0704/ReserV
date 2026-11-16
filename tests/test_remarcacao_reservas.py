import pytest

from src import armazenamento
from src.consultas import consultar_disponibilidade
from src.remarcacao import remarcar_reserva
from src.reservas import cancelar_reserva, realizar_reserva
from src.salas import cadastrar_sala, excluir_sala


def test_remarcar_reserva_para_horario_livre():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")

    resultado = remarcar_reserva(reserva["id"], "21/11/2026", "14:00-15:00")

    assert resultado["data"] == "21/11/2026"
    assert resultado["horario"] == "14:00-15:00"


def test_remarcar_reserva_mantem_id_sala_responsavel_e_status():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")
    id_original = reserva["id"]

    resultado = remarcar_reserva(id_original, "21/11/2026", "14:00-15:00")

    assert resultado["id"] == id_original
    assert resultado["sala_id"] == sala["id"]
    assert resultado["responsavel"] == "Gustavo"
    assert resultado["status"] == "ativa"
    assert len(armazenamento.reservas) == 1


def test_remarcar_reserva_libera_o_horario_antigo_e_ocupa_o_novo():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")

    remarcar_reserva(reserva["id"], "21/11/2026", "14:00-15:00")

    assert consultar_disponibilidade("20/11/2026", "10:00-11:00") == [sala]
    assert consultar_disponibilidade("21/11/2026", "14:00-15:00") == []


def test_nao_remarcar_reserva_inexistente():
    with pytest.raises(ValueError, match="Reserva não encontrada"):
        remarcar_reserva(99, "21/11/2026", "14:00-15:00")


def test_nao_remarcar_reserva_cancelada():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")
    cancelar_reserva(reserva["id"])

    with pytest.raises(ValueError, match="cancelada"):
        remarcar_reserva(reserva["id"], "21/11/2026", "14:00-15:00")

    assert (reserva["data"], reserva["horario"]) == ("20/11/2026", "10:00-11:00")


@pytest.mark.parametrize(
    ("nova_data", "novo_horario"),
    [
        ("", "14:00-15:00"),
        ("   ", "14:00-15:00"),
        ("21/11/2026", ""),
        ("21/11/2026", "   "),
    ],
)
def test_nao_remarcar_com_campo_obrigatorio_vazio(nova_data, novo_horario):
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")

    with pytest.raises(ValueError, match="obrigat"):
        remarcar_reserva(reserva["id"], nova_data, novo_horario)

    assert (reserva["data"], reserva["horario"]) == ("20/11/2026", "10:00-11:00")


def test_nao_remarcar_para_a_mesma_data_e_horario():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")

    with pytest.raises(ValueError, match="já está"):
        remarcar_reserva(reserva["id"], "20/11/2026", "10:00-11:00")


def test_nao_remarcar_reserva_de_sala_que_foi_excluida():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "10/01/2025", "10:00-11:00")
    excluir_sala(sala["id"])

    with pytest.raises(ValueError, match="Sala não encontrada"):
        remarcar_reserva(reserva["id"], "21/11/2026", "14:00-15:00")


def test_nao_remarcar_para_horario_ocupado_por_outra_reserva():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")
    realizar_reserva(sala["id"], "Pedro", "20/11/2026", "14:00-15:00")

    with pytest.raises(ValueError, match="reservado"):
        remarcar_reserva(reserva["id"], "20/11/2026", "14:00-15:00")

    assert (reserva["data"], reserva["horario"]) == ("20/11/2026", "10:00-11:00")


def test_remarcar_para_horario_ocupado_em_outra_sala_e_permitido():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 20, "Bloco A")
    reserva = realizar_reserva(sala1["id"], "Gustavo", "20/11/2026", "10:00-11:00")
    realizar_reserva(sala2["id"], "Pedro", "20/11/2026", "14:00-15:00")

    resultado = remarcar_reserva(reserva["id"], "20/11/2026", "14:00-15:00")

    assert resultado["horario"] == "14:00-15:00"


def test_remarcar_para_horario_de_reserva_cancelada_e_permitido():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")
    outra = realizar_reserva(sala["id"], "Pedro", "20/11/2026", "14:00-15:00")
    cancelar_reserva(outra["id"])

    resultado = remarcar_reserva(reserva["id"], "20/11/2026", "14:00-15:00")

    assert resultado["horario"] == "14:00-15:00"
