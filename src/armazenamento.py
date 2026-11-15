"""
Formato de cada sala:
    {"id": int, "nome": str, "capacidade": int, "localizacao": str}

Formato de cada reserva:
    {"id": int, "sala_id": int, "responsavel": str, "data": str,
     "horario": str, "status": str}
"""

salas = []
reservas = []

_proximo_id = 1
_proximo_id_reserva = 1


def gerar_id():
    global _proximo_id
    novo_id = _proximo_id
    _proximo_id += 1
    return novo_id


def gerar_id_reserva():
    global _proximo_id_reserva
    novo_id = _proximo_id_reserva
    _proximo_id_reserva += 1
    return novo_id


def reiniciar():
    global _proximo_id, _proximo_id_reserva
    salas.clear()
    reservas.clear()
    _proximo_id = 1
    _proximo_id_reserva = 1
