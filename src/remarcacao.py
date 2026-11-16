from src.reservas import _buscar_reserva


def remarcar_reserva(reserva_id, nova_data, novo_horario):
    reserva = _buscar_reserva(reserva_id)
    reserva["data"] = nova_data
    reserva["horario"] = novo_horario
    return reserva
