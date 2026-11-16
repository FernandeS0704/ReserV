import pytest

from src.buscas import buscar_salas
from src.salas import cadastrar_sala


def test_buscar_salas_por_capacidade_minima():
    cadastrar_sala("Sala 01", 10, "Bloco A")
    media = cadastrar_sala("Laboratório", 30, "Bloco B")
    grande = cadastrar_sala("Auditório", 100, "Bloco B")

    resultado = buscar_salas(capacidade_minima=30)

    assert resultado == [media, grande]


def test_buscar_salas_inclui_sala_com_capacidade_igual_ao_minimo():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    assert buscar_salas(capacidade_minima=20) == [sala]


def test_buscar_salas_sem_resultado_devolve_lista_vazia():
    cadastrar_sala("Sala 01", 10, "Bloco A")

    assert buscar_salas(capacidade_minima=50) == []


def test_buscar_salas_sem_salas_cadastradas_devolve_lista_vazia():
    assert buscar_salas(capacidade_minima=10) == []


def test_buscar_salas_por_localizacao():
    sala1 = cadastrar_sala("Sala 01", 20, "Bloco A")
    cadastrar_sala("Auditório", 100, "Bloco B")
    sala3 = cadastrar_sala("Laboratório", 30, "Bloco A")

    assert buscar_salas(localizacao="Bloco A") == [sala1, sala3]


def test_buscar_salas_por_localizacao_ignora_maiusculas_e_minusculas():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A")

    assert buscar_salas(localizacao="bloco a") == [sala]


def test_buscar_salas_por_localizacao_aceita_parte_do_texto():
    sala = cadastrar_sala("Sala 01", 20, "Bloco A - 2º andar")
    cadastrar_sala("Sala 02", 20, "Bloco B")

    assert buscar_salas(localizacao="2º andar") == [sala]


def test_buscar_salas_combinando_capacidade_e_localizacao():
    cadastrar_sala("Sala 01", 10, "Bloco A")
    alvo = cadastrar_sala("Laboratório", 30, "Bloco A")
    cadastrar_sala("Auditório", 100, "Bloco B")

    assert buscar_salas(capacidade_minima=20, localizacao="Bloco A") == [alvo]


def test_nao_buscar_sem_nenhum_criterio():
    cadastrar_sala("Sala 01", 20, "Bloco A")

    with pytest.raises(ValueError, match="critério"):
        buscar_salas()


@pytest.mark.parametrize("valor", [0, -5, "abc", 2.5, True])
def test_nao_buscar_com_capacidade_minima_invalida(valor):
    with pytest.raises(ValueError, match="capacidade mínima"):
        buscar_salas(capacidade_minima=valor)


@pytest.mark.parametrize("valor", ["", "   ", 10])
def test_nao_buscar_com_localizacao_invalida(valor):
    with pytest.raises(ValueError, match="localização"):
        buscar_salas(localizacao=valor)
