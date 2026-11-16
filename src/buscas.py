from src import armazenamento
from src.salas import _texto_preenchido, formatar_listagem

MENSAGEM_SEM_RESULTADO = "Nenhuma sala encontrada para os critérios informados."


def _capacidade_minima_valida(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def _validar_criterios(capacidade_minima, localizacao):
    if capacidade_minima is None and localizacao is None:
        raise ValueError(
            "Informe ao menos um critério de busca: capacidade mínima ou localização."
        )

    if capacidade_minima is not None and not _capacidade_minima_valida(capacidade_minima):
        raise ValueError("A capacidade mínima deve ser um número inteiro maior que zero.")

    if localizacao is not None and not _texto_preenchido(localizacao):
        raise ValueError("A localização da busca não pode ser vazia.")


def _atende_criterios(sala, capacidade_minima, localizacao):
    if capacidade_minima is not None and sala["capacidade"] < capacidade_minima:
        return False
    if localizacao is not None and localizacao.lower() not in sala["localizacao"].lower():
        return False
    return True


def buscar_salas(capacidade_minima=None, localizacao=None):
    _validar_criterios(capacidade_minima, localizacao)

    return [
        sala
        for sala in armazenamento.salas
        if _atende_criterios(sala, capacidade_minima, localizacao)
    ]


def formatar_resultado_busca(lista_salas):
    if not lista_salas:
        return MENSAGEM_SEM_RESULTADO
    return formatar_listagem(lista_salas)
