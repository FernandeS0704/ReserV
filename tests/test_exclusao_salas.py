from datetime import datetime, timedelta
import pytest

from src import armazenamento
from src.salas import cadastrar_sala, excluir_sala


def test_excluir_sala_com_sucesso():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    resultado = excluir_sala(sala["id"])

    assert resultado is True
    assert len(armazenamento.salas) == 0
    assert sala not in armazenamento.salas


def test_excluir_sala_com_reservas_passadas():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    armazenamento.reservas.append({
        "id": 1,
        "sala_id": sala["id"],
        "data_fim": datetime.now() - timedelta(days=1),
    })

    resultado = excluir_sala(sala["id"])

    assert resultado is True
    assert sala not in armazenamento.salas


def test_excluir_uma_sala_mantem_as_demais():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 30, "Bloco B")
    sala3 = cadastrar_sala("Sala 03", 15, "Bloco C")

    excluir_sala(sala2["id"])

    assert armazenamento.salas == [sala1, sala3]


def test_excluir_sala_inexistente_lanca_erro():
    with pytest.raises(ValueError, match="Sala não encontrada"):
        excluir_sala(999)


def test_nao_permite_excluir_sala_com_reserva_futura():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    armazenamento.reservas.append({
        "id": 1,
        "sala_id": sala["id"],
        "data_fim": datetime.now() + timedelta(days=2),
    })

    with pytest.raises(ValueError, match="reservas futuras"):
        excluir_sala(sala["id"])

    assert sala in armazenamento.salas


def test_nao_permite_excluir_sala_com_reserva_em_andamento():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    armazenamento.reservas.append({
        "id": 1,
        "sala_id": sala["id"],
        "data_fim": datetime.now() + timedelta(hours=1),
    })

    with pytest.raises(ValueError, match="reservas futuras"):
        excluir_sala(sala["id"])

    assert sala in armazenamento.salas


def test_excluir_sala_ignora_reservas_de_outras_salas():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    sala2 = cadastrar_sala("Sala 02", 30, "Bloco B")

    # Sala 2 tem reserva futura, mas sala 1 não
    armazenamento.reservas.append({
        "id": 1,
        "sala_id": sala2["id"],
        "data_fim": datetime.now() + timedelta(days=1),
    })

    resultado = excluir_sala(sala1["id"])

    assert resultado is True
    assert sala1 not in armazenamento.salas
    assert sala2 in armazenamento.salas
