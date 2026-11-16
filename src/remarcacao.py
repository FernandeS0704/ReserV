from src.reservas import _buscar_reserva, _sala_existe, _texto_obrigatorio


def remarcar_reserva(reserva_id, nova_data, novo_horario):
    reserva = _buscar_reserva(reserva_id)
    if reserva is None:
        raise ValueError("Reserva não encontrada.")
    if reserva["status"] == "cancelada":
        raise ValueError("Não é possível remarcar uma reserva cancelada.")
    if not _sala_existe(reserva["sala_id"]):
        raise ValueError("Sala não encontrada.")

    _texto_obrigatorio(nova_data, "data")
    _texto_obrigatorio(novo_horario, "horário")

    if reserva["data"] == nova_data and reserva["horario"] == novo_horario:
        raise ValueError("A reserva já está nesta data e horário.")

    reserva["data"] = nova_data
    reserva["horario"] = novo_horario
    return reserva
