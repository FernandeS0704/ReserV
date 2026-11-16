from src import armazenamento
from src.reservas import _existe_conflito, _texto_obrigatorio
from src.salas import _calcular_larguras, _montar_linha

SALA_REMOVIDA = {"nome": "Sala removida", "localizacao": "-"}


def consultar_disponibilidade(data, horario):
    _texto_obrigatorio(data, "data")
    _texto_obrigatorio(horario, "horário")

    return [
        sala
        for sala in armazenamento.salas
        if not _existe_conflito(sala["id"], data, horario)
    ]


def _buscar_sala(sala_id):
    return next(
        (sala for sala in armazenamento.salas if sala["id"] == sala_id),
        SALA_REMOVIDA,
    )


def _montar_item_reserva(reserva):
    sala = _buscar_sala(reserva["sala_id"])
    return {
        "id": reserva["id"],
        "sala_id": reserva["sala_id"],
        "sala_nome": sala["nome"],
        "sala_localizacao": sala["localizacao"],
        "responsavel": reserva["responsavel"],
        "data": reserva["data"],
        "horario": reserva["horario"],
        "status": reserva["status"],
    }


def listar_reservas():
    return [_montar_item_reserva(reserva) for reserva in armazenamento.reservas]


TITULOS_RESERVAS = ["ID", "Sala", "Localização", "Responsável", "Data", "Horário", "Status"]


def _linha_reserva(item):
    return [
        str(item["id"]),
        item["sala_nome"],
        item["sala_localizacao"],
        item["responsavel"],
        item["data"],
        item["horario"],
        item["status"],
    ]


def formatar_reservas(lista_reservas):
    if not lista_reservas:
        return "Não há reservas realizadas."

    linhas = [_linha_reserva(item) for item in lista_reservas]
    larguras = _calcular_larguras(TITULOS_RESERVAS, linhas)
    separador = "  ".join("-" * largura for largura in larguras)

    partes = [_montar_linha(TITULOS_RESERVAS, larguras), separador]
    partes += [_montar_linha(linha, larguras) for linha in linhas]
    return "\n".join(partes)
