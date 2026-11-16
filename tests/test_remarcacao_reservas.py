from src import armazenamento
from src.consultas import consultar_disponibilidade
from src.remarcacao import remarcar_reserva
from src.reservas import realizar_reserva
from src.salas import cadastrar_sala


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
