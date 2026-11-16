from src import armazenamento


def buscar_salas(capacidade_minima=None, localizacao=None):
    resultado = []
    for sala in armazenamento.salas:
        if capacidade_minima is not None and sala["capacidade"] < capacidade_minima:
            continue
        if localizacao is not None and localizacao.lower() not in sala["localizacao"].lower():
            continue
        resultado.append(sala)
    return resultado
