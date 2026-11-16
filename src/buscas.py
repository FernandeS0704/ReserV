from src import armazenamento


def buscar_salas(capacidade_minima=None, localizacao=None):
    if capacidade_minima is None and localizacao is None:
        raise ValueError(
            "Informe ao menos um critério de busca: capacidade mínima ou localização."
        )

    if capacidade_minima is not None and not (
        isinstance(capacidade_minima, int)
        and not isinstance(capacidade_minima, bool)
        and capacidade_minima > 0
    ):
        raise ValueError("A capacidade mínima deve ser um número inteiro maior que zero.")

    if localizacao is not None and not (
        isinstance(localizacao, str) and localizacao.strip()
    ):
        raise ValueError("A localização da busca não pode ser vazia.")

    resultado = []
    for sala in armazenamento.salas:
        if capacidade_minima is not None and sala["capacidade"] < capacidade_minima:
            continue
        if localizacao is not None and localizacao.lower() not in sala["localizacao"].lower():
            continue
        resultado.append(sala)
    return resultado
