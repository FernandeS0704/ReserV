"""Testes BDD das funcionalidades de cadastro e listagem de salas."""
from pytest_bdd import given, parsers, scenarios, then, when

from src import armazenamento
from src.salas import cadastrar_sala, formatar_listagem, listar_salas

# Transforma cada cenário do arquivo .feature em um teste do pytest.
# O caminho é relativo à pasta deste arquivo (tests).
scenarios("features/cadastro_salas.feature")


# ---------------------------------------------------------------------------
# Funções auxiliares (não são passos)
# ---------------------------------------------------------------------------
def _remover_aspas(texto):
    """Transforma '"Sala 01"' em 'Sala 01' e '""' em '' (texto vazio)."""
    return texto.strip('"')


def _converter_capacidade(texto):
    """Converte o texto em inteiro; se não der (ex.: 'abc'), devolve o texto."""
    try:
        return int(texto)
    except ValueError:
        return texto


# ---------------------------------------------------------------------------
# Dado (situação inicial)
# ---------------------------------------------------------------------------
@given("que estou no sistema de gerenciamento de salas")
def dado_sistema_pronto():
    # O conftest.py já zera o armazenamento antes de cada cenário.
    assert armazenamento.salas == []


@given("que existem salas cadastradas", target_fixture="salas_cadastradas")
def dado_existem_salas():
    return [
        cadastrar_sala("Sala 01", 20, "Bloco A"),
        cadastrar_sala("Sala 02", 30, "Bloco B"),
    ]


@given("que não existem salas cadastradas")
def dado_nao_existem_salas():
    assert armazenamento.salas == []

@when(
    parsers.parse(
        "informo o nome {nome}, a capacidade {capacidade} "
        "e a localização {localizacao}"
    ),
    target_fixture="resultado",
)
def quando_informo_dados(nome, capacidade, localizacao):
    """Tenta cadastrar a sala e guarda o resultado (sala criada ou erro)."""
    try:
        sala = cadastrar_sala(
            _remover_aspas(nome),
            _converter_capacidade(capacidade),
            _remover_aspas(localizacao),
        )
    except ValueError as erro:
        return {"sala": None, "erro": str(erro)}
    return {"sala": sala, "erro": None}


@when("solicito a listagem de salas", target_fixture="listagem")
def quando_solicito_listagem():
    salas = listar_salas()
    return {"salas": salas, "texto": formatar_listagem(salas)}


@then("a sala deve ser cadastrada com sucesso")
def entao_sala_cadastrada(resultado):
    assert resultado["erro"] is None
    assert resultado["sala"] in armazenamento.salas


@then("a sala deve receber um identificador único")
def entao_identificador_unico(resultado):
    ids = [sala["id"] for sala in armazenamento.salas]
    assert isinstance(resultado["sala"]["id"], int)
    assert ids.count(resultado["sala"]["id"]) == 1


@then("as duas salas devem estar cadastradas com identificadores diferentes")
def entao_duas_salas_ids_diferentes():
    ids = [sala["id"] for sala in armazenamento.salas]
    assert len(ids) == 2
    assert len(set(ids)) == 2


@then(parsers.parse('o cadastro deve ser recusado com a mensagem "{mensagem}"'))
def entao_cadastro_recusado(resultado, mensagem):
    assert resultado["sala"] is None
    assert resultado["erro"] == mensagem


@then("nenhuma sala deve ser adicionada à lista")
def entao_nenhuma_sala_adicionada():
    assert armazenamento.salas == []

@then("o sistema deve apresentar todas as salas cadastradas")
def entao_todas_as_salas(listagem, salas_cadastradas):
    assert listagem["salas"] == salas_cadastradas
    for sala in salas_cadastradas:
        assert sala["nome"] in listagem["texto"]


@then(
    "a listagem deve mostrar o identificador, o nome, a capacidade "
    "e a localização de cada sala"
)
def entao_listagem_mostra_dados(listagem, salas_cadastradas):
    linhas = listagem["texto"].splitlines()

    for titulo in ["ID", "Nome", "Capacidade", "Localização"]:
        assert titulo in linhas[0]

    for sala, linha in zip(salas_cadastradas, linhas[2:]):
        for valor in (sala["id"], sala["nome"], sala["capacidade"], sala["localizacao"]):
            assert str(valor) in linha


@then("o sistema deve informar que não há salas disponíveis")
def entao_sem_salas(listagem):
    assert "não há salas disponíveis" in listagem["texto"].lower()