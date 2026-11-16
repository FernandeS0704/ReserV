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
