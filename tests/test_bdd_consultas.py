"""Testes BDD das funcionalidades de consulta de disponibilidade e listagem de reservas."""
from pytest_bdd import given, parsers, scenarios, then, when

from src import armazenamento
from src.consultas import consultar_disponibilidade, formatar_reservas, listar_reservas
from src.reservas import cancelar_reserva, realizar_reserva
from src.salas import cadastrar_sala, formatar_listagem

# Transforma cada cenário do arquivo .feature em um teste do pytest.
scenarios("features/consultas.feature")


# ---------------------------------------------------------------------------
# Funções auxiliares (não são passos)
# ---------------------------------------------------------------------------
def _id_da_sala(nome):
    return next(sala["id"] for sala in armazenamento.salas if sala["nome"] == nome)


# ---------------------------------------------------------------------------
# Dado (situação inicial)
# ---------------------------------------------------------------------------
@given(parsers.parse('que existem as salas "{sala1}" e "{sala2}" cadastradas'))
def dado_salas_cadastradas(sala1, sala2):
    cadastrar_sala(sala1, 20, "Bloco A")
    cadastrar_sala(sala2, 30, "Bloco B")


@given(parsers.parse('a sala "{nome}" está reservada na data "{data}" e horário "{horario}"'))
def dado_sala_reservada(nome, data, horario):
    realizar_reserva(_id_da_sala(nome), "Pedro", data, horario)


@given(
    parsers.parse(
        'a sala "{nome}" teve uma reserva cancelada na data "{data}" e horário "{horario}"'
    )
)
def dado_sala_com_reserva_cancelada(nome, data, horario):
    reserva = realizar_reserva(_id_da_sala(nome), "Pedro", data, horario)
    cancelar_reserva(reserva["id"])


@given("que não existem reservas realizadas")
def dado_sem_reservas():
    assert armazenamento.reservas == []


# ---------------------------------------------------------------------------
# Quando (ação)
# ---------------------------------------------------------------------------
@when(
    parsers.re(r'consulto a disponibilidade na data "(?P<data>.*)" e horário "(?P<horario>.*)"'),
    target_fixture="consulta",
)
def quando_consulto_disponibilidade(data, horario):
    try:
        salas = consultar_disponibilidade(data, horario)
    except ValueError as erro:
        return {"salas": None, "texto": None, "erro": str(erro)}
    return {"salas": salas, "texto": formatar_listagem(salas), "erro": None}


@when("solicito a listagem de reservas", target_fixture="consulta")
def quando_solicito_listagem_reservas():
    reservas = listar_reservas()
    return {"reservas": reservas, "texto": formatar_reservas(reservas), "erro": None}


# ---------------------------------------------------------------------------
# Então (resultado esperado)
# ---------------------------------------------------------------------------
@then(parsers.parse('as salas disponíveis devem ser "{sala1}" e "{sala2}"'))
def entao_salas_disponiveis(consulta, sala1, sala2):
    assert consulta["erro"] is None
    assert [sala["nome"] for sala in consulta["salas"]] == [sala1, sala2]


@then(parsers.parse('apenas a sala "{nome}" deve estar disponível'))
def entao_apenas_uma_sala_disponivel(consulta, nome):
    assert consulta["erro"] is None
    assert [sala["nome"] for sala in consulta["salas"]] == [nome]


@then(parsers.parse('o sistema deve informar "{mensagem}"'))
def entao_sistema_informa(consulta, mensagem):
    assert consulta["texto"] == mensagem


@then(parsers.parse('a consulta deve ser recusada com a mensagem "{mensagem}"'))
def entao_consulta_recusada(consulta, mensagem):
    assert consulta["salas"] is None
    assert consulta["erro"] == mensagem


@then(parsers.parse("o sistema deve apresentar {quantidade:d} reservas"))
def entao_quantidade_reservas(consulta, quantidade):
    assert len(consulta["reservas"]) == quantidade


@then("a listagem deve mostrar a sala, a data e o horário de cada reserva")
def entao_listagem_mostra_dados(consulta):
    linhas = consulta["texto"].splitlines()

    for titulo in ["Sala", "Data", "Horário"]:
        assert titulo in linhas[0]

    for reserva, linha in zip(consulta["reservas"], linhas[2:]):
        for valor in (reserva["sala_nome"], reserva["data"], reserva["horario"]):
            assert valor in linha


@then(parsers.parse('a reserva deve aparecer com o status "{status}"'))
def entao_reserva_com_status(consulta, status):
    assert consulta["reservas"][0]["status"] == status
    assert status in consulta["texto"]
