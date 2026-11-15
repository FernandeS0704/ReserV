from pytest_bdd import given, parsers, scenarios, then, when

from src import armazenamento
from src.reservas import cancelar_reserva, realizar_reserva
from src.salas import cadastrar_sala

scenarios("features/reservas.feature")


@given("que existe uma sala disponível", target_fixture="sala")
def dado_sala_disponivel():
    return cadastrar_sala("Sala 01", 20, "Bloco A")


@given(parsers.parse("que não existe uma sala com id {sala_id:d}"))
def dado_sala_inexistente(sala_id):
    assert all(sala["id"] != sala_id for sala in armazenamento.salas)


@given(
    parsers.parse(
        'que existe uma sala com uma reserva ativa na data "{data}" e horário "{horario}"'
    ),
    target_fixture="reserva",
)
def dado_sala_reservada(data, horario):
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Djames", data, horario)
    return {"sala": sala, "reserva": reserva}


@given("que existe uma reserva ativa", target_fixture="reserva")
def dado_reserva_ativa():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    return realizar_reserva(sala["id"], "Djames", "15/11/2026", "19:00-20:00")


@given("que existe uma reserva já cancelada", target_fixture="reserva")
def dado_reserva_cancelada():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Djames", "15/11/2026", "19:00-20:00")
    return cancelar_reserva(reserva["id"])


@given(parsers.parse("que não existe uma reserva com id {reserva_id:d}"))
def dado_reserva_inexistente(reserva_id):
    assert all(reserva["id"] != reserva_id for reserva in armazenamento.reservas)


@when(
    parsers.parse(
        'realizo uma reserva para "{responsavel}" na data "{data}" e horário "{horario}"'
    ),
    target_fixture="resultado",
)
def quando_realizo_reserva(sala, responsavel, data, horario):
    return realizar_reserva(sala["id"], responsavel, data, horario)


@when(
    parsers.parse(
        'tento reservar a sala {sala_id:d} para "{responsavel}" na data "{data}" e horário "{horario}"'
    ),
    target_fixture="resultado",
)
def quando_tento_reservar(sala_id, responsavel, data, horario):
    try:
        return {
            "reserva": realizar_reserva(sala_id, responsavel, data, horario),
            "erro": None,
        }
    except ValueError as erro:
        return {"reserva": None, "erro": str(erro)}


@when(
    parsers.parse(
        'tento reservar a mesma sala para "{responsavel}" na data "{data}" e horário "{horario}"'
    ),
    target_fixture="resultado",
)
def quando_tento_reservar_mesma_sala(reserva, responsavel, data, horario):
    try:
        return {
            "reserva": realizar_reserva(
                reserva["sala"]["id"], responsavel, data, horario
            ),
            "erro": None,
        }
    except ValueError as erro:
        return {"reserva": None, "erro": str(erro)}


@when("cancelo essa reserva", target_fixture="resultado")
def quando_cancelo_reserva(reserva):
    return cancelar_reserva(reserva["id"])


@when(parsers.parse("tento cancelar a reserva {reserva_id:d}"), target_fixture="resultado")
def quando_tento_cancelar(reserva_id):
    try:
        return {"reserva": cancelar_reserva(reserva_id), "erro": None}
    except ValueError as erro:
        return {"reserva": None, "erro": str(erro)}


@when("tento cancelar essa reserva novamente", target_fixture="resultado")
def quando_tento_cancelar_novamente(reserva):
    try:
        return {"reserva": cancelar_reserva(reserva["id"]), "erro": None}
    except ValueError as erro:
        return {"reserva": None, "erro": str(erro)}


@then(parsers.parse('a reserva deve ser criada com status "{status}"'))
def entao_reserva_criada(resultado, status):
    assert resultado["status"] == status
    assert resultado in armazenamento.reservas


@then(parsers.parse('a reserva deve ser recusada com a mensagem "{mensagem}"'))
def entao_reserva_recusada(resultado, mensagem):
    assert resultado["reserva"] is None
    assert resultado["erro"] == mensagem


@then(parsers.parse('o status da reserva deve ser "{status}"'))
def entao_status_reserva(resultado, status):
    assert resultado["status"] == status


@then(parsers.parse('o cancelamento deve ser recusado com a mensagem "{mensagem}"'))
def entao_cancelamento_recusado(resultado, mensagem):
    assert resultado["reserva"] is None
    assert resultado["erro"] == mensagem
