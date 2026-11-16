"""Testes BDD das funcionalidades de busca de salas e remarcação de reservas."""
from pytest_bdd import given, parsers, scenarios, then, when

from src import armazenamento
from src.buscas import buscar_salas, formatar_resultado_busca
from src.consultas import consultar_disponibilidade
from src.remarcacao import remarcar_reserva
from src.reservas import cancelar_reserva, realizar_reserva
from src.salas import cadastrar_sala

# Transforma cada cenário dos arquivos .feature em um teste do pytest.
scenarios("features/busca_salas.feature")
scenarios("features/remarcacao_reservas.feature")


# ---------------------------------------------------------------------------
# Busca de salas: Dado (situação inicial)
# ---------------------------------------------------------------------------
@given(
    parsers.parse(
        'a sala "{nome}" cadastrada com capacidade {capacidade:d} e localização "{localizacao}"'
    )
)
def dado_sala_cadastrada(nome, capacidade, localizacao):
    cadastrar_sala(nome, capacidade, localizacao)


# ---------------------------------------------------------------------------
# Busca de salas: Quando (ação)
# ---------------------------------------------------------------------------
def _executar_busca(**criterios):
    try:
        salas = buscar_salas(**criterios)
    except ValueError as erro:
        return {"salas": None, "texto": None, "erro": str(erro)}
    return {"salas": salas, "texto": formatar_resultado_busca(salas), "erro": None}


@when(
    parsers.parse("busco salas com capacidade mínima de {capacidade:d}"),
    target_fixture="busca",
)
def quando_busco_por_capacidade(capacidade):
    return _executar_busca(capacidade_minima=capacidade)


@when(
    parsers.parse('busco salas na localização "{localizacao}"'),
    target_fixture="busca",
)
def quando_busco_por_localizacao(localizacao):
    return _executar_busca(localizacao=localizacao)


@when(
    parsers.parse(
        'busco salas com capacidade mínima de {capacidade:d} na localização "{localizacao}"'
    ),
    target_fixture="busca",
)
def quando_busco_por_capacidade_e_localizacao(capacidade, localizacao):
    return _executar_busca(capacidade_minima=capacidade, localizacao=localizacao)


@when("busco salas sem informar critérios", target_fixture="busca")
def quando_busco_sem_criterios():
    return _executar_busca()


# ---------------------------------------------------------------------------
# Busca de salas: Então (resultado esperado)
# ---------------------------------------------------------------------------
@then(parsers.parse('as salas encontradas devem ser "{sala1}" e "{sala2}"'))
def entao_salas_encontradas(busca, sala1, sala2):
    assert busca["erro"] is None
    assert [sala["nome"] for sala in busca["salas"]] == [sala1, sala2]


@then(parsers.parse('apenas a sala "{nome}" deve ser encontrada'))
def entao_apenas_uma_sala(busca, nome):
    assert busca["erro"] is None
    assert [sala["nome"] for sala in busca["salas"]] == [nome]


@then(parsers.parse('o sistema deve informar "{mensagem}"'))
def entao_sistema_informa(busca, mensagem):
    assert busca["texto"] == mensagem


@then(parsers.parse('a busca deve ser recusada com a mensagem "{mensagem}"'))
def entao_busca_recusada(busca, mensagem):
    assert busca["salas"] is None
    assert busca["erro"] == mensagem


# ---------------------------------------------------------------------------
# Remarcação de reservas: Dado (situação inicial)
# ---------------------------------------------------------------------------
@given(
    parsers.parse(
        'que existe uma sala com uma reserva ativa na data "{data}" e horário "{horario}"'
    ),
    target_fixture="reserva",
)
def dado_reserva_ativa(data, horario):
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    return realizar_reserva(sala["id"], "Gustavo", data, horario)


@given(
    parsers.parse(
        'a mesma sala tem outra reserva ativa na data "{data}" e horário "{horario}"'
    )
)
def dado_outra_reserva_na_mesma_sala(reserva, data, horario):
    realizar_reserva(reserva["sala_id"], "Pedro", data, horario)


@given("que existe uma reserva cancelada", target_fixture="reserva")
def dado_reserva_cancelada():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")
    reserva = realizar_reserva(sala["id"], "Gustavo", "20/11/2026", "10:00-11:00")
    cancelar_reserva(reserva["id"])
    return reserva


@given(parsers.parse("que não existe uma reserva com id {reserva_id:d}"))
def dado_reserva_inexistente(reserva_id):
    assert all(r["id"] != reserva_id for r in armazenamento.reservas)


# ---------------------------------------------------------------------------
# Remarcação de reservas: Quando (ação)
# ---------------------------------------------------------------------------
def _executar_remarcacao(reserva_id, data, horario):
    try:
        remarcar_reserva(reserva_id, data, horario)
    except ValueError as erro:
        return {"erro": str(erro)}
    return {"erro": None}


@when(
    parsers.re(
        r'remarco essa reserva para a data "(?P<data>.*)" e horário "(?P<horario>.*)"'
    ),
    target_fixture="remarcacao",
)
def quando_remarco_reserva(reserva, data, horario):
    return _executar_remarcacao(reserva["id"], data, horario)


@when(
    parsers.parse(
        'tento remarcar a reserva {reserva_id:d} para a data "{data}" e horário "{horario}"'
    ),
    target_fixture="remarcacao",
)
def quando_tento_remarcar_reserva_por_id(reserva_id, data, horario):
    return _executar_remarcacao(reserva_id, data, horario)


# ---------------------------------------------------------------------------
# Remarcação de reservas: Então (resultado esperado)
# ---------------------------------------------------------------------------
@then(parsers.parse('a reserva deve estar na data "{data}" e horário "{horario}"'))
def entao_reserva_na_data_e_horario(reserva, data, horario):
    assert (reserva["data"], reserva["horario"]) == (data, horario)


@then(parsers.parse('a sala deve estar disponível na data "{data}" e horário "{horario}"'))
def entao_sala_disponivel(reserva, data, horario):
    salas = consultar_disponibilidade(data, horario)
    assert reserva["sala_id"] in [sala["id"] for sala in salas]


@then(parsers.parse('a remarcação deve ser recusada com a mensagem "{mensagem}"'))
def entao_remarcacao_recusada(remarcacao, mensagem):
    assert remarcacao["erro"] == mensagem
