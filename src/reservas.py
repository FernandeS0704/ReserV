from src import armazenamento


def _sala_existe(sala_id):
    return any(sala["id"] == sala_id for sala in armazenamento.salas)


def _texto_obrigatorio(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"O campo {campo} é obrigatório.")


def _existe_conflito(sala_id, data, horario):
    return any(
        reserva["status"] == "ativa"
        and reserva["sala_id"] == sala_id
        and reserva["data"] == data
        and reserva["horario"] == horario
        for reserva in armazenamento.reservas
    )


def realizar_reserva(sala_id, responsavel, data, horario):
    if not _sala_existe(sala_id):
        raise ValueError("Sala não encontrada.")

    _texto_obrigatorio(responsavel, "responsável")
    _texto_obrigatorio(data, "data")
    _texto_obrigatorio(horario, "horário")

    if _existe_conflito(sala_id, data, horario):
        raise ValueError("O horário já está reservado para esta sala.")

    reserva = {
        "id": armazenamento.gerar_id_reserva(),
        "sala_id": sala_id,
        "responsavel": responsavel,
        "data": data,
        "horario": horario,
        "status": "ativa",
    }
    armazenamento.reservas.append(reserva)
    return reserva


def _buscar_reserva(reserva_id):
    return next(
        (item for item in armazenamento.reservas if item["id"] == reserva_id),
        None,
    )


def cancelar_reserva(reserva_id):
    reserva = _buscar_reserva(reserva_id)
    if reserva is None:
        raise ValueError("Reserva não encontrada.")
    if reserva["status"] == "cancelada":
        raise ValueError("A reserva já está cancelada.")

    reserva["status"] = "cancelada"
    return reserva
