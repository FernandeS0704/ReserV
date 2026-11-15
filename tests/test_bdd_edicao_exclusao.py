"""Testes BDD das funcionalidades de edição e exclusão de salas."""
from datetime import datetime, timedelta
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from src import armazenamento
from src.salas import cadastrar_sala, editar_sala, excluir_sala

# Carrega os cenários Gherkin
scenarios("features/edicao_exclusao_salas.feature")


# ---------------------------------------------------------------------------
# Contextos (Dado)
# ---------------------------------------------------------------------------
@given("que estou no sistema de gerenciamento de salas")
def dado_sistema_pronto():
    assert armazenamento.salas == []


@given(
    parsers.parse(
        'que existe uma sala cadastrada com nome "{nome}", capacidade {capacidade:d} e localização "{localizacao}"'
    ),
    target_fixture="sala_cadastrada",
)
def dado_sala_cadastrada(nome, capacidade, localizacao):
    return cadastrar_sala(nome, capacidade, localizacao)


@given("que existe uma sala cadastrada com reservas apenas no passado", target_fixture="sala_cadastrada")
def dado_sala_com_reservas_passadas():
    sala = cadastrar_sala("Sala Passada", 20, "Bloco A")
    armazenamento.reservas.append({
        "id": 1,
        "sala_id": sala["id"],
        "data_fim": datetime.now() - timedelta(days=1),
    })
    return sala


@given("que existe uma sala cadastrada com reservas futuras", target_fixture="sala_cadastrada")
def dado_sala_com_reservas_futuras():
    sala = cadastrar_sala("Sala Futura", 20, "Bloco A")
    armazenamento.reservas.append({
        "id": 1,
        "sala_id": sala["id"],
        "data_fim": datetime.now() + timedelta(days=2),
    })
    return sala


# ---------------------------------------------------------------------------
# Ações (Quando)
# ---------------------------------------------------------------------------
@when(
    parsers.parse(
        'altero o nome para "{nome}", a capacidade para {capacidade:d} e a localização para "{localizacao}"'
    ),
    target_fixture="resultado_edicao",
)
def quando_altero_todos_os_dados(sala_cadastrada, nome, capacidade, localizacao):
    try:
        sala = editar_sala(
            sala_cadastrada["id"],
            nome=nome,
            capacidade=capacidade,
            localizacao=localizacao,
        )
        return {"sala": sala, "erro": None}
    except ValueError as erro:
        return {"sala": None, "erro": str(erro)}


@when(
    parsers.parse('altero apenas a capacidade para {capacidade:d}'),
    target_fixture="resultado_edicao",
)
def quando_altero_apenas_capacidade(sala_cadastrada, capacidade):
    try:
        sala = editar_sala(sala_cadastrada["id"], capacidade=capacidade)
        return {"sala": sala, "erro": None}
    except ValueError as erro:
        return {"sala": None, "erro": str(erro)}


@when(
    parsers.parse('tento editar uma sala com id inexistente {id_sala:d}'),
    target_fixture="resultado_edicao",
)
def quando_tento_editar_sala_inexistente(id_sala):
    try:
        sala = editar_sala(id_sala, nome="Novo Nome")
        return {"sala": sala, "erro": None}
    except ValueError as erro:
        return {"sala": None, "erro": str(erro)}


@when(
    parsers.re(r'altero o nome para "(?P<nome>.*)"'),
    target_fixture="resultado_edicao",
)
def quando_altero_apenas_nome(sala_cadastrada, nome):
    try:
        sala = editar_sala(sala_cadastrada["id"], nome=nome)
        return {"sala": sala, "erro": None}
    except ValueError as erro:
        return {"sala": None, "erro": str(erro)}


@when(
    parsers.parse('altero a capacidade para {capacidade:d}'),
    target_fixture="resultado_edicao",
)
def quando_altero_capacidade_invalida(sala_cadastrada, capacidade):
    try:
        sala = editar_sala(sala_cadastrada["id"], capacidade=capacidade)
        return {"sala": sala, "erro": None}
    except ValueError as erro:
        return {"sala": None, "erro": str(erro)}


@when("solicito a exclusão da sala", target_fixture="resultado_exclusao")
def quando_solicito_exclusao(sala_cadastrada):
    try:
        excluir_sala(sala_cadastrada["id"])
        return {"erro": None}
    except ValueError as erro:
        return {"erro": str(erro)}


@when(
    parsers.parse('solicito a exclusão de uma sala com id {id_sala:d}'),
    target_fixture="resultado_exclusao",
)
def quando_solicito_exclusao_inexistente(id_sala):
    try:
        excluir_sala(id_sala)
        return {"erro": None}
    except ValueError as erro:
        return {"erro": str(erro)}


# ---------------------------------------------------------------------------
# Resultados esperados (Então)
# ---------------------------------------------------------------------------
@then("os dados da sala devem ser atualizados com sucesso")
def entao_dados_atualizados(resultado_edicao, sala_cadastrada):
    assert resultado_edicao["erro"] is None
    assert resultado_edicao["sala"]["id"] == sala_cadastrada["id"]
    assert resultado_edicao["sala"] in armazenamento.salas


@then(
    parsers.parse(
        'a capacidade da sala deve ser {capacidade:d} e os demais dados devem ser mantidos'
    )
)
def entao_apenas_capacidade_atualizada(resultado_edicao, sala_cadastrada, capacidade):
    assert resultado_edicao["erro"] is None
    assert resultado_edicao["sala"]["capacidade"] == capacidade
    assert resultado_edicao["sala"]["nome"] == sala_cadastrada["nome"]
    assert resultado_edicao["sala"]["localizacao"] == sala_cadastrada["localizacao"]


@then(parsers.parse('a alteração deve ser recusada com a mensagem "{mensagem}"'))
def entao_edicao_recusada(resultado_edicao, mensagem):
    assert resultado_edicao["erro"] == mensagem


@then(parsers.parse('a exclusão deve ser recusada com a mensagem "{mensagem}"'))
def entao_exclusao_recusada(resultado_exclusao, mensagem):
    assert resultado_exclusao["erro"] == mensagem


@then("os dados originais da sala devem ser mantidos")
def entao_dados_originais_mantidos(sala_cadastrada):
    sala_no_armazenamento = [s for s in armazenamento.salas if s["id"] == sala_cadastrada["id"]][0]
    assert sala_no_armazenamento["nome"] == sala_cadastrada["nome"]
    assert sala_no_armazenamento["capacidade"] == sala_cadastrada["capacidade"]
    assert sala_no_armazenamento["localizacao"] == sala_cadastrada["localizacao"]


@then("a sala deve ser removida do sistema com sucesso")
def entao_sala_removida_com_sucesso(resultado_exclusao, sala_cadastrada):
    assert resultado_exclusao["erro"] is None
    assert sala_cadastrada not in armazenamento.salas


@then("a sala deve permanecer cadastrada no sistema")
def entao_sala_permanece_cadastrada(sala_cadastrada):
    assert sala_cadastrada in armazenamento.salas
