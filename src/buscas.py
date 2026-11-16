from src import armazenamento


def buscar_salas(capacidade_minima):
    return [
        sala
        for sala in armazenamento.salas
        if sala["capacidade"] >= capacidade_minima
    ]
