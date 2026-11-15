"""
Formato de cada sala:
    {"id": int, "nome": str, "capacidade": int, "localizacao": str}

Formato de cada reserva:
    {"id": int, "sala_id": int, "data_inicio": datetime/str, "data_fim": datetime/str}
"""

salas = []
reservas = []

_proximo_id = 1


def gerar_id():
    global _proximo_id
    novo_id = _proximo_id
    _proximo_id += 1
    return novo_id


def reiniciar():
    global _proximo_id
    salas.clear()
    reservas.clear()
    _proximo_id = 1
